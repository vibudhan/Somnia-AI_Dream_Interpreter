"""
OpenAI Service - Integrates with OpenAI API for dream interpretation
Handles GPT-4 requests for psychological insights and conversational responses
"""

import os
import openai
from typing import List, Dict, Optional
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenAIService:
    """
    Service for integrating with OpenAI API for dream interpretation
    """
    
    def __init__(self):
        """Initialize OpenAI client"""
        # In production, set this via environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
            self.enabled = True
        else:
            logger.warning("OpenAI API key not found. Service will return mock responses.")
            self.enabled = False
        
        # Configuration
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    async def get_psychological_interpretation(self, dream_text: str, 
                                            extracted_symbols: List[Dict], 
                                            emotional_tone: str) -> List[str]:
        """
        Get psychological insights from OpenAI based on dream content
        """
        try:
            if not self.enabled:
                return self._get_mock_psychological_insights()
            
            # Prepare symbols context
            symbols_context = ", ".join([f"{s['symbol']} ({s['meaning']})" 
                                       for s in extracted_symbols[:5]])
            
            prompt = self._create_psychological_prompt(dream_text, symbols_context, emotional_tone)
            
            response = await self._make_openai_request(prompt)
            insights = self._parse_insights_response(response)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get psychological interpretation: {e}")
            return self._get_mock_psychological_insights()

    async def generate_interpretation(self, dream_text: str, 
                                    symbols: List[Dict], 
                                    insights: List[str]) -> str:
        """
        Generate comprehensive dream interpretation
        """
        try:
            if not self.enabled:
                return self._get_mock_interpretation()
            
            prompt = self._create_interpretation_prompt(dream_text, symbols, insights)
            response = await self._make_openai_request(prompt)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate interpretation: {e}")
            return self._get_mock_interpretation()

    async def generate_conversational_response(self, original_dream: str, 
                                             original_interpretation: str,
                                             user_question: str, 
                                             context: Optional[Dict] = None) -> str:
        """
        Generate contextual response for follow-up questions
        """
        try:
            if not self.enabled:
                return self._get_mock_conversational_response(user_question)
            
            prompt = self._create_conversation_prompt(
                original_dream, original_interpretation, user_question, context
            )
            
            response = await self._make_openai_request(prompt, temperature=0.8)
            return response.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate conversational response: {e}")
            return self._get_mock_conversational_response(user_question)

    def _create_psychological_prompt(self, dream_text: str, symbols_context: str, 
                                   emotional_tone: str) -> str:
        """Create prompt for psychological analysis"""
        return f"""
You are an expert dream analyst with deep knowledge of psychology, particularly Jungian analysis, Freudian theory, and modern dream research. 

Analyze this dream and provide 3-5 psychological insights:

Dream: "{dream_text}"

Detected symbols: {symbols_context}
Emotional tone: {emotional_tone}

Please provide insights that:
1. Connect the symbols to possible psychological meanings
2. Consider the emotional context
3. Relate to potential waking life concerns
4. Use established psychological frameworks
5. Are supportive and constructive

Format as a numbered list of insights, each 1-2 sentences long.
"""

    def _create_interpretation_prompt(self, dream_text: str, symbols: List[Dict], 
                                    insights: List[str]) -> str:
        """Create prompt for comprehensive interpretation"""
        symbols_text = "\n".join([f"- {s['symbol']}: {s['meaning']}" for s in symbols[:5]])
        insights_text = "\n".join([f"- {insight}" for insight in insights])
        
        return f"""
As a professional dream interpreter, provide a comprehensive yet accessible interpretation of this dream.

Dream: "{dream_text}"

Key Symbols:
{symbols_text}

Psychological Insights:
{insights_text}

Create a cohesive interpretation that:
1. Weaves together the symbols and insights
2. Provides practical relevance to the dreamer's life
3. Is encouraging and constructive
4. Is 2-3 paragraphs long
5. Uses accessible language while maintaining depth

Begin with "This dream appears to..." and provide a thoughtful, integrated analysis.
"""

    def _create_conversation_prompt(self, original_dream: str, original_interpretation: str,
                                  user_question: str, context: Optional[Dict]) -> str:
        """Create prompt for conversational follow-up"""
        return f"""
You are continuing a conversation about a dream interpretation. The user has a follow-up question.

Original Dream: "{original_dream}"

Original Interpretation: "{original_interpretation}"

User's Question: "{user_question}"

Provide a helpful, conversational response that:
1. Directly addresses their question
2. References the original dream and interpretation
3. Offers additional insights if relevant
4. Is supportive and encouraging
5. Is 1-2 paragraphs long

Maintain the tone of a knowledgeable but approachable dream counselor.
"""

    async def _make_openai_request(self, prompt: str, temperature: float = None) -> str:
        """Make request to OpenAI API with error handling"""
        try:
            # In production, use the official openai client:
            # response = await openai.ChatCompletion.acreate(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are an expert dream analyst."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     max_tokens=self.max_tokens,
            #     temperature=temperature or self.temperature
            # )
            # return response.choices[0].message.content
            
            # For skeleton version, simulate API delay and return mock response
            await asyncio.sleep(1)
            return self._generate_mock_response(prompt)
            
        except Exception as e:
            logger.error(f"OpenAI API request failed: {e}")
            raise

    def _generate_mock_response(self, prompt: str) -> str:
        """Generate mock response based on prompt type"""
        if "psychological insights" in prompt.lower():
            return """1. This dream suggests you're processing feelings of transformation in your life.
2. The symbols indicate a desire for greater freedom and perspective.
3. The emotional tone reflects inner conflicts between security and growth.
4. Your subconscious may be preparing you for upcoming changes."""

        elif "comprehensive interpretation" in prompt.lower():
            return """This dream appears to reflect a significant period of personal transformation you're experiencing. The symbolic elements suggest your psyche is processing the balance between staying grounded in familiar territory while yearning for the freedom to explore new possibilities. The interplay of these symbols indicates that you're at a crossroads where growth requires letting go of old patterns that no longer serve you.

The emotional undertones of your dream suggest that while change can feel uncertain, your unconscious mind is actually preparing you for positive developments ahead. This dream may be encouraging you to trust in your ability to navigate transitions and to embrace the opportunities for expansion that lie before you."""

        else:
            return """That's a thoughtful question about your dream symbolism. Based on the elements in your original dream, this particular aspect often represents the psyche's way of processing complex emotions and life transitions. Dreams have a remarkable ability to synthesize our experiences and present them in symbolic form, helping us understand deeper truths about our inner world and current life circumstances."""

    def _parse_insights_response(self, response: str) -> List[str]:
        """Parse insights from OpenAI response"""
        # Split by numbers and clean up
        insights = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove number prefix and clean
                cleaned = line.lstrip('0123456789.- ').strip()
                if cleaned:
                    insights.append(cleaned)
        
        return insights[:5]  # Limit to 5 insights

    def _get_mock_psychological_insights(self) -> List[str]:
        """Mock psychological insights for when OpenAI is not available"""
        return [
            "This dream suggests you're processing feelings of transformation in your current life situation.",
            "The symbolic elements indicate a desire for greater freedom and new perspectives on existing challenges.",
            "Your subconscious appears to be working through themes of personal growth and emotional development.",
            "The dream imagery reflects inner conflicts between security and the need for positive change.",
            "These symbols often appear when the psyche is preparing for important life transitions."
        ]

    def _get_mock_interpretation(self) -> str:
        """Mock comprehensive interpretation"""
        return """This dream appears to reflect a significant period of personal transformation and growth in your life. The symbolic elements present in your dream suggest that your unconscious mind is actively processing the balance between maintaining stability and embracing new opportunities for expansion. The interplay of these powerful symbols indicates that you're currently navigating a meaningful transition where personal development requires releasing outdated patterns and beliefs.

The emotional landscape of your dream reveals that while uncertainty can feel challenging, your deeper wisdom is actually preparing you for positive developments ahead. This dream seems to be encouraging you to trust in your innate ability to handle life's transitions and to remain open to the growth opportunities that are emerging in your path forward."""

    def _get_mock_conversational_response(self, user_question: str) -> str:
        """Mock conversational response"""
        responses = [
            "That's an insightful question about your dream symbolism. The elements you're asking about often represent the psyche's way of processing important life themes and emotional development.",
            "Your question touches on a fascinating aspect of dream interpretation. This particular symbol frequently appears when we're working through significant personal growth and transformation.",
            "I'm glad you asked about that detail. In dream analysis, this type of imagery typically reflects your unconscious mind's efforts to integrate new understandings about yourself and your life situation.",
            "That's a thoughtful observation about your dream. These symbolic elements often emerge when we're ready to embrace positive changes and new perspectives in our waking life."
        ]
        
        # Simple selection based on question content
        if any(word in user_question.lower() for word in ['symbol', 'meaning', 'represent']):
            return responses[0]
        elif any(word in user_question.lower() for word in ['why', 'how', 'what']):
            return responses[1]
        else:
            return responses[2]