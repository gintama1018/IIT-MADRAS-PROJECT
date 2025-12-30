"""
STEP 2.3: Gemini API Client
LLM-based decision modeling for risk classification.
We use Gemini because we lack labeled historical data for traditional ML.
"""

import google.generativeai as genai
from typing import Dict, Optional
import json
import re

class GeminiRiskClassifier:
    """
    Gemini AI client for risk classification.
    
    Important: Gemini doesn't access the database directly.
    It only performs REASONING on the context we provide.
    """
    
    def __init__(self, api_key: str):
        """Initialize Gemini with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Use Gemini 1.5 Flash for faster responses
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System prompt for consistent output
        self.system_prompt = """
You are an AI Risk Assessment Agent for a debt collection enterprise.
Your job is to classify overdue debt cases into risk categories and predict recovery probability.

RISK CATEGORIES:
1. LOW RISK - Customer likely to pay, minor delays, low amount
2. MEDIUM RISK - Needs attention, moderate delays/amounts, some recovery attempts failed
3. HIGH RISK - Serious concern, long overdue, high amounts, multiple failed attempts

RECOVERY PROBABILITY:
Based on case factors, estimate the likelihood of successful debt recovery:
- VERY HIGH (>80%): New overdue, cooperative customer, small amount
- HIGH (60-80%): Moderate overdue, some attempts, willing to negotiate
- MODERATE (40-60%): Longer overdue, multiple attempts, uncertain outcome
- LOW (20-40%): Severely overdue, many failed attempts, unresponsive
- VERY LOW (<20%): Written-off candidate, legal action needed

OUTPUT FORMAT (JSON only, no markdown):
{
    "risk_level": "LOW" or "MEDIUM" or "HIGH",
    "confidence": 0.0 to 1.0,
    "recovery_probability": "VERY HIGH" or "HIGH" or "MODERATE" or "LOW" or "VERY LOW",
    "recovery_percentage": 0 to 100,
    "reason": "2-3 sentence explanation",
    "recommended_action": "Suggested next step for recovery team"
}

IMPORTANT:
- Be objective and base decisions on the provided context
- Consider all factors: amount, overdue duration, past attempts, customer type
- Provide actionable recommendations
- Output ONLY valid JSON, no other text
- Do not include any text outside the JSON response.
"""
    
    def classify_risk(self, case_context: str) -> Optional[Dict]:
        """
        Send case context to Gemini and get risk classification.
        
        Args:
            case_context: Pre-processed context string from preprocessor
            
        Returns:
            Dict with risk_level, confidence, reason, recommended_action
        """
        try:
            # Construct the full prompt
            full_prompt = f"""
{self.system_prompt}

{case_context}

