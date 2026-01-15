# Response Generator Module
# Generates empathetic, emotionally-aware responses using LLM

import logging
import requests
import os
from typing import Optional

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """
    Generates emotionally aware responses using HuggingFace Inference API or local LLM
    
    Configuration via environment variables:
    - LLM_PROVIDER: "huggingface-api" or "ollama"
    - HF_API_KEY: HuggingFace API token (for HF provider)
    - OLLAMA_URL: Ollama server URL (for local provider, default: http://localhost:11434)
    """
    
    def __init__(self):
        """Initialize response generator with configured LLM provider"""
        self.provider = os.getenv("LLM_PROVIDER", "huggingface-api")
        
        if self.provider == "huggingface-api":
            self.api_key = os.getenv("HF_API_KEY")
            if not self.api_key:
                logger.warning("HF_API_KEY not set. Using fallback response mode.")
            self.model_id = "meta-llama/Llama-2-7b-chat-hf"  # Free, requires API key
            self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        
        elif self.provider == "ollama":
            self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            self.model_name = os.getenv("OLLAMA_MODEL", "mistral")
            logger.info(f"Using Ollama provider: {self.ollama_url}/api/generate")
        
        else:
            logger.warning(f"Unknown provider: {self.provider}. Using fallback mode.")
            self.provider = "fallback"
    
    def generate_response(self, user_message: str, sentiment: str, context: str) -> str:
        """
        Generate empathetic response based on user message and sentiment
        
        Args:
            user_message: Original user message
            sentiment: Detected sentiment (POSITIVE/NEGATIVE)
            context: Conversation context for continuity
        
        Returns:
            Generated response string
        """
        try:
            # Build system prompt for emotional awareness
            system_prompt = self._build_system_prompt(sentiment)
            
            # Build user prompt with context
            user_prompt = self._build_user_prompt(user_message, context)
            
            # Generate response based on provider
            if self.provider == "huggingface-api" and self.api_key:
                response = self._generate_with_huggingface(system_prompt, user_prompt)
            
            elif self.provider == "ollama":
                response = self._generate_with_ollama(system_prompt, user_prompt)
            
            else:
                # Fallback mode when no LLM is available
                response = self._generate_fallback_response(user_message, sentiment)
            
            return response
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._generate_fallback_response(user_message, sentiment)
    
    def _build_system_prompt(self, sentiment: str) -> str:
        """
        Build system prompt that guides LLM behavior
        
        Args:
            sentiment: Current sentiment (POSITIVE/NEGATIVE)
        
        Returns:
            System prompt with safety and empathy guidelines
        """
        base_prompt = """You are a compassionate, empathetic mental wellness support chatbot.
Your role is to provide emotional support and encourage healthy coping strategies.

IMPORTANT GUIDELINES:
1. Always be warm, non-judgmental, and supportive
2. Validate the person's feelings and experiences
3. Ask thoughtful follow-up questions to show you understand
4. Suggest healthy coping strategies (journaling, exercise, breathing exercises, etc.)
5. Encourage professional help when appropriate
6. NEVER provide medical advice, diagnosis, or prescriptions
7. NEVER pretend to be a licensed therapist or psychiatrist
8. Keep responses concise and natural (2-4 sentences)
9. Use simple, clear language
10. If user is in crisis, immediately redirect to professional help

Remember: You are NOT a mental health professional. You provide general wellness support only."""
        
        # Adjust tone based on sentiment
        if sentiment == "NEGATIVE":
            base_prompt += "\n\nThe user is expressing negative emotions. Show extra empathy and validation."
        else:
            base_prompt += "\n\nThe user seems to be in a better emotional state. Encourage positive momentum."
        
        return base_prompt
    
    def _build_user_prompt(self, user_message: str, context: str) -> str:
        """
        Build user prompt with context
        
        Args:
            user_message: Current user message
            context: Conversation history
        
        Returns:
            Formatted user prompt
        """
        prompt = f"""{context}

Please respond warmly and supportively to the user's message. Remember to stay within your role as a wellness chatbot."""
        return prompt
    
    def _generate_with_huggingface(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate response using HuggingFace Inference API
        
        Requires HF_API_KEY environment variable
        Uses Llama-2-7b-chat model (free tier, rate limited)
        """
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            # Format as conversation for chat model
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            payload = {
                "inputs": self._format_for_llama2(system_prompt, user_prompt),
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                # Extract generated text
                if isinstance(result, list) and len(result) > 0:
                    generated = result[0].get("generated_text", "")
                    # Clean up response (remove prompt echo)
                    response_text = generated.split("Assistant:")[-1].strip()
                    return response_text[:300]  # Limit response length
            
            else:
                logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
                return self._generate_fallback_response("", "NEGATIVE")
        
        except Exception as e:
            logger.error(f"HuggingFace API request failed: {e}")
            return self._generate_fallback_response("", "NEGATIVE")
    
    def _generate_with_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate response using local Ollama instance
        
        Requires Ollama to be running and model to be pulled
        Free and private - no API key needed
        """
        try:
            # Build the prompt for Ollama
            full_prompt = f"{system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
            
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "temperature": 0.7,
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()
                return response_text[:300]  # Limit response length
            
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return self._generate_fallback_response("", "NEGATIVE")
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Cannot connect to Ollama at {self.ollama_url}")
            return self._generate_fallback_response("", "NEGATIVE")
        
        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            return self._generate_fallback_response("", "NEGATIVE")
    
    def _generate_fallback_response(self, user_message: str, sentiment: str) -> str:
        """
        Generate a template-based response when LLM is unavailable
        
        This ensures the chatbot always has a meaningful response
        even without API access or local model
        """
        fallback_responses = {
            "NEGATIVE": [
                "I hear that you're going through a difficult time. It's okay to feel this way, and I'm here to listen. What's been the most challenging part for you?",
                "Thank you for sharing that with me. Those feelings are valid, and many people experience what you're going through. Have you tried any coping strategies that have helped before?",
                "I can sense you're struggling right now. That takes courage to express. Remember that difficult feelings are temporary, even when they feel overwhelming.",
                "It sounds like you're dealing with a lot. While I can't provide medical advice, I encourage you to consider talking with a counselor or therapist who can offer professional support.",
                "I appreciate you opening up about this. Sometimes just acknowledging what we're feeling is an important first step. What would help you feel a little better right now?"
            ],
            "POSITIVE": [
                "That sounds wonderful! It's great to hear positive energy from you. What's been contributing to this good feeling?",
                "I'm glad to hear that! Celebrating these moments is important. How are you planning to maintain this positive momentum?",
                "That's fantastic! Keep nurturing what's bringing you joy. What's one thing you appreciate about yourself right now?",
                "Your positive outlook is inspiring! Keep channeling that energy into things that matter to you.",
                "That's excellent! It sounds like things are moving in a good direction for you. What's helping you feel this way?"
            ]
        }
        
        import random
        responses = fallback_responses.get(sentiment, fallback_responses["POSITIVE"])
        return random.choice(responses)
    
    def _format_for_llama2(self, system_prompt: str, user_prompt: str) -> str:
        """
        Format prompts for Llama-2-chat model
        Llama-2 expects specific formatting for chat
        """
        return f"""[INST] <<SYS>>
{system_prompt}
<</SYS>>

{user_prompt}
[/INST]"""
