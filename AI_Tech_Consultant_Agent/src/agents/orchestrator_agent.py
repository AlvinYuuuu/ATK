"""
Orchestrator Agent - Coordinates all other agents and manages the proposal generation workflow.
"""

import asyncio
from typing import Dict, List, Any, Optional
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from src.tools.memory_tools import (
    get_context_summary,
    search_memories,
    get_latest_memory
)
from src.agents.tender_analysis_agent import tender_analysis_agent
from src.agents.solution_strategy_agent import solution_strategy_agent
from src.agents.visualization_agent import visualization_agent
from src.agents.project_planner_agent import project_planner_agent
from src.agents.technical_writer_agent import technical_writer_agent
from src.core.agent_runner import create_simple_runner


async def start_proposal_generation(tender_content: Optional[str] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Start the proposal generation process by analyzing the tender document.
    
    Args:
        tender_content: Direct text content of the tender
        file_path: Path to the tender document file
    
    Returns:
        Dictionary containing the initial analysis results
    """
    # Step 1: Analyze tender document
    print("🔍 Starting tender analysis...")
    
    if file_path:
        analysis_result = await tender_analysis_agent.run_async(f"Analyze the tender document at {file_path}")
    elif tender_content:
        analysis_result = await tender_analysis_agent.run_async(f"Analyze this tender content: {tender_content}")
    else:
        return {"error": "Either tender_content or file_path must be provided"}
    
    print("✅ Tender analysis completed")
    
    return {
        "status": "tender_analyzed",
        "analysis_result": analysis_result,
        "next_step": "design_solution_strategy"
    }


async def design_solution_strategy() -> Dict[str, Any]:
    """
    Design the solution strategy based on tender analysis.
    
    Returns:
        Dictionary containing the solution strategy
    """
    print("🧠 Designing solution strategy...")
    
    # Step 2: Design solution strategy
    strategy_result = await solution_strategy_agent.run_async("Design a comprehensive solution strategy based on the tender analysis")
    
    print("✅ Solution strategy completed")
    
    return {
        "status": "strategy_designed",
        "strategy_result": strategy_result,
        "next_step": "create_visualizations"
    }


async def create_visualizations() -> Dict[str, Any]:
    """
    Create all necessary diagrams and visualizations.
    
    Returns:
        Dictionary containing the created visualizations
    """
    print("📊 Creating visualizations...")
    
    # Step 3: Create visualizations
    viz_result = await visualization_agent.run_async("Create all necessary diagrams for the technical proposal")
    
    print("✅ Visualizations completed")
    
    return {
        "status": "visualizations_created",
        "visualization_result": viz_result,
        "next_step": "create_project_plan"
    }


async def create_project_plan() -> Dict[str, Any]:
    """
    Create the project plan with timeline and cost estimates.
    
    Returns:
        Dictionary containing the project plan
    """
    print("📋 Creating project plan...")
    
    # Step 4: Create project plan
    plan_result = await project_planner_agent.run_async("Create a comprehensive project plan including timeline, costs, and resource allocation")
    
    print("✅ Project plan completed")
    
    return {
        "status": "project_plan_created",
        "plan_result": plan_result,
        "next_step": "generate_final_proposal"
    }


async def generate_final_proposal() -> Dict[str, Any]:
    """
    Generate the final comprehensive technical proposal.
    
    Returns:
        Dictionary containing the complete proposal
    """
    print("📄 Generating final proposal...")
    
    # Step 5: Generate final proposal
    proposal_result = await technical_writer_agent.run_async("Create a comprehensive technical proposal combining all analysis and planning")
    
    print("✅ Final proposal completed")
    
    return {
        "status": "proposal_generated",
        "proposal_result": proposal_result,
        "next_step": "complete"
    }


async def run_complete_workflow(tender_content: Optional[str] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Run the complete proposal generation workflow from start to finish.
    
    Args:
        tender_content: Direct text content of the tender
        file_path: Path to the tender document file
    
    Returns:
        Dictionary containing the complete workflow results
    """
    workflow_results = {}
    
    try:
        # Step 1: Analyze tender
        print("🚀 Starting complete proposal generation workflow...")
        step1_result = await start_proposal_generation(tender_content, file_path)
        workflow_results["tender_analysis"] = step1_result
        
        # Step 2: Design solution strategy
        step2_result = await design_solution_strategy()
        workflow_results["solution_strategy"] = step2_result
        
        # Step 3: Create visualizations
        step3_result = await create_visualizations()
        workflow_results["visualizations"] = step3_result
        
        # Step 4: Create project plan
        step4_result = await create_project_plan()
        workflow_results["project_plan"] = step4_result
        
        # Step 5: Generate final proposal
        step5_result = await generate_final_proposal()
        workflow_results["final_proposal"] = step5_result
        
        print("🎉 Complete workflow finished successfully!")
        
        return {
            "status": "completed",
            "workflow_results": workflow_results,
            "summary": "All steps completed successfully"
        }
        
    except Exception as e:
        print(f"❌ Workflow failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "workflow_results": workflow_results
        }


def check_workflow_status() -> Dict[str, Any]:
    """
    Check the current status of the proposal generation workflow.
    
    Returns:
        Dictionary containing the current workflow status
    """
    context_summary = get_context_summary()
    
    # Check what has been completed
    completed_steps = []
    missing_steps = []
    
    if get_latest_memory("tender_analysis"):
        completed_steps.append("tender_analysis")
    else:
        missing_steps.append("tender_analysis")
    
    if get_latest_memory("solution_strategy"):
        completed_steps.append("solution_strategy")
    else:
        missing_steps.append("solution_strategy")
    
    if get_latest_memory("visualization"):
        completed_steps.append("visualizations")
    else:
        missing_steps.append("visualizations")
    
    if get_latest_memory("project_plan"):
        completed_steps.append("project_plan")
    else:
        missing_steps.append("project_plan")
    
    if get_latest_memory("technical_proposal"):
        completed_steps.append("final_proposal")
    else:
        missing_steps.append("final_proposal")
    
    progress_percentage = (len(completed_steps) / 5) * 100
    
    return {
        "progress_percentage": progress_percentage,
        "completed_steps": completed_steps,
        "missing_steps": missing_steps,
        "context_summary": context_summary,
        "next_recommended_step": missing_steps[0] if missing_steps else "complete"
    }


def identify_missing_information() -> Dict[str, Any]:
    """
    Identify any missing information that needs to be clarified with the client.
    
    Returns:
        Dictionary containing missing information analysis
    """
    tender_analysis = get_latest_memory("tender_analysis")
    
    if not tender_analysis:
        return {"error": "No tender analysis found. Please run tender analysis first."}
    
    analysis_data = tender_analysis.get("metadata", {}).get("data", {})
    missing_info = analysis_data.get("missing_information", [])
    
    # Categorize missing information by priority
    high_priority = []
    medium_priority = []
    low_priority = []
    
    priority_keywords = {
        "high": ["budget", "cost", "timeline", "deadline", "requirements", "scope"],
        "medium": ["technical", "integration", "security", "compliance"],
        "low": ["background", "stakeholders", "success_criteria"]
    }
    
    for item in missing_info:
        item_lower = item.lower()
        if any(keyword in item_lower for keyword in priority_keywords["high"]):
            high_priority.append(item)
        elif any(keyword in item_lower for keyword in priority_keywords["medium"]):
            medium_priority.append(item)
        else:
            low_priority.append(item)
    
    return {
        "total_missing_items": len(missing_info),
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority,
        "recommendations": _generate_clarification_recommendations(high_priority, medium_priority)
    }

def _generate_clarification_recommendations(high_priority: List[str], medium_priority: List[str]) -> List[str]:
    """Generate recommendations for clarifying missing information."""
    recommendations = []
    
    if high_priority:
        recommendations.append("Please provide the following critical information:")
        for item in high_priority:
            recommendations.append(f"- {item}")
    
    if medium_priority:
        recommendations.append("The following information would be helpful to refine the solution:")
        for item in medium_priority:
            recommendations.append(f"- {item}")
    
    if not high_priority and not medium_priority:
        recommendations.append("All critical information has been provided. The proposal can proceed.")
    
    return recommendations


def generate_proposal_summary() -> Dict[str, Any]:
    """
    Generate a summary of the current proposal status and key information.
    
    Returns:
        Dictionary containing proposal summary
    """
    # Get latest proposal
    proposal = get_latest_memory("technical_proposal")
    
    if not proposal:
        return {"error": "No technical proposal found. Please complete the workflow first."}
    
    proposal_data = proposal.get("metadata", {}).get("data", {})
    executive_summary = proposal_data.get("executive_summary", {})
    
    summary = {
        "project_name": "Technical Solution Implementation",
        "total_cost": executive_summary.get("total_cost", 0),
        "duration_weeks": executive_summary.get("duration", 0),
        "team_size": executive_summary.get("team_size", 0),
        "risk_level": executive_summary.get("risk_level", "Medium"),
        "key_features": executive_summary.get("key_features", []),
        "business_value": executive_summary.get("business_value", ""),
        "status": "ready_for_review"
    }
    
    return summary

def start_proposal_generation_sync(tender_content: Optional[str] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Start the proposal generation process by analyzing the tender document.
    
    Args:
        tender_content: Direct text content of the tender
        file_path: Path to the tender document file
    
    Returns:
        Dictionary containing the initial analysis results
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're in an existing event loop, create a task
            task = asyncio.create_task(start_proposal_generation(tender_content, file_path))
            # This is a sync function, so we need to wait for the result
            # We'll return a placeholder and let the async function handle it
            return {"status": "started", "message": "Proposal generation started asynchronously"}
        else:
            # If no event loop is running, we can use asyncio.run()
            return asyncio.run(start_proposal_generation(tender_content, file_path))
    except RuntimeError:
        # Fallback for when we can't get the event loop
        return {"status": "error", "message": "Cannot run async function in current context"}


def design_solution_strategy_sync() -> Dict[str, Any]:
    """
    Design the solution strategy based on tender analysis.
    
    Returns:
        Dictionary containing the solution strategy
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return {"status": "started", "message": "Solution strategy design started asynchronously"}
        else:
            return asyncio.run(design_solution_strategy())
    except RuntimeError:
        return {"status": "error", "message": "Cannot run async function in current context"}


def create_visualizations_sync() -> Dict[str, Any]:
    """
    Create visualizations for the proposal.
    
    Returns:
        Dictionary containing the visualization results
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return {"status": "started", "message": "Visualization creation started asynchronously"}
        else:
            return asyncio.run(create_visualizations())
    except RuntimeError:
        return {"status": "error", "message": "Cannot run async function in current context"}


def create_project_plan_sync() -> Dict[str, Any]:
    """
    Create a detailed project plan.
    
    Returns:
        Dictionary containing the project plan
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return {"status": "started", "message": "Project plan creation started asynchronously"}
        else:
            return asyncio.run(create_project_plan())
    except RuntimeError:
        return {"status": "error", "message": "Cannot run async function in current context"}


def generate_final_proposal_sync() -> Dict[str, Any]:
    """
    Generate the final proposal document.
    
    Returns:
        Dictionary containing the final proposal
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return {"status": "started", "message": "Final proposal generation started asynchronously"}
        else:
            return asyncio.run(generate_final_proposal())
    except RuntimeError:
        return {"status": "error", "message": "Cannot run async function in current context"}


def run_complete_workflow_sync(tender_content: Optional[str] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Run the complete proposal generation workflow from start to finish.
    
    Args:
        tender_content: Direct text content of the tender
        file_path: Path to the tender document file
    
    Returns:
        Dictionary containing the complete workflow results
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return {"status": "started", "message": "Complete workflow started asynchronously"}
        else:
            return asyncio.run(run_complete_workflow(tender_content, file_path))
    except RuntimeError:
        return {"status": "error", "message": "Cannot run async function in current context"}

# Define the Orchestrator Agent
orchestrator_agent = Agent(
    name="OrchestratorAgent",
    model="gemini-2.0-flash-exp",
    description="""
    The central orchestrator that coordinates all other agents in the AI Tech Consultant system.
    This agent is responsible for:
    
    1. Managing the complete proposal generation workflow
    2. Coordinating between specialized agents
    3. Tracking workflow progress and status
    4. Identifying missing information that needs client clarification
    5. Ensuring all steps are completed in the correct order
    6. Providing workflow status updates and summaries
    7. Handling errors and workflow recovery
    
    The orchestrator acts as the single point of contact for users and ensures
    that the multi-agent system works together seamlessly to generate comprehensive
    technical proposals.
    
    Your primary responsibilities:
    1. **Workflow Management**: Guide users through the complete proposal generation process
    2. **Agent Coordination**: Ensure all specialized agents work together effectively
    3. **Progress Tracking**: Monitor and report on workflow progress
    4. **Quality Assurance**: Ensure all steps are completed properly before proceeding
    5. **Error Handling**: Handle issues and provide recovery options
    6. **Client Communication**: Identify when additional information is needed from clients
    
    Workflow Steps:
    1. **Tender Analysis**: Analyze the tender document to extract requirements
    2. **Solution Strategy**: Design the technical solution and architecture
    3. **Visualizations**: Create diagrams and visual aids
    4. **Project Planning**: Create timeline, costs, and resource allocation
    5. **Final Proposal**: Generate the comprehensive technical proposal
    
    Always:
    - Check workflow status before proceeding
    - Identify missing information that needs clarification
    - Provide clear progress updates
    - Handle errors gracefully
    - Ensure all steps are completed before moving to the next
    
    You are the friendly, helpful interface between users and the complex
    multi-agent system, making the proposal generation process smooth and efficient.
    """,
    tools=[
        AgentTool(
            agent=tender_analysis_agent
        ),
        AgentTool(
            agent=solution_strategy_agent
        ),
        AgentTool(
            agent=visualization_agent
        ),
        AgentTool(
            agent=project_planner_agent
        ),
        AgentTool(
            agent=technical_writer_agent
        ),
        search_memories,
        # start_proposal_generation_sync,
        # design_solution_strategy_sync,
        # create_visualizations_sync,
        # create_project_plan_sync,
        # generate_final_proposal_sync,
        # run_complete_workflow_sync,
        # check_workflow_status,
        # identify_missing_information,
        # generate_proposal_summary
    ]
)

# # Create a simple runner for the orchestrator agent
# from src.core.agent_runner import create_simple_runner
# orchestrator_runner = create_simple_runner(orchestrator_agent)
