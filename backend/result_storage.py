"""
STEP 4: Result Storage Module
Stores AI decisions for audit and explainability.
Enterprise requirement: Decision traceability & governance.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class ResultStorage:
    """
    Stores risk classification results for audit purposes.
    Enables: Explainability & Governance
    """
    
    def __init__(self, storage_path: str = None):
        """Initialize storage with file path."""
        if storage_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            storage_path = os.path.join(current_dir, "..", "results", "decisions.json")
        
        self.storage_path = storage_path
        self._ensure_storage_exists()
        self._load_results()
    
    def _ensure_storage_exists(self) -> None:
        """Create storage directory and file if not exists."""
        storage_dir = os.path.dirname(self.storage_path)
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def _load_results(self) -> None:
        """Load existing results from storage."""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                self.results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.results = []
    
    def _save_results(self) -> None:
        """Save results to storage file."""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
    
    def store_decision(self, case_id: str, customer_name: str, 
                       raw_case_data: Dict, classification_result: Dict) -> Dict:
        """
        Store a risk classification decision.
        
        Args:
            case_id: Unique case identifier
            customer_name: Customer name for reference
            raw_case_data: Original case data
            classification_result: Gemini's classification output
            
        Returns:
            The stored decision record
        """
        decision_record = {
            "decision_id": f"DEC{len(self.results) + 1:05d}",
            "case_id": case_id,
            "customer_name": customer_name,
            "timestamp": datetime.now().isoformat(),
            "input_data": {
                "amount": raw_case_data.get("amount"),
                "days_overdue": raw_case_data.get("days_overdue"),
                "past_attempts": raw_case_data.get("past_attempts"),
                "customer_type": raw_case_data.get("customer_type"),
                "loan_type": raw_case_data.get("loan_type")
            },
            "ai_decision": {
                "risk_level": classification_result.get("risk_level"),
                "confidence": classification_result.get("confidence"),
                "reason": classification_result.get("reason"),
                "recommended_action": classification_result.get("recommended_action")
            },
            "status": "pending_review"  # For audit workflow
        }
        
        self.results.append(decision_record)
        self._save_results()
        
        return decision_record
    
    def get_all_decisions(self) -> List[Dict]:
        """Return all stored decisions."""
        return self.results
    
    def get_decision_by_case(self, case_id: str) -> List[Dict]:
        """Get all decisions for a specific case."""
        return [d for d in self.results if d.get("case_id") == case_id]
    
    def get_latest_decision(self, case_id: str) -> Optional[Dict]:
        """Get the most recent decision for a case."""
        case_decisions = self.get_decision_by_case(case_id)
        if case_decisions:
            return case_decisions[-1]
        return None
    
    def get_decisions_by_risk(self, risk_level: str) -> List[Dict]:
        """Get all decisions of a specific risk level."""
        return [
            d for d in self.results 
            if d.get("ai_decision", {}).get("risk_level") == risk_level
        ]
    
    def get_statistics(self) -> Dict:
        """Get summary statistics of all decisions."""
        total = len(self.results)
        if total == 0:
            return {"total": 0, "high": 0, "medium": 0, "low": 0}
        
        high = len(self.get_decisions_by_risk("HIGH"))
        medium = len(self.get_decisions_by_risk("MEDIUM"))
        low = len(self.get_decisions_by_risk("LOW"))
        
        return {
            "total": total,
            "high": high,
            "medium": medium,
            "low": low,
            "high_percentage": round(high/total * 100, 1),
            "medium_percentage": round(medium/total * 100, 1),
            "low_percentage": round(low/total * 100, 1)
        }
    
    def clear_all(self) -> None:
        """Clear all stored decisions (use with caution)."""
        self.results = []
        self._save_results()


# Quick test
if __name__ == "__main__":
    storage = ResultStorage()
    
    # Test storing a decision
    test_case = {
        "amount": 500000,
        "days_overdue": 120,
        "past_attempts": 8,
        "customer_type": "Business",
        "loan_type": "Business Loan"
    }
    
    test_result = {
        "risk_level": "HIGH",
        "confidence": 0.92,
        "reason": "High amount with extended overdue period and multiple failed attempts.",
        "recommended_action": "Escalate to legal team."
    }
    
    record = storage.store_decision(
        case_id="CASE003",
        customer_name="ABC Enterprises",
        raw_case_data=test_case,
        classification_result=test_result
    )
    
    print("✅ Stored Decision:")
    print(json.dumps(record, indent=2))
    
    print("\n📊 Statistics:")
    print(json.dumps(storage.get_statistics(), indent=2))
