# AI Dream Interpreter

A comprehensive AI-powered dream interpretation system that analyzes dream content using advanced NLP and provides psychological insights through symbolic analysis and conversational AI.

## 🌟 Features

### Core Functionality
- **Dream Text Analysis**: Advanced NLP processing using HuggingFace transformers (BERT/T5)
- **Voice Input**: Speech-to-text transcription using OpenAI Whisper API
- **Symbolic Interpretation**: Curated symbolic dictionary with psychological meanings
- **AI-Powered Insights**: GPT-4 integration for deep psychological analysis
- **Conversational Interface**: Interactive Q&A for follow-up questions
- **Feedback System**: User corrections and ratings for continuous improvement

### Technical Features
- **Modern Frontend**: Next.js with TypeScript, Tailwind CSS, and shadcn/ui
- **Robust Backend**: FastAPI with SQLAlchemy and PostgreSQL
- **Real-time Processing**: Async processing with progress tracking
- **Containerized Deployment**: Docker Compose for easy deployment
- **Responsive Design**: Mobile-first design with beautiful animations
- **Production Ready**: Comprehensive error handling and logging

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│ (PostgreSQL)    │
│                 │    │                 │    │                 │
│ • Dream Input   │    │ • NLP Pipeline  │    │ • Dreams        │
│ • Voice Record  │    │ • Symbol Mapper │    │ • Interpretations│
│ • Chat UI       │    │ • OpenAI API    │    │ • Feedback      │
│ • Feedback      │    │ • Whisper API   │    │ • Analytics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  External APIs  │
                    │                 │
                    │ • OpenAI GPT-4  │
                    │ • Whisper API   │
                    │ • Stable Diff.  │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose
- OpenAI API key

### 1. Clone Repository
```bash
git clone <repository-url>
cd ai-dream-interpreter
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Add your OpenAI API key
echo "OPENAI_API_KEY=your-api-key-here" >> .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
```

### 3. Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 4. Manual Setup (Development)

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (using Docker)
docker run -d \
  --name dreams_db \
  -e POSTGRES_DB=dreams_db \
  -e POSTGRES_USER=dreams_user \
  -e POSTGRES_PASSWORD=dreams_password \
  -p 5432:5432 \
  postgres:15

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Access at http://localhost:3000
```

## 📁 Project Structure

```
ai-dream-interpreter/
├── app/                          # Next.js frontend
│   ├── page.tsx                 # Main dream interpreter interface
│   ├── layout.tsx               # App layout and metadata
│   └── globals.css              # Global styles
├── backend/                      # FastAPI backend
│   ├── main.py                  # FastAPI app and routes
│   ├── nlp/                     # NLP processing modules
│   │   ├── dream_analyzer.py    # Core dream analysis
│   │   └── symbol_mapper.py     # Symbol interpretation
│   ├── services/                # External service integrations
│   │   ├── openai_service.py    # OpenAI GPT integration
│   │   └── whisper_service.py   # Speech transcription
│   ├── database/                # Database models and config
│   │   └── models.py            # SQLAlchemy models
│   └── utils/                   # Utilities and config
│       └── config.py            # Application settings
├── data/                        # Data files
│   └── symbols.json             # Symbolic dictionary
├── components/                  # Reusable React components
│   └── ui/                     # shadcn/ui components
├── docker-compose.yml          # Multi-container setup
├── Dockerfile                  # Frontend container
├── backend/Dockerfile          # Backend container
└── README.md                   # This file
```

## 🔌 API Endpoints

### Core Endpoints
- `POST /analyze_dream` - Analyze dream text and return interpretation
- `POST /feedback` - Submit user feedback on interpretations
- `POST /conversation` - Continue conversation about interpretation
- `POST /transcribe` - Convert audio to text using Whisper
- `GET /visualize/{interpretation_id}` - Generate dream visualization

### Example API Usage
```python
import httpx

# Analyze a dream
response = httpx.post("http://localhost:8000/analyze_dream", json={
    "dream_text": "I was flying over a vast ocean when I saw a golden key floating in the water...",
    "user_id": "user123",
    "language": "en"
})