Analyze this case and provide risk classification in JSON format.
"""
            
            # Make API call to Gemini
            response = self.model.generate_content(full_prompt)
            
            # Parse the response
            result = self._parse_response(response.text)
            return result
            
        except Exception as e:
            print(f"❌ Gemini API Error: {str(e)}")
            return {
                "risk_level": "ERROR",
                "confidence": 0.0,
                "reason": f"API Error: {str(e)}",
                "recommended_action": "Manual review required"
            }
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse Gemini's response into structured format."""
        try:
            # Clean response - remove markdown code blocks if present
            cleaned = response_text.strip()
            
            # Remove ```json and ``` markers
            cleaned = re.sub(r'^```json\s*', '', cleaned)
            cleaned = re.sub(r'^```\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)
            cleaned = cleaned.strip()
            
            # Parse JSON
            result = json.loads(cleaned)
            
            # Validate required fields
            required_fields = ["risk_level", "reason"]
            for field in required_fields:
                if field not in result:
                    result[field] = "Unknown" if field == "risk_level" else "No explanation provided"
            
            # Ensure confidence is present
            if "confidence" not in result:
                result["confidence"] = 0.8  # Default confidence
            
            # Ensure recommended_action is present
            if "recommended_action" not in result:
                result["recommended_action"] = "Follow standard recovery procedure"
            
            # Ensure recovery prediction fields are present
            if "recovery_probability" not in result:
                # Infer from risk level
                risk = result.get("risk_level", "MEDIUM").upper()
                result["recovery_probability"] = "HIGH" if risk == "LOW" else "MODERATE" if risk == "MEDIUM" else "LOW"
            
            if "recovery_percentage" not in result:
                prob_map = {"VERY HIGH": 85, "HIGH": 70, "MODERATE": 50, "LOW": 30, "VERY LOW": 15}
                result["recovery_percentage"] = prob_map.get(result.get("recovery_probability", "MODERATE"), 50)
            
            return result
            
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract key information
            return {
                "risk_level": self._extract_risk_level(response_text),
                "confidence": 0.7,
                "reason": response_text[:200] if len(response_text) > 200 else response_text,
                "recommended_action": "Manual review recommended"
            }
    
    def _extract_risk_level(self, text: str) -> str:
        """Try to extract risk level from unstructured text."""
        text_upper = text.upper()
        if "HIGH RISK" in text_upper or "HIGH" in text_upper:
            return "HIGH"
        elif "MEDIUM RISK" in text_upper or "MEDIUM" in text_upper:
            return "MEDIUM"
        elif "LOW RISK" in text_upper or "LOW" in text_upper:
            return "LOW"
        return "UNKNOWN"


# Demo mode for testing without API key
class DemoGeminiClassifier:
    """Demo classifier for testing without Gemini API."""
    
    def classify_risk(self, case_context: str) -> Dict:
        """Rule-based demo classification."""
        # Simple rule-based logic for demo
        context_lower = case_context.lower()
        
        # High risk indicators
        high_risk_indicators = [
            "critically overdue",
            "exhaustive recovery attempts",
            "very high amount",
            "immediate action required"
        ]
        
        # Low risk indicators
        low_risk_indicators = [
            "recently overdue",
            "no recovery attempts",
            "low amount",
            "within grace period"
        ]
        
        high_score = sum(1 for ind in high_risk_indicators if ind in context_lower)
        low_score = sum(1 for ind in low_risk_indicators if ind in context_lower)
        
        if high_score >= 2:
            return {
                "risk_level": "HIGH",
                "confidence": 0.85,
                "recovery_probability": "LOW",
                "recovery_percentage": 30,
                "reason": "Case shows multiple high-risk indicators including long overdue duration and multiple failed recovery attempts.",
                "recommended_action": "Escalate to legal team for formal notice. Consider asset recovery if secured loan."
            }
        elif low_score >= 2:
            return {
                "risk_level": "LOW",
                "confidence": 0.90,
                "recovery_probability": "VERY HIGH",
                "recovery_percentage": 85,
                "reason": "Case is recently overdue with low amount. Customer likely to pay with gentle reminder.",
                "recommended_action": "Send automated payment reminder. Schedule follow-up call in 3 days."
            }
        else:
            return {
                "risk_level": "MEDIUM",
                "confidence": 0.75,
                "recovery_probability": "MODERATE",
                "recovery_percentage": 55,
                "reason": "Case shows mixed indicators. Moderate attention required with proactive follow-up.",
                "recommended_action": "Assign to recovery agent for personal follow-up. Offer payment plan options."
            }


# Quick test
if __name__ == "__main__":
    # Test with demo classifier
    demo_classifier = DemoGeminiClassifier()
    
    test_context = """
    CASE DETAILS FOR RISK ASSESSMENT:
    Case ID: CASE003
    Customer: ABC Enterprises
    Amount: Very high amount (₹5,00,000)
    Duration: Critically overdue (120 days)
    Past Attempts: Exhaustive recovery attempts failed (8 attempts)
    """
    
    print("🤖 Testing Demo Classifier:")
    result = demo_classifier.classify_risk(test_context)
    print(json.dumps(result, indent=2))
