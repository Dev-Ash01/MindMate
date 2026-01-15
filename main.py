# Mental Wellness Chatbot - Backend
# Main FastAPI application
# This is the core backend for the AI-powered mental wellness chatbot

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Import custom modules
from nlp_pipeline import NLPPipeline
from response_generator import ResponseGenerator
from safety_handler import SafetyHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mental Wellness Chatbot API",
    description="AI-powered empathetic chatbot for mental wellness support",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NLP components
try:
    nlp_pipeline = NLPPipeline()
    logger.info("NLP pipeline initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize NLP pipeline: {e}")
    raise

response_generator = ResponseGenerator()
safety_handler = SafetyHandler()

# ==================== Pydantic Models ====================

class Message(BaseModel):
    """Single message in conversation history"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None
    sentiment: Optional[str] = None

class ChatRequest(BaseModel):
    """Request body for chat endpoint"""
    message: str
    conversation_history: Optional[List[Message]] = []

class SentimentAnalysis(BaseModel):
    """Sentiment analysis result"""
    label: str
    score: float

class RiskAssessment(BaseModel):
    """Risk assessment result"""
    is_high_risk: bool
    risk_level: str  # "low", "medium", "high"
    risk_indicators: List[str]

class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    user_message: str
    sentiment: SentimentAnalysis
    is_high_risk: bool
    risk_level: str
    bot_response: str
    conversation_summary: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    nlp_model: str
    llm_provider: str

# ==================== API Endpoints ====================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify all services are running
    Returns status of NLP models and LLM provider
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        nlp_model="distilbert-base-uncased-finetuned-sst-2-english",
        llm_provider=os.getenv("LLM_PROVIDER", "huggingface-api")
    )

@app.get("/config")
async def get_config():
    """
    Get current configuration (non-sensitive)
    Useful for frontend to understand system capabilities
    """
    return {
        "max_conversation_history": 20,
        "sentiment_model": "distilbert-base-uncased-finetuned-sst-2-english",
        "emotion_labels": ["NEGATIVE", "POSITIVE"],
        "risk_detection_enabled": True,
        "disclaimer": "This chatbot provides non-clinical mental wellness support. It is not a substitute for professional medical advice."
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    - Analyzes sentiment of user message
    - Detects high-risk language
    - Generates empathetic response
    - Returns complete analysis and response
    """
    try:
        user_message = request.message.strip()
        
        # Validate input
        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if len(user_message) > 5000:
            raise HTTPException(status_code=400, detail="Message too long (max 5000 characters)")
        
        logger.info(f"Processing message: {user_message[:100]}...")
        
        # 1. Sentiment Analysis
        sentiment_result = nlp_pipeline.analyze_sentiment(user_message)
        logger.info(f"Sentiment: {sentiment_result['label']} (score: {sentiment_result['score']:.3f})")
        
        # 2. Risk Detection
        risk_result = safety_handler.assess_risk(user_message)
        logger.info(f"Risk Level: {risk_result['risk_level']} - High Risk: {risk_result['is_high_risk']}")
        
        # 3. Handle high-risk cases
        if risk_result['is_high_risk']:
            bot_response = safety_handler.get_crisis_response()
            logger.warning(f"High-risk message detected. Indicators: {risk_result['risk_indicators']}")
        else:
            # 4. Generate contextual response
            conversation_context = _format_conversation_context(
                request.conversation_history,
                user_message
            )
            bot_response = response_generator.generate_response(
                user_message=user_message,
                sentiment=sentiment_result['label'],
                context=conversation_context
            )
        
        # 5. Build response
        return ChatResponse(
            user_message=user_message,
            sentiment=SentimentAnalysis(
                label=sentiment_result['label'],
                score=sentiment_result['score']
            ),
            is_high_risk=risk_result['is_high_risk'],
            risk_level=risk_result['risk_level'],
            bot_response=bot_response,
            conversation_summary=_generate_summary(sentiment_result['label'])
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing your message"
        )

@app.post("/analyze-sentiment")
async def analyze_sentiment(request: ChatRequest):
    """
    Standalone sentiment analysis endpoint
    Useful for debugging or frontend preview
    """
    try:
        sentiment = nlp_pipeline.analyze_sentiment(request.message)
        return sentiment
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing sentiment")

@app.post("/assess-risk")
async def assess_risk(request: ChatRequest):
    """
    Standalone risk assessment endpoint
    Returns risk level and detected indicators
    """
    try:
        risk = safety_handler.assess_risk(request.message)
        return risk
    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        raise HTTPException(status_code=500, detail="Error assessing risk")

# ==================== Helper Functions ====================

def _format_conversation_context(conversation_history: List[Message], current_message: str) -> str:
    """
    Format conversation history for context-aware response generation
    Limits to last 10 messages to prevent token overflow
    """
    recent_history = conversation_history[-10:] if conversation_history else []
    
    context = "Recent conversation:\n"
    for msg in recent_history:
        role = "User" if msg.role == "user" else "Assistant"
        context += f"{role}: {msg.content}\n"
    
    context += f"Current user message: {current_message}"
    return context

def _generate_summary(sentiment: str) -> str:
    """
    Generate a brief summary of the conversation state
    Used for frontend display or logging
    """
    if sentiment == "NEGATIVE":
        return "User expressing difficult emotions - heightened empathy mode"
    else:
        return "Conversation flowing normally - supportive mode"

# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return {"error": exc.detail, "status_code": exc.status_code}

if __name__ == "__main__":
    import uvicorn
    # Run with: python main.py
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
