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
        "nlp_model": "distilbert-base-uncas
