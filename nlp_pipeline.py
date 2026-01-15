# NLP Pipeline Module
# Handles sentiment analysis using pretrained transformer models

import logging
from transformers import pipeline
from typing import Dict

logger = logging.getLogger(__name__)

class NLPPipeline:
    """
    NLP Pipeline for sentiment and emotion analysis
    Uses HuggingFace transformers with DistilBERT for efficiency
    """
    
    def __init__(self):
        """
        Initialize sentiment analysis model
        DistilBERT is lightweight (~67M parameters) and fast
        Pre-trained on SST-2 (Stanford Sentiment Treebank)
        """
        try:
            # Load sentiment analysis pipeline
            # This model classifies text as POSITIVE or NEGATIVE
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # Use CPU (-1) or GPU (0) based on availability
            )
            logger.info("Sentiment analyzer loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentiment analyzer: {e}")
            raise
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of input text
        
        Args:
            text: User message to analyze
        
        Returns:
            Dict with 'label' (POSITIVE/NEGATIVE) and 'score' (0-1 confidence)
        """
        try:
            if not text or len(text.strip()) == 0:
                return {"label": "NEUTRAL", "score": 0.5}
            
            # Truncate to 512 tokens (BERT limit)
            truncated_text = text[:512]
            
            # Run sentiment analysis
            result = self.sentiment_analyzer(truncated_text)
            
            # Extract label and score
            label = result[0]['label']  # POSITIVE or NEGATIVE
            score = result[0]['score']  # Confidence score
            
            logger.debug(f"Sentiment analysis: {label} ({score:.3f})")
            
            return {
                "label": label,
                "score": score
            }
        
        except Exception as e:
            logger.error(f"Error during sentiment analysis: {e}")
            # Return neutral sentiment on error
            return {"label": "NEUTRAL", "score": 0.5}
    
    def get_emotion_insights(self, sentiment: str, score: float) -> str:
        """
        Convert sentiment label to human-readable emotion insights
        Used for generating contextual responses
        
        Args:
            sentiment: POSITIVE or NEGATIVE
            score: Confidence score (0-1)
        
        Returns:
            Description of detected emotion
        """
        if sentiment == "NEGATIVE":
            if score > 0.9:
                return "User expressing strong negative emotions (distress, sadness, frustration)"
            else:
                return "User expressing negative emotions"
        else:
            if score > 0.9:
                return "User expressing positive emotions (optimism, contentment)"
            else:
                return "User expressing mixed or neutral emotions"
