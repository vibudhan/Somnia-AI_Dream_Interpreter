"""
Dream Analyzer - NLP preprocessing and entity extraction
Uses HuggingFace transformers for advanced text analysis
"""

import re
import json
from typing import Dict, List, Tuple
from datetime import datetime
import logging

# In production, install these packages:
# from transformers import pipeline, AutoTokenizer, AutoModel
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk.corpus import stopwords
# import nltk
# import torch

logger = logging.getLogger(__name__)

class DreamAnalyzer:
    """
    Advanced NLP processor for dream text analysis
    """
    
    def __init__(self):
        """Initialize the dream analyzer with ML models"""
        try:
            # In production environment:
            # self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
            # self.model = AutoModel.from_pretrained('bert-base-uncased')
            # self.sentiment_analyzer = SentimentIntensityAnalyzer()
            # self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
            # self.emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
            
            # For skeleton version, use mock components
            self.initialized = True
            logger.info("Dream Analyzer initialized (skeleton mode)")
            
        except Exception as e:
            logger.error(f"Failed to initialize Dream Analyzer: {e}")
            self.initialized = False

    def preprocess_text(self, dream_text: str) -> str:
        """
        Clean and preprocess dream text
        """
        try:
            # Remove extra whitespace
            cleaned = re.sub(r'\s+', ' ', dream_text.strip())
            
            # Normalize punctuation
            cleaned = re.sub(r'\.{2,}', '.', cleaned)
            cleaned = re.sub(r'\?{2,}', '?', cleaned)
            cleaned = re.sub(r'!{2,}', '!', cleaned)
            
            # Fix common OCR errors if text was transcribed
            cleaned = self._fix_common_errors(cleaned)
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Text preprocessing failed: {e}")
            return dream_text

    def extract_dream_elements(self, dream_text: str) -> Dict:
        """
        Extract symbols, entities, emotions, and themes from dream text
        """
        try:
            # In production, this would use advanced NLP models
            # entities = self.ner_pipeline(dream_text)
            # emotions = self.emotion_pipeline(dream_text)
            # sentiment = self.sentiment_analyzer.polarity_scores(dream_text)
            
            # For skeleton version, use pattern matching and heuristics
            extracted = {
                'symbols': self._extract_symbols_heuristic(dream_text),
                'entities': self._extract_entities_heuristic(dream_text),
                'emotions': self._extract_emotions_heuristic(dream_text),
                'emotional_tone': self._determine_emotional_tone(dream_text),
                'themes': self._extract_themes(dream_text),
                'archetypes': self._identify_archetypes(dream_text)
            }
            
            return extracted
            
        except Exception as e:
            logger.error(f"Dream element extraction failed: {e}")
            return {
                'symbols': [],
                'entities': [],
                'emotions': [],
                'emotional_tone': 'neutral',
                'themes': [],
                'archetypes': []
            }

    def _extract_symbols_heuristic(self, text: str) -> List[Dict]:
        """
        Extract common dream symbols using pattern matching
        """
        # Common dream symbols with their typical categories
        symbol_patterns = {
            # Animals
            'animals': ['dog', 'cat', 'bird', 'snake', 'spider', 'horse', 'wolf', 'bear', 'lion', 'fish', 'butterfly'],
            # Water elements
            'water': ['water', 'ocean', 'sea', 'lake', 'river', 'rain', 'swimming', 'drowning', 'flood', 'waves'],
            # Flight and movement
            'flight': ['flying', 'falling', 'jumping', 'running', 'climbing', 'soaring', 'floating'],
            # People and relationships
            'people': ['mother', 'father', 'family', 'friend', 'stranger', 'child', 'baby', 'lover', 'teacher'],
            # Places and structures
            'places': ['house', 'school', 'workplace', 'forest', 'mountain', 'cave', 'bridge', 'door', 'window', 'room'],
            # Objects and tools
            'objects': ['car', 'phone', 'mirror', 'key', 'book', 'money', 'clothes', 'food', 'fire', 'light'],
            # Abstract concepts
            'abstract': ['death', 'birth', 'lost', 'found', 'trapped', 'free', 'hidden', 'revealed', 'broken', 'whole']
        }
        
        found_symbols = []
        text_lower = text.lower()
        
        for category, symbols in symbol_patterns.items():
            for symbol in symbols:
                if symbol in text_lower:
                    # Calculate simple confidence based on context
                    confidence = self._calculate_symbol_confidence(symbol, text)
                    
                    found_symbols.append({
                        'symbol': symbol.title(),
                        'category': category,
                        'confidence': confidence,
                        'context': self._get_symbol_context(symbol, text)
                    })
        
        # Sort by confidence and return top symbols
        return sorted(found_symbols, key=lambda x: x['confidence'], reverse=True)[:10]

    def _extract_entities_heuristic(self, text: str) -> List[Dict]:
        """
        Extract named entities and important nouns
        """
        # Simple entity extraction for skeleton version
        # In production, use spaCy or BERT-based NER
        
        # Pattern for proper nouns (capitalized words)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', text)
        
        entities = []
        for noun in set(proper_nouns):
            entities.append({
                'text': noun,
                'type': 'PERSON',  # Would be classified properly in production
                'confidence': 0.8
            })
        
        return entities

    def _extract_emotions_heuristic(self, text: str) -> List[Dict]:
        """
        Extract emotional content from the dream
        """
        emotion_keywords = {
            'fear': ['scared', 'afraid', 'terrified', 'frightened', 'anxious', 'worried', 'panic'],
            'joy': ['happy', 'excited', 'joyful', 'elated', 'cheerful', 'delighted', 'pleased'],
            'sadness': ['sad', 'depressed', 'melancholy', 'grief', 'sorrow', 'disappointed'],
            'anger': ['angry', 'furious', 'mad', 'irritated', 'frustrated', 'rage'],
            'surprise': ['surprised', 'amazed', 'shocked', 'astonished', 'stunned'],
            'confusion': ['confused', 'puzzled', 'lost', 'uncertain', 'bewildered'],
            'peace': ['peaceful', 'calm', 'serene', 'relaxed', 'tranquil', 'content']
        }
        
        found_emotions = []
        text_lower = text.lower()
        
        for emotion, keywords in emotion_keywords.items():
            emotion_score = sum(1 for keyword in keywords if keyword in text_lower)
            if emotion_score > 0:
                found_emotions.append({
                    'emotion': emotion,
                    'intensity': min(emotion_score / len(keywords), 1.0),
                    'keywords_found': [kw for kw in keywords if kw in text_lower]
                })
        
        return sorted(found_emotions, key=lambda x: x['intensity'], reverse=True)

    def _determine_emotional_tone(self, text: str) -> str:
        """
        Determine overall emotional tone of the dream
        """
        emotions = self._extract_emotions_heuristic(text)
        
        if not emotions:
            return 'neutral'
        
        # Return the strongest emotion as overall tone
        dominant_emotion = emotions[0]['emotion']
        
        # Map to broader categories
        tone_mapping = {
            'fear': 'anxious',
            'joy': 'positive',
            'sadness': 'melancholic',
            'anger': 'intense',
            'surprise': 'transformative',
            'confusion': 'uncertain',
            'peace': 'serene'
        }
        
        return tone_mapping.get(dominant_emotion, 'neutral')

    def _extract_themes(self, text: str) -> List[str]:
        """
        Identify major themes in the dream using Hall & Van de Castle framework
        """
        themes = {
            'transformation': ['changing', 'becoming', 'turning', 'growing', 'shrinking', 'metamorphosis'],
            'journey': ['traveling', 'walking', 'driving', 'path', 'road', 'destination', 'journey'],
            'conflict': ['fighting', 'arguing', 'battle', 'war', 'struggle', 'competition'],
            'relationships': ['meeting', 'talking', 'loving', 'friendship', 'family', 'romantic'],
            'achievement': ['winning', 'success', 'graduation', 'promotion', 'accomplishment'],
            'loss': ['losing', 'missing', 'dead', 'gone', 'lost', 'disappeared'],
            'exploration': ['discovering', 'exploring', 'finding', 'searching', 'adventure']
        }
        
        found_themes = []
        text_lower = text.lower()
        
        for theme, keywords in themes.items():
            if any(keyword in text_lower for keyword in keywords):
                found_themes.append(theme)
        
        return found_themes

    def _identify_archetypes(self, text: str) -> List[str]:
        """
        Identify Jungian archetypes present in the dream
        """
        archetypes = {
            'hero': ['saving', 'rescuing', 'fighting', 'brave', 'courage', 'quest'],
            'shadow': ['dark', 'evil', 'monster', 'demon', 'enemy', 'hidden'],
            'anima_animus': ['mysterious person', 'guide', 'wise', 'beautiful', 'handsome'],
            'mother': ['nurturing', 'caring', 'protective', 'feeding', 'mother'],
            'father': ['authority', 'teaching', 'guiding', 'strong', 'father'],
            'trickster': ['joking', 'laughing', 'fooling', 'mischief', 'playful'],
            'wise_old_man': ['teacher', 'mentor', 'advice', 'wisdom', 'elder']
        }
        
        found_archetypes = []
        text_lower = text.lower()
        
        for archetype, keywords in archetypes.items():
            if any(keyword in text_lower for keyword in keywords):
                found_archetypes.append(archetype)
        
        return found_archetypes

    def _calculate_symbol_confidence(self, symbol: str, text: str) -> float:
        """
        Calculate confidence score for symbol extraction
        """
        # Simple confidence based on frequency and context
        frequency = text.lower().count(symbol.lower())
        
        # Base confidence on frequency
        confidence = min(frequency * 0.3 + 0.4, 1.0)
        
        # Boost confidence if symbol appears in important positions
        if symbol.lower() in text[:50].lower():  # Beginning of text
            confidence += 0.1
        
        if symbol.lower() in text[-50:].lower():  # End of text
            confidence += 0.1
        
        return min(confidence, 1.0)

    def _get_symbol_context(self, symbol: str, text: str, window: int = 30) -> str:
        """
        Get contextual text around the symbol
        """
        text_lower = text.lower()
        symbol_lower = symbol.lower()
        
        index = text_lower.find(symbol_lower)
        if index == -1:
            return ""
        
        start = max(0, index - window)
        end = min(len(text), index + len(symbol) + window)
        
        return text[start:end].strip()

    def _fix_common_errors(self, text: str) -> str:
        """
        Fix common transcription errors
        """
        # Common speech-to-text errors
        corrections = {
            ' there was ': ' I was ',
            ' they was ': ' I was ',
            ' we was ': ' I was ',
        }
        
        for error, correction in corrections.items():
            text = text.replace(error, correction)
        
        return text

    def get_embeddings(self, text: str):
        """
        Generate text embeddings for similarity analysis
        In production, this would use BERT or similar
        """
        # Placeholder for embedding generation
        # In production:
        # inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        # outputs = self.model(**inputs)
        # return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        
        return [0.1] * 768  # Mock embedding vector