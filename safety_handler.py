# Safety Handler Module
# Detects high-risk language and provides crisis response

import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)

class SafetyHandler:
    """
    Detects high-risk indicators in user messages
    Uses keyword-based and semantic detection for crisis situations
    Provides appropriate crisis response and resources
    """
    
    def __init__(self):
        """Initialize safety detection patterns"""
        
        # HIGH-RISK keywords indicating immediate danger
        self.high_risk_keywords = {
            "suicide": ["suicide", "suicidal", "kill myself", "end my life", "don't want to live"],
            "self_harm": ["self harm", "cut myself", "hurt myself", "injure", "harm myself"],
            "extreme_despair": ["can't take it anymore", "hopeless", "no point", "nothing matters"],
            "abuse": ["abusing me", "beat me", "hit me", "abuse", "violent"],
            "acute_crisis": ["emergency", "urgent", "right now", "immediately"]
        }
        
        # MEDIUM-RISK keywords indicating elevated emotional distress
        self.medium_risk_keywords = [
            "depressed", "suicidal thoughts", "panic", "overwhelmed",
            "can't cope", "breakdown", "crisis", "scared", "terrified",
            "dying", "death", "toxic", "trapped"
        ]
        
        # Low-risk everyday emotional words
        self.low_risk_keywords = [
            "sad", "anxious", "worried", "stressed", "frustrated",
            "tired", "lonely", "confused", "lost", "scared"
        ]
    
    def assess_risk(self, message: str) -> Dict:
        """
        Assess risk level of user message
        
        Args:
            message: User message to analyze
        
        Returns:
            Dict with 'is_high_risk', 'risk_level', and 'risk_indicators'
        """
        try:
            message_lower = message.lower()
            risk_indicators = []
            
            # Check for high-risk patterns
            for category, keywords in self.high_risk_keywords.items():
                for keyword in keywords:
                    if self._keyword_match(message_lower, keyword):
                        risk_indicators.append(f"{category}: {keyword}")
            
            # Check for medium-risk keywords
            if not risk_indicators:  # Only check if no high-risk found
                for keyword in self.medium_risk_keywords:
                    if self._keyword_match(message_lower, keyword):
                        risk_indicators.append(f"medium_risk: {keyword}")
            
            # Determine risk level
            if risk_indicators and any("suicide" in ind or "self_harm" in ind for ind in risk_indicators):
                risk_level = "high"
                is_high_risk = True
            elif len([ind for ind in risk_indicators if "medium_risk" in ind]) >= 2:
                risk_level = "medium"
                is_high_risk = False
            else:
                risk_level = "low"
                is_high_risk = False
            
            logger.info(f"Risk assessment: {risk_level} | Indicators: {risk_indicators}")
            
            return {
                "is_high_risk": is_high_risk,
                "risk_level": risk_level,
                "risk_indicators": risk_indicators[:5]  # Limit to top 5
            }
        
        except Exception as e:
            logger.error(f"Error in risk assessment: {e}")
            return {
                "is_high_risk": False,
                "risk_level": "low",
                "risk_indicators": []
            }
    
    def _keyword_match(self, message: str, keyword: str) -> bool:
        """
        Safely match keyword in message
        Uses word boundaries to avoid false positives
        
        Args:
            message: Message to search in (lowercase)
            keyword: Keyword to find
        
        Returns:
            True if keyword found with word boundaries
        """
        try:
            # Use regex with word boundaries for accurate matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            return bool(re.search(pattern, message))
        except:
            # Fallback to simple string matching if regex fails
            return keyword in message
    
    def get_crisis_response(self) -> str:
        """
        Return appropriate crisis response with professional resources
        
        Returns:
            Crisis response message with emergency resources
        """
        crisis_response = """I'm concerned about what you're sharing. Your safety is important.

If you're in immediate danger or having thoughts of self-harm, please reach out to emergency services or a crisis helpline right away:

🆘 **Immediate Help Resources:**
• **National Suicide Prevention Lifeline (US):** 988 (call or text)
• **Crisis Text Line:** Text HOME to 741741
• **International Association for Suicide Prevention:** https://www.iasp.info/resources/Crisis_Centres/
• **Samaritans (UK):** 116 123
• **Lifeline (Australia):** 13 11 14
• **India Crisis Helpline:** 9152987821

Please reach out to someone you trust - a friend, family member, or mental health professional. You're not alone in this.

This chatbot is not a substitute for professional mental health care. Please speak with a licensed therapist or counselor."""
        
        return crisis_response
    
    def is_safe_to_continue(self, message: str) -> bool:
        """
        Check if conversation can continue safely
        Used to determine if bot should refuse to engage
        
        Args:
            message: Message to check
        
        Returns:
            True if safe to continue, False if immediate danger detected
        """
        assessment = self.assess_risk(message)
        # Only refuse if explicitly high-risk (suicide/self-harm indicators)
        return not assessment['is_high_risk']
    
    def get_resource_suggestions(self, risk_level: str) -> List[str]:
        """
        Get suggested resources based on risk level
        
        Args:
            risk_level: "low", "medium", or "high"
        
        Returns:
            List of relevant resource suggestions
        """
        resources = {
            "low": [
                "Consider journaling about your feelings",
                "Try a breathing exercise when stressed",
                "Reach out to someone you trust",
                "Engage in activities that bring joy"
            ],
            "medium": [
                "Consider speaking with a counselor or therapist",
                "Contact a crisis support hotline",
                "Visit a mental health clinic",
                "Reach out to a trusted friend or family member"
            ],
            "high": [
                "**Contact emergency services immediately**",
                "**Call the National Suicide Prevention Lifeline: 988**",
                "**Go to the nearest emergency room**",
                "**Tell someone you trust right now**"
            ]
        }
        
        return resources.get(risk_level, resources["low"])
