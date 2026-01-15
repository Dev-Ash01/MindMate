from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import pipeline
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = FastAPI(
    title="MindMate AI",
    version="1.0.0",
    description="Mental wellness chatbot with sentiment analysis"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy-load model
sentiment_model = None
crisis_keywords = [
    "suicide", "hurt myself", "kill myself", "die", "overdose",
    "self harm", "cut myself", "depressed", "hopeless", "worthless"
]

def load_sentiment_model():
    """Load DistilBERT only on first request."""
    global sentiment_model
    if sentiment_model is None:
        logger.info("Loading DistilBERT model (first request)...")
        try:
            sentiment_model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1,  # CPU only (Render has no GPU)
                torch_dtype=torch.float16,  # Half precision: 50% less memory
                model_kwargs={"low_cpu_mem_usage": True}  # Further optimization
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Model load failed: {e}")
            raise
    return sentiment_model

# Request models
class TextRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    is_crisis: bool

# Health check (no model needed)
@app.get("/health")
async def health_check():
    """Lightweight health check for Render."""
    return {
        "status": "healthy",
        "nlp_model": "distilbert-base-uncased-finetuned-sst-2-english",
        "llm_provider": "huggingface-api",
        "memory_optimized": True
    }

# Root endpoint
@app.get("/")
async def root():
    """Welcome message."""
    return {
        "name": "MindMate",
        "message": "AI Mental Wellness Chatbot",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze",
            "docs": "/docs"
        }
    }

# Sentiment analysis endpoint
@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: TextRequest):
    """
    Analyze sentiment of user text.
    
    Args:
        text: User input text
    
    Returns:
        sentiment: POSITIVE or NEGATIVE
        confidence: 0.0-1.0 confidence score
        is_crisis: True if crisis keywords detected
    """
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    text_lower = request.text.lower()
    
    # Check for crisis indicators (instant, no model needed)
    is_crisis = any(keyword in text_lower for keyword in crisis_keywords)
    
    # Load model on first request
    model = load_sentiment_model()
    
    # Truncate long texts to save memory
    text_to_analyze = request.text[:512]
    
    try:
        result = model(text_to_analyze)[0]
        return SentimentResponse(
            text=request.text,
            sentiment=result["label"].upper(),
            confidence=float(result["score"]),
            is_crisis=is_crisis
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        # Fallback if model unavailable
        return SentimentResponse(
            text=request.text,
            sentiment="NEUTRAL",
            confidence=0.5,
            is_crisis=is_crisis
        )

# Crisis response endpoint
@app.get("/crisis-resources")
async def get_crisis_resources():
    """Return crisis support resources if needed."""
    return {
        "crisis_detected": True,
        "resources": {
            "national_suicide_prevention": "1-800-273-8255",
            "crisis_text_line": "Text HOME to 741741",
            "international_association": "https://www.iasp.info/resources/Crisis_Centres/",
            "mindmate_support": "Talk to a professional immediately"
        }
    }

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all exceptions gracefully."""
    logger.error(f"Error: {exc}")
    return {
        "error": "Internal server error",
        "status": 500
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
