"""
STEP 2.1: Case Fetcher Module
Fetches case data from the mock database.
Enterprise systems process single cases for accountability.
"""

import json
import os
from typing import Dict, List, Optional

class CaseFetcher:
    """Handles fetching case data from the database."""
    
    def __init__(self, db_path: str = None):
        """Initialize with database path."""
        if db_path is None:
            # Default path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "..", "database", "cases.json")
        self.db_path = db_path
        self._load_database()
    
    def _load_database(self) -> None:
        """Load the JSON database into memory."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.cases = json.load(f)
            print(f"✅ Database loaded: {len(self.cases)} cases found")
        except FileNotFoundError:
            print(f"❌ Database not found at {self.db_path}")
            self.cases = []
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in database file")
            self.cases = []
    
    def get_all_cases(self) -> List[Dict]:
        """Return all cases from the database."""
        return self.cases
    
    def get_case_by_id(self, case_id: str) -> Optional[Dict]:
        """
        Fetch a single case by its ID.
        This is the primary method for single-case processing.
        """
        for case in self.cases:
            if case.get("case_id") == case_id:
                return case
        return None
    
    def get_case_ids(self) -> List[str]:
        """Return list of all case IDs for dropdown/selection."""
        return [case.get("case_id") for case in self.cases]
    
    def get_case_summary(self, case_id: str) -> str:
        """Get a formatted summary of a case for display."""
        case = self.get_case_by_id(case_id)
        if case:
            return f"{case['case_id']} - {case['customer_name']} (₹{case['amount']:,})"
        return "Case not found"


# Quick test
if __name__ == "__main__":
    fetcher = CaseFetcher()
    print("\n📋 All Case IDs:")
    for cid in fetcher.get_case_ids():
        print(f"  - {fetcher.get_case_summary(cid)}")
    
    print("\n🔍 Fetching CASE003:")
    case = fetcher.get_case_by_id("CASE003")
    if case:
        for key, value in case.items():
            print(f"  {key}: {value}")
