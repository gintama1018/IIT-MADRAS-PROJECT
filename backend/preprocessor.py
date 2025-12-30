"""
STEP 2.2: Pre-Processing Module (VERY IMPORTANT)
Converts raw numbers to decision-ready context for Gemini.
We normalize and summarize case attributes before reasoning.
"""

from typing import Dict

class CasePreprocessor:
    """
    Transforms raw case data into contextual descriptions.
    This is crucial - we give Gemini CONTEXT, not raw numbers.
    """
    
    def __init__(self):
        """Define thresholds for categorization."""
        # Amount thresholds (in INR)
        self.amount_thresholds = {
            'low': 20000,      # Below 20k = Low amount
            'medium': 100000,  # 20k-1L = Medium amount
            'high': 500000     # Above 1L = High amount, Above 5L = Very High
        }
        
        # Days overdue thresholds
        self.overdue_thresholds = {
            'recent': 15,      # 0-15 days = Recently overdue
            'moderate': 45,    # 15-45 days = Moderately overdue
            'long': 90,        # 45-90 days = Long overdue
            'critical': 180    # Above 90 days = Critically overdue
        }
        
        # Past attempts thresholds
        self.attempts_thresholds = {
            'none': 0,         # No attempts yet
            'few': 2,          # 1-2 attempts
            'multiple': 5,     # 3-5 attempts
            'exhaustive': 10   # Above 5 = Many failed attempts
        }
    
    def _categorize_amount(self, amount: float) -> str:
        """Convert amount to descriptive category."""
        if amount < self.amount_thresholds['low']:
            return "Low amount (below ₹20,000)"
        elif amount < self.amount_thresholds['medium']:
            return "Medium amount (₹20,000 - ₹1,00,000)"
        elif amount < self.amount_thresholds['high']:
            return "High amount (₹1,00,000 - ₹5,00,000)"
        else:
            return f"Very high amount (above ₹5,00,000 - specifically ₹{amount:,.0f})"
    
    def _categorize_overdue(self, days: int) -> str:
        """Convert days overdue to descriptive category."""
        if days <= self.overdue_thresholds['recent']:
            return f"Recently overdue ({days} days - within grace period)"
        elif days <= self.overdue_thresholds['moderate']:
            return f"Moderately overdue ({days} days - needs attention)"
        elif days <= self.overdue_thresholds['long']:
            return f"Long overdue ({days} days - serious concern)"
        else:
            return f"Critically overdue ({days} days - immediate action required)"
    
    def _categorize_attempts(self, attempts: int) -> str:
        """Convert past attempts to descriptive category."""
        if attempts == self.attempts_thresholds['none']:
            return "No recovery attempts made yet"
        elif attempts <= self.attempts_thresholds['few']:
            return f"Few recovery attempts ({attempts} attempts)"
        elif attempts <= self.attempts_thresholds['multiple']:
            return f"Multiple failed recovery attempts ({attempts} attempts)"
        else:
            return f"Exhaustive recovery attempts failed ({attempts} attempts - customer unresponsive)"
    
    def _categorize_customer_type(self, customer_type: str) -> str:
        """Add context about customer type."""
        if customer_type.lower() == "business":
            return "Business customer (higher stakes, formal recovery process needed)"
        else:
            return "Individual customer (personal approach may work)"
    
    def _categorize_loan_type(self, loan_type: str) -> str:
        """Add context about loan type and its implications."""
        loan_contexts = {
            "Credit Card": "Credit card debt (unsecured, typically smaller amounts)",
            "Personal Loan": "Personal loan (unsecured, medium priority)",
            "Home Loan": "Home loan (secured by property, high recovery priority)",
            "Vehicle Loan": "Vehicle loan (secured by vehicle, can be repossessed)",
            "Business Loan": "Business loan (complex recovery, may involve legal action)"
        }
        return loan_contexts.get(loan_type, f"{loan_type} (standard recovery process)")
    
    def preprocess(self, case: Dict) -> Dict:
        """
        Main preprocessing function.
        Transforms raw case data into decision-ready context.
        
        Returns:
            Dict with both raw data and contextual descriptions
        """
        if not case:
            return None
        
        # Create context summary for each field
        context = {
            "case_id": case.get("case_id"),
            "customer_name": case.get("customer_name"),
            
            # Raw values (for reference)
            "raw_amount": case.get("amount"),
            "raw_days_overdue": case.get("days_overdue"),
            "raw_past_attempts": case.get("past_attempts"),
            
            # Contextual descriptions (for Gemini)
            "amount_context": self._categorize_amount(case.get("amount", 0)),
            "overdue_context": self._categorize_overdue(case.get("days_overdue", 0)),
            "attempts_context": self._categorize_attempts(case.get("past_attempts", 0)),
            "customer_context": self._categorize_customer_type(case.get("customer_type", "Individual")),
            "loan_context": self._categorize_loan_type(case.get("loan_type", "Unknown"))
        }
        
        return context
    
    def generate_prompt_context(self, preprocessed_case: Dict) -> str:
        """
        Generate a formatted context string for Gemini prompt.
        This is what Gemini will actually read.
        """
        if not preprocessed_case:
            return ""
        
        context_str = f"""
CASE DETAILS FOR RISK ASSESSMENT:
==================================
Case ID: {preprocessed_case['case_id']}
Customer: {preprocessed_case['customer_name']}

FINANCIAL CONTEXT:
- Amount: {preprocessed_case['amount_context']}
- Loan Type: {preprocessed_case['loan_context']}

OVERDUE STATUS:
- Duration: {preprocessed_case['overdue_context']}

RECOVERY HISTORY:
- Past Attempts: {preprocessed_case['attempts_context']}

CUSTOMER PROFILE:
- Type: {preprocessed_case['customer_context']}
==================================
"""
        return context_str


# Quick test
if __name__ == "__main__":
    from case_fetcher import CaseFetcher
    
    fetcher = CaseFetcher()
    preprocessor = CasePreprocessor()
    
    # Test with a high-risk case
    print("🔄 Testing Preprocessor with CASE003 (High Risk Expected):")
    case = fetcher.get_case_by_id("CASE003")
    processed = preprocessor.preprocess(case)
    prompt_context = preprocessor.generate_prompt_context(processed)
    print(prompt_context)
    
    print("\n🔄 Testing Preprocessor with CASE004 (Low Risk Expected):")
    case = fetcher.get_case_by_id("CASE004")
    processed = preprocessor.preprocess(case)
    prompt_context = preprocessor.generate_prompt_context(processed)
    print(prompt_context)
