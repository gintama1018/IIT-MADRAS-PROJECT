"""
MAIN PIPELINE - The Brain of the System
Orchestrates the entire flow:
DB → Preprocessing → Gemini AI → Result Storage
"""

import os
from typing import Dict, Optional
from case_fetcher import CaseFetcher
from preprocessor import CasePreprocessor
from gemini_client import GeminiRiskClassifier, DemoGeminiClassifier
from result_storage import ResultStorage

class RiskClassificationPipeline:
    """
    Main pipeline that orchestrates the risk classification process.
    
    Flow:
    1. Fetch case from database
    2. Preprocess into contextual format
    3. Send to Gemini for classification
    4. Store results for audit
    """
    
    def __init__(self, gemini_api_key: str = None, use_demo: bool = False):
        """
        Initialize the pipeline with all components.
        
        Args:
            gemini_api_key: Your Gemini API key
            use_demo: If True, uses demo classifier (no API needed)
        """
        # Initialize all components
        self.fetcher = CaseFetcher()
        self.preprocessor = CasePreprocessor()
        self.storage = ResultStorage()
        
        # Initialize Gemini client
        if use_demo or not gemini_api_key:
            print("⚠️ Using Demo Mode (rule-based classification)")
            self.classifier = DemoGeminiClassifier()
            self.demo_mode = True
        else:
            print("✅ Using Gemini AI for classification")
            self.classifier = GeminiRiskClassifier(gemini_api_key)
            self.demo_mode = False
    
    def process_case(self, case_id: str, save_result: bool = True) -> Dict:
        """
        Process a single case through the entire pipeline.
        
        Args:
            case_id: The case ID to process
            save_result: Whether to save the result to storage
            
        Returns:
            Complete result with case data and classification
        """
        result = {
            "success": False,
            "case_id": case_id,
            "case_data": None,
            "processed_context": None,
            "classification": None,
            "decision_record": None,
            "error": None
        }
        
        try:
            # STEP 1: Fetch case from database
            print(f"\n📥 Step 1: Fetching case {case_id}...")
            case_data = self.fetcher.get_case_by_id(case_id)
            
            if not case_data:
                result["error"] = f"Case {case_id} not found in database"
                return result
            
            result["case_data"] = case_data
            print(f"   ✓ Found: {case_data['customer_name']} - ₹{case_data['amount']:,}")
            
            # STEP 2: Preprocess the case
            print(f"🔄 Step 2: Preprocessing case data...")
            processed = self.preprocessor.preprocess(case_data)
            context = self.preprocessor.generate_prompt_context(processed)
            result["processed_context"] = context
            print(f"   ✓ Context generated for AI")
            
            # STEP 3: Classify with Gemini
            mode = "Demo Classifier" if self.demo_mode else "Gemini AI"
            print(f"🤖 Step 3: Classifying with {mode}...")
            classification = self.classifier.classify_risk(context)
            result["classification"] = classification
            print(f"   ✓ Risk Level: {classification['risk_level']}")
            print(f"   ✓ Confidence: {classification.get('confidence', 'N/A')}")
            
            # STEP 4: Store result
            if save_result:
                print(f"💾 Step 4: Storing decision for audit...")
                decision_record = self.storage.store_decision(
                    case_id=case_id,
                    customer_name=case_data['customer_name'],
                    raw_case_data=case_data,
                    classification_result=classification
                )
                result["decision_record"] = decision_record
                print(f"   ✓ Saved as {decision_record['decision_id']}")
            
            result["success"] = True
            print(f"\n✅ Pipeline completed successfully for {case_id}")
            
        except Exception as e:
            result["error"] = str(e)
            print(f"\n❌ Pipeline error: {str(e)}")
        
        return result
    
    def get_all_cases(self):
        """Get list of all available cases."""
        return self.fetcher.get_all_cases()
    
    def get_case_ids(self):
        """Get list of all case IDs."""
        return self.fetcher.get_case_ids()
    
    def get_case_summary(self, case_id: str):
        """Get formatted case summary."""
        return self.fetcher.get_case_summary(case_id)
    
    def get_statistics(self):
        """Get classification statistics."""
        return self.storage.get_statistics()
    
    def get_all_decisions(self):
        """Get all stored decisions."""
        return self.storage.get_all_decisions()


# Quick test
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RISK CLASSIFICATION PIPELINE - TEST RUN")
    print("=" * 60)
    
    # Initialize pipeline in demo mode
    pipeline = RiskClassificationPipeline(use_demo=True)
    
    # Process a few cases
    test_cases = ["CASE004", "CASE007", "CASE003"]
    
    for case_id in test_cases:
        print("\n" + "-" * 60)
        result = pipeline.process_case(case_id)
        
        if result["success"]:
            print(f"\n📋 RESULT SUMMARY:")
            print(f"   Customer: {result['case_data']['customer_name']}")
            print(f"   Amount: ₹{result['case_data']['amount']:,}")
            print(f"   Risk: {result['classification']['risk_level']}")
            print(f"   Reason: {result['classification']['reason']}")
    
    print("\n" + "=" * 60)
    print("📊 OVERALL STATISTICS:")
    stats = pipeline.get_statistics()
    print(f"   Total Decisions: {stats['total']}")
    print(f"   High Risk: {stats['high']} ({stats.get('high_percentage', 0)}%)")
    print(f"   Medium Risk: {stats['medium']} ({stats.get('medium_percentage', 0)}%)")
    print(f"   Low Risk: {stats['low']} ({stats.get('low_percentage', 0)}%)")
    print("=" * 60)
