"""
Main entry point for the AI Tech Consultant Agent system.
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import setup_langfuse_tracing
from core.shared_memory import shared_memory
from agents.orchestrator_agent import orchestrator_agent

def main():
    """Main function to run the AI Tech Consultant Agent."""
    print("🤖 AI Tech Consultant Agent")
    print("=" * 50)
    
    # Initialize tracing
    setup_langfuse_tracing()
    
    # Initialize shared memory
    print("📚 Initializing shared memory system...")
    
    # Example usage
    print("\n🚀 Ready to generate technical proposals!")
    print("\nAvailable commands:")
    print("1. run_complete_workflow(tender_content='...') - Run full workflow")
    print("2. check_workflow_status() - Check current status")
    print("3. identify_missing_information() - Find missing info")
    print("4. generate_proposal_summary() - Get proposal summary")
    
    return {
        "status": "ready",
        "orchestrator_agent": orchestrator_agent,
        "shared_memory": shared_memory
    }

def run_example_workflow():
    """Run an example workflow with sample tender content."""
    print("\n🧪 Running example workflow...")
    
    # Sample tender content
    sample_tender = """
    TECHNICAL SOLUTION RFP
    
    Project: Customer Management System
    
    Requirements:
    - The system must be able to store customer information
    - The system should provide a web interface for customer management
    - The system must integrate with existing payment processing
    - The system should support user authentication and authorization
    - The system must be scalable to handle 10,000+ customers
    
    Technical Constraints:
    - Must use cloud-based infrastructure
    - Must support mobile access
    - Must have 99.9% uptime
    - Must be secure and compliant with data protection regulations
    
    Budget: $150,000 - $200,000
    Timeline: 12-16 weeks
    
    Success Criteria:
    - Improved customer data management efficiency
    - Reduced manual processing time by 50%
    - Enhanced customer experience
    """
    
    try:
        # Run the complete workflow
        result = orchestrator_agent.run_complete_workflow(tender_content=sample_tender)
        
        print("\n✅ Example workflow completed!")
        print(f"Status: {result.get('status', 'unknown')}")
        
        if result.get('status') == 'completed':
            print("🎉 All steps completed successfully!")
            
            # Generate summary
            summary = orchestrator_agent.generate_proposal_summary()
            if 'error' not in summary:
                print(f"\n📊 Proposal Summary:")
                print(f"Total Cost: ${summary.get('total_cost', 0):,.0f}")
                print(f"Duration: {summary.get('duration_weeks', 0)} weeks")
                print(f"Team Size: {summary.get('team_size', 0)} members")
                print(f"Risk Level: {summary.get('risk_level', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Example workflow failed: {str(e)}")
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    # Initialize the system
    system = main()
    
    # Check if we should run the example
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        run_example_workflow()
    else:
        print("\n💡 To run an example workflow, use: python main.py --example")
        print("💡 To use the system interactively, import and use the orchestrator_agent")