interpretation = response.json()
print(interpretation["interpretation"])
```

## 🧠 NLP Pipeline

### 1. Preprocessing
- Text cleaning and normalization
- Tokenization and entity extraction
- Emotion and sentiment analysis

### 2. Symbol Extraction
- Pattern matching for common dream symbols
- Contextual analysis using BERT embeddings
- Confidence scoring for symbol relevance

### 3. Interpretation Generation
- Symbolic dictionary lookup
- GPT-4 psychological analysis
- Cultural context integration
- Archetypal pattern recognition (Jungian)

### 4. Conversational AI
- Context-aware follow-up responses
- Memory of previous interpretations
- Personalized insights based on user feedback

## 🎨 Frontend Features

### User Interface
- **Modern Design**: Clean, intuitive interface with smooth animations
- **Voice Input**: Web Speech API integration for voice recording
- **Chat Interface**: WhatsApp-style conversation view
- **Progress Tracking**: Real-time analysis progress with loading states
- **Responsive Design**: Optimized for mobile, tablet, and desktop

### User Experience
- **Instant Feedback**: Thumbs up/down for quick responses
- **Follow-up Questions**: Natural conversation flow
- **Symbol Highlighting**: Interactive symbol exploration
- **Personalization**: Learns from user preferences

## 🔧 Configuration

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://dreams_user:dreams_password@localhost:5432/dreams_db
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key
DEBUG=false
OPENAI_MODEL=gpt-4
MAX_AUDIO_FILE_SIZE=10485760

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Customization Options
- **Symbolic Dictionary**: Add custom symbols in `data/symbols.json`
- **Cultural Contexts**: Extend cultural interpretations
- **NLP Models**: Swap HuggingFace models for different languages
- **UI Themes**: Customize Tailwind configuration

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=.
```

### Frontend Tests
```bash
npm test
npm run test:e2e
```

## 🚀 Deployment

### Production Deployment
```bash
# Build and deploy with Docker Compose
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Or use individual services
docker build -t dreams-backend ./backend
docker build -t dreams-frontend .
```

### Cloud Deployment Options
- **AWS**: ECS, RDS, S3 for audio files
- **Google Cloud**: Cloud Run, Cloud SQL, Cloud Storage
- **Azure**: Container Instances, Azure Database
- **Vercel**: Frontend deployment with serverless functions

## 📊 Analytics & Monitoring

### Built-in Analytics
- Dream analysis frequency
- Symbol usage statistics
- User feedback tracking
- Performance metrics

### Monitoring Stack
- **Logs**: Structured logging with timestamps
- **Metrics**: Prometheus integration ready
- **Health Checks**: Database and service health endpoints
- **Error Tracking**: Comprehensive error logging

## 🔒 Security Considerations

- **API Rate Limiting**: Prevents abuse
- **Input Sanitization**: SQL injection prevention
- **Authentication**: JWT token support (ready to implement)
- **Data Privacy**: User data encryption options
- **CORS Configuration**: Secure cross-origin requests

## 🛠 Development

### Adding New Features
1. **New Symbols**: Add to `data/symbols.json` with meanings
2. **Custom Analysis**: Extend `DreamAnalyzer` class
3. **UI Components**: Use shadcn/ui component system
4. **API Endpoints**: Follow FastAPI patterns in `main.py`

### Code Style
- **Backend**: Black formatting, type hints
- **Frontend**: Prettier, ESLint, TypeScript strict mode
- **Database**: SQLAlchemy ORM with Alembic migrations

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request with detailed description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 and Whisper API
- **HuggingFace** for transformer models
- **Jung & Freud** for psychological frameworks
- **Hall & Van de Castle** for dream coding methodology
- **shadcn/ui** for beautiful UI components

## 📞 Support

For issues, questions, or contributions:
- **Issues**: GitHub Issues tab
- **Discussions**: GitHub Discussions
- **Documentation**: `/docs` endpoint when running

---

**Ready to explore the mysteries of your dreams? Start your journey with AI Dream Interpreter!** 🌙✨