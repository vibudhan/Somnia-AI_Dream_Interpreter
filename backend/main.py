"""
AI Dream Interpreter - FastAPI Backend
Production-ready API server with NLP pipeline and database integration
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
import os
import json
import logging
from contextlib import asynccontextmanager

# Import our custom modules
from nlp.dream_analyzer import DreamAnalyzer
from nlp.symbol_mapper import SymbolMapper
from services.openai_service import OpenAIService
from services.whisper_service import WhisperService
from database.models import Dream, Interpretation, Feedback
from utils.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
dream_analyzer = DreamAnalyzer()
symbol_mapper = SymbolMapper()
openai_service = OpenAIService()
whisper_service = WhisperService()

# Database setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dreams_db")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting AI Dream Interpreter API...")
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Shutting down AI Dream Interpreter API...")

# Initialize FastAPI app
app = FastAPI(
    title="AI Dream Interpreter API",
    description="Advanced NLP-powered dream analysis and interpretation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class DreamAnalysisRequest(BaseModel):
    dream_text: str
    user_id: Optional[str] = None
    language: str = "en"

class SymbolModel(BaseModel):
    symbol: str
    meaning: str
    confidence: float
    category: str

class DreamAnalysisResponse(BaseModel):
    id: str
    symbols: List[SymbolModel]
    psychological_insights: List[str]
    emotional_tone: str
    interpretation: str
    confidence_score: float
    processing_time_ms: int

class FeedbackRequest(BaseModel):
    interpretation_id: str
    feedback_type: str  # 'positive', 'negative', 'clarification'
    feedback_text: Optional[str] = None
    user_corrections: Optional[Dict] = None

class ConversationRequest(BaseModel):
    interpretation_id: str
    message: str
    context: Optional[Dict] = None

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication dependency (placeholder)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In production, implement proper JWT validation
    return {"user_id": "anonymous"}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Dream Interpreter API",
        "status": "active",
        "version": "1.0.0"
    }

@app.post("/analyze_dream", response_model=DreamAnalysisResponse)
async def analyze_dream(
    request: DreamAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Analyze a dream text and return symbolic and psychological interpretations
    """
    try:
        start_time = datetime.now()
        
        # Step 1: Clean and preprocess the dream text
        cleaned_text = dream_analyzer.preprocess_text(request.dream_text)
        
        # Step 2: Extract entities, symbols, and emotions
        extracted_data = dream_analyzer.extract_dream_elements(cleaned_text)
        
        # Step 3: Map symbols to meanings using our curated dictionary
        symbols = symbol_mapper.map_symbols(extracted_data['symbols'])
        
        # Step 4: Get psychological insights from OpenAI
        psychological_insights = await openai_service.get_psychological_interpretation(
            dream_text=request.dream_text,
            extracted_symbols=symbols,
            emotional_tone=extracted_data['emotional_tone']
        )
        
        # Step 5: Generate comprehensive interpretation
        full_interpretation = await openai_service.generate_interpretation(
            dream_text=request.dream_text,
            symbols=symbols,
            insights=psychological_insights
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Create response
        response = DreamAnalysisResponse(
            id=str(hash(request.dream_text + str(start_time))),
            symbols=[
                SymbolModel(
                    symbol=s['symbol'],
                    meaning=s['meaning'],
                    confidence=s['confidence'],
                    category=s.get('category', 'general')
                ) for s in symbols
            ],
            psychological_insights=psychological_insights,
            emotional_tone=extracted_data['emotional_tone'],
            interpretation=full_interpretation,
            confidence_score=sum(s['confidence'] for s in symbols) / len(symbols) if symbols else 0.0,
            processing_time_ms=int(processing_time)
        )
        
        # Store in database (background task)
        background_tasks.add_task(
            store_dream_analysis,
            db, request.dream_text, response, current_user['user_id']
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Dream analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Submit feedback for an interpretation
    """
    try:
        # Store feedback in database
        feedback = Feedback(
            interpretation_id=request.interpretation_id,
            user_id=current_user['user_id'],
            feedback_type=request.feedback_type,
            feedback_text=request.feedback_text,
            user_corrections=json.dumps(request.user_corrections) if request.user_corrections else None,
            created_at=datetime.now()
        )
        
        db.add(feedback)
        db.commit()
        
        return {"status": "success", "message": "Feedback recorded"}
        
    except Exception as e:
        logger.error(f"Feedback submission failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to record feedback")

@app.post("/conversation")
async def continue_conversation(
    request: ConversationRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Handle follow-up questions and conversation about dream interpretation
    """
    try:
        # Get original interpretation context
        interpretation = db.query(Interpretation).filter(
            Interpretation.id == request.interpretation_id
        ).first()
        
        if not interpretation:
            raise HTTPException(status_code=404, detail="Interpretation not found")
        
        # Generate contextual response using OpenAI
        response = await openai_service.generate_conversational_response(
            original_dream=interpretation.dream_text,
            original_interpretation=interpretation.full_interpretation,
            user_question=request.message,
            context=request.context
        )
        
        return {
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Conversation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

@app.post("/transcribe")
async def transcribe_audio(
    audio_file: bytes,
    current_user = Depends(get_current_user)
):
    """
    Transcribe audio to text using Whisper API
    """
    try:
        transcription = await whisper_service.transcribe(audio_file)
        return {"transcription": transcription}
        
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to transcribe audio")

@app.get("/visualize/{interpretation_id}")
async def generate_dream_visualization(
    interpretation_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Generate visual representation of dream using Stable Diffusion
    """
    try:
        # Get interpretation
        interpretation = db.query(Interpretation).filter(
            Interpretation.id == interpretation_id
        ).first()
        
        if not interpretation:
            raise HTTPException(status_code=404, detail="Interpretation not found")
        
        # Generate visualization prompt from symbols and interpretation
        visual_prompt = create_visualization_prompt(
            interpretation.symbols_data,
            interpretation.full_interpretation
        )
        
        # This would integrate with Stable Diffusion API
        # For now, return the prompt
        return {
            "visualization_prompt": visual_prompt,
            "status": "generation_queued",
            "message": "Visualization generation not implemented in skeleton version"
        }
        
    except Exception as e:
        logger.error(f"Visualization generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate visualization")

# Utility functions
async def store_dream_analysis(db: Session, dream_text: str, response: DreamAnalysisResponse, user_id: str):
    """Store dream analysis in database"""
    try:
        dream = Dream(
            user_id=user_id,
            dream_text=dream_text,
            created_at=datetime.now()
        )
        db.add(dream)
        db.flush()
        
        interpretation = Interpretation(
            dream_id=dream.id,
            symbols_data=json.dumps([s.dict() for s in response.symbols]),
            psychological_insights=json.dumps(response.psychological_insights),
            emotional_tone=response.emotional_tone,
            full_interpretation=response.interpretation,
            confidence_score=response.confidence_score,
            processing_time_ms=response.processing_time_ms,
            created_at=datetime.now()
        )
        db.add(interpretation)
        db.commit()
        
    except Exception as e:
        logger.error(f"Failed to store analysis: {str(e)}")
        db.rollback()

def create_visualization_prompt(symbols_data: str, interpretation: str) -> str:
    """Create a prompt for dream visualization"""
    symbols = json.loads(symbols_data)
    prompt_parts = []
    
    for symbol in symbols[:3]:  # Use top 3 symbols
        prompt_parts.append(f"{symbol['symbol']} representing {symbol['meaning']}")
    
    prompt = f"A surreal dreamlike scene featuring {', '.join(prompt_parts)}, artistic, ethereal, symbolic"
    return prompt

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)