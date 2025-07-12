#!/usr/bin/env python3
"""
Example usage of the AI Tech Consultant Agent system.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from agents.orchestrator_agent import orchestrator_runner
from core.shared_memory import shared_memory

def example_basic_workflow():
    """Example of running a basic workflow with tender content."""
    print("🚀 Running Basic Workflow Example")
    print("=" * 50)
    
    # Sample tender content
    tender_content = """
    REQUEST FOR PROPOSAL: E-COMMERCE PLATFORM
    
    Project Overview:
    We are seeking a comprehensive e-commerce platform solution for our retail business.
    
    Functional Requirements:
    - User registration and authentication system
    - Product catalog with search and filtering
    - Shopping cart and checkout functionality
    - Order management and tracking
    - Payment processing integration
    - Admin dashboard for inventory management
    - Customer support system
    - Mobile-responsive design
    
    Technical Requirements:
    - Cloud-based deployment (AWS preferred)
    - Scalable architecture to handle 50,000+ users
    - 99.9% uptime requirement
    - PCI DSS compliance for payment processing
    - Integration with existing ERP system
    - Real-time inventory management
    - Analytics and reporting capabilities
    
    Budget: $200,000 - $300,000
    Timeline: 6-8 months
    Team Size: 6-8 developers
    
    Success Criteria:
    - 50% reduction in order processing time
    - 30% increase in online sales
    - Improved customer satisfaction scores
    - Seamless integration with existing systems
    """
    
    try:
        # Run the complete workflow using the agent runner
        print("📋 Starting proposal generation...")
        result = orchestrator_runner.run(f"Run the complete workflow with this tender content: {tender_content}")
        
        if result.get('status') == 'completed':
            print("✅ Workflow completed successfully!")
            
            # Get proposal summary
            summary = orchestrator_runner.run("Generate a proposal summary")
            if 'error' not in summary:
                print("\n📊 Proposal Summary:")
                print(f"Project: {summary.get('project_name', 'E-Commerce Platform')}")
                print(f"Total Cost: ${summary.get('total_cost', 0):,.0f}")
                print(f"Duration: {summary.get('duration_weeks', 0)} weeks")
                print(f"Team Size: {summary.get('team_size', 0)} members")
                print(f"Risk Level: {summary.get('risk_level', 'Unknown')}")
                print(f"Business Value: {summary.get('business_value', 'N/A')}")
            
            return result
        else:
            print(f"❌ Workflow failed: {result.get('error', 'Unknown error')}")
            return result
            
    except Exception as e:
        print(f"❌ Error running workflow: {str(e)}")
        return {"status": "failed", "error": str(e)}

def example_step_by_step():
    """Example of running the workflow step by step."""
    print("\n🔧 Running Step-by-Step Example")
    print("=" * 50)
    
    tender_content = """
    PROJECT: INVENTORY MANAGEMENT SYSTEM
    
    Requirements:
    - Track inventory levels in real-time
    - Generate purchase orders automatically
    - Barcode scanning integration
    - Reporting and analytics
    - User role management
    
    Budget: $100,000
    Timeline: 4 months
    """
    
    try:
        # Step 1: Analyze tender
        print("1️⃣ Analyzing tender document...")
        step1 = orchestrator_runner.run(f"Start proposal generation with this tender content: {tender_content}")
        print(f"   Status: {step1.get('status', 'unknown')}")
        
        # Step 2: Design solution strategy
        print("2️⃣ Designing solution strategy...")
        step2 = orchestrator_runner.run("Design solution strategy based on the tender analysis")
        print(f"   Status: {step2.get('status', 'unknown')}")
        
        # Step 3: Create visualizations
        print("3️⃣ Creating visualizations...")
        step3 = orchestrator_runner.run("Create visualizations for the technical proposal")
        print(f"   Status: {step3.get('status', 'unknown')}")
        
        # Step 4: Create project plan
        print("4️⃣ Creating project plan...")
        step4 = orchestrator_runner.run("Create project plan with timeline and costs")
        print(f"   Status: {step4.get('status', 'unknown')}")
        
        # Step 5: Generate final proposal
        print("5️⃣ Generating final proposal...")
        step5 = orchestrator_runner.run("Generate the final comprehensive technical proposal")
        print(f"   Status: {step5.get('status', 'unknown')}")
        
        print("✅ Step-by-step workflow completed!")
        
        # Check final status
        status = orchestrator_runner.run("Check the current workflow status")
        print(f"\n📈 Final Progress: {status.get('progress_percentage', 0)}%")
        print(f"Completed Steps: {', '.join(status.get('completed_steps', []))}")
        
        return {
            "step1": step1,
            "step2": step2,
            "step3": step3,
            "step4": step4,
            "step5": step5,
            "final_status": status
        }
        
    except Exception as e:
        print(f"❌ Error in step-by-step workflow: {str(e)}")
        return {"status": "failed", "error": str(e)}

def example_memory_operations():
    """Example of working with the shared memory system."""
    print("\n🧠 Memory Operations Example")
    print("=" * 50)
    
    try:
        # Get context summary
        context = shared_memory.get_context_summary()
        print(f"Current Context:\n{context}")
        
        # Search for specific information
        search_results = shared_memory.search_memories("architecture")
        print(f"\nFound {len(search_results)} memories containing 'architecture'")
        
        # Get latest tender analysis
        tender_analysis = shared_memory.get_latest_memory("tender_analysis")
        if tender_analysis:
            print(f"\nLatest tender analysis ID: {tender_analysis.get('id', 'N/A')}")
        
        return {
            "context_summary": context,
            "search_results_count": len(search_results),
            "has_tender_analysis": tender_analysis is not None
        }
        
    except Exception as e:
        print(f"❌ Error in memory operations: {str(e)}")
        return {"status": "failed", "error": str(e)}

def example_missing_information():
    """Example of identifying missing information."""
    print("\n🔍 Missing Information Analysis Example")
    print("=" * 50)
    
    try:
        # Check for missing information
        missing_info = orchestrator_runner.run("Identify any missing information that needs clarification")
        
        if 'error' not in missing_info:
            print(f"Total missing items: {missing_info.get('total_missing_items', 0)}")
            
            if missing_info.get('high_priority'):
                print("\n🚨 High Priority Missing Information:")
                for item in missing_info['high_priority']:
                    print(f"  - {item}")
            
            if missing_info.get('medium_priority'):
                print("\n⚠️ Medium Priority Missing Information:")
                for item in missing_info['medium_priority']:
                    print(f"  - {item}")
            
            if missing_info.get('recommendations'):
                print("\n💡 Recommendations:")
                for rec in missing_info['recommendations']:
                    print(f"  {rec}")
        else:
            print(f"❌ Error: {missing_info.get('error')}")
        
        return missing_info
        
    except Exception as e:
        print(f"❌ Error analyzing missing information: {str(e)}")
        return {"status": "failed", "error": str(e)}

def main():
    """Run all examples."""
    print("🤖 AI Tech Consultant Agent - Examples")
    print("=" * 60)
    
    # Check if we have the required environment
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Some features may not work.")
        print("   Set your API key in the .env file or environment variables.")
    
    # Run examples
    results = {}
    
    # Example 1: Basic workflow
    results['basic_workflow'] = example_basic_workflow()
    
    # Example 2: Step by step
    results['step_by_step'] = example_step_by_step()
    
    # Example 3: Memory operations
    results['memory_operations'] = example_memory_operations()
    
    # Example 4: Missing information
    results['missing_information'] = example_missing_information()
    
    # Summary
    print("\n📋 Example Summary")
    print("=" * 60)
    for example_name, result in results.items():
        status = result.get('status', 'unknown')
        print(f"{example_name}: {status}")
    
    print("\n🎉 All examples completed!")
    print("\n💡 To use the system in your own code:")
    print("   from src.agents.orchestrator_agent import orchestrator_runner")
    print("   result = orchestrator_runner.run('Run complete workflow with tender content: ...')")

if __name__ == "__main__":
    main() 