"""
Technical Writer Agent - Creates comprehensive technical proposals and documentation.
"""

from typing import Dict, List, Any
from google.adk.agents import Agent
from litellm import LiteLLM
from src.tools.memory_tools import (
    get_latest_memory, 
    store_technical_proposal, 
    search_memories,
    get_all_memories
)


def create_comprehensive_proposal() -> Dict[str, Any]:
    """
    Create a comprehensive technical proposal combining all analysis and planning.
    
    Returns:
        Dictionary containing the complete technical proposal
    """
    # Gather all information from memory
    tender_analysis = get_latest_memory("tender_analysis")
    solution_strategy = get_latest_memory("solution_strategy")
    project_plan = get_latest_memory("project_plan")
    visualizations = get_all_memories("visualization")
    
    if not tender_analysis or not solution_strategy:
        return {"error": "Missing required analysis or strategy data"}
    
    # Extract data
    analysis_data = tender_analysis.get("metadata", {}).get("data", {})
    strategy_data = solution_strategy.get("metadata", {}).get("data", {})
    plan_data = project_plan.get("metadata", {}).get("data", {}) if project_plan else {}
    
    # Create comprehensive proposal
    proposal = {
        "executive_summary": _create_executive_summary(analysis_data, strategy_data, plan_data),
        "client_background": _extract_client_background(analysis_data),
        "requirements_analysis": _format_requirements_analysis(analysis_data),
        "proposed_solution": _format_proposed_solution(strategy_data),
        "technical_architecture": _format_technical_architecture(strategy_data),
        "implementation_plan": _format_implementation_plan(strategy_data, plan_data),
        "project_timeline": _format_project_timeline(plan_data),
        "cost_breakdown": _format_cost_breakdown(plan_data),
        "risk_assessment": _format_risk_assessment(plan_data),
        "quality_assurance": _format_quality_assurance(plan_data),
        "diagrams_and_visualizations": _format_visualizations(visualizations),
        "assumptions_and_constraints": _format_assumptions_constraints(strategy_data, plan_data),
        "next_steps": _create_next_steps()
    }
    
    # Store in memory
    memory_id = store_technical_proposal(proposal)
    proposal["memory_id"] = memory_id
    
    return proposal

def _create_executive_summary(analysis_data: Dict[str, Any], strategy_data: Dict[str, Any], plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create an executive summary for the proposal."""
    requirements = analysis_data.get("requirements", {})
    solution_overview = strategy_data.get("solution_overview", {})
    
    summary = {
        "project_overview": solution_overview.get("summary", "Comprehensive technical solution"),
        "business_value": solution_overview.get("business_value", "Improved efficiency and cost reduction"),
        "key_features": solution_overview.get("key_features", []),
        "total_cost": plan_data.get("cost_estimates", {}).get("total_cost", 0) if plan_data else 0,
        "duration": plan_data.get("timeline", {}).get("total_duration_weeks", 0) if plan_data else 0,
        "team_size": len(plan_data.get("resource_allocation", {}).get("team_members", [])) if plan_data else 0,
        "risk_level": plan_data.get("risk_assessment", {}).get("risk_level", "Medium") if plan_data else "Medium"
    }
    
    return summary

def _extract_client_background(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and format client background information."""
    requirements = analysis_data.get("requirements", {})
    
    background = {
        "client_description": requirements.get("client_background", "Client information to be provided"),
        "project_scope": requirements.get("project_scope", "Project scope to be defined"),
        "key_stakeholders": requirements.get("key_stakeholders", []),
        "success_criteria": requirements.get("success_criteria", [])
    }
    
    return background

def _format_requirements_analysis(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the requirements analysis section."""
    requirements = analysis_data.get("requirements", {})
    missing_info = analysis_data.get("missing_information", [])
    
    formatted_requirements = {
        "functional_requirements": requirements.get("functional_requirements", []),
        "non_functional_requirements": requirements.get("non_functional_requirements", []),
        "technical_constraints": requirements.get("technical_constraints", []),
        "budget_constraints": requirements.get("budget_constraints", []),
        "timeline_constraints": requirements.get("timeline_constraints", []),
        "missing_information": missing_info,
        "document_quality_score": analysis_data.get("structure_analysis", {}).get("document_quality_score", 0)
    }
    
    return formatted_requirements

def _format_proposed_solution(strategy_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the proposed solution section."""
    solution_overview = strategy_data.get("solution_overview", {})
    tech_stack = strategy_data.get("technology_stack", {})
    
    solution = {
        "overview": solution_overview.get("summary", ""),
        "key_features": solution_overview.get("key_features", []),
        "business_value": solution_overview.get("business_value", ""),
        "differentiators": solution_overview.get("differentiators", []),
        "technology_stack": {
            "frontend": tech_stack.get("frontend", {}),
            "backend": tech_stack.get("backend", {}),
            "database": tech_stack.get("database", {}),
            "infrastructure": tech_stack.get("infrastructure", {}),
            "monitoring": tech_stack.get("monitoring", {})
        }
    }
    
    return solution

def _format_technical_architecture(strategy_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the technical architecture section."""
    architecture = strategy_data.get("technical_architecture", {})
    
    return {
        "layers": architecture.get("layers", {}),
        "integration_points": architecture.get("integration_points", []),
        "security_measures": architecture.get("security_measures", []),
        "scalability_features": [
            "Horizontal scaling with load balancers",
            "Database read replicas",
            "Caching layers for performance",
            "Microservices architecture"
        ]
    }

def _format_implementation_plan(strategy_data: Dict[str, Any], plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the implementation plan section."""
    implementation = strategy_data.get("implementation_approach", {})
    
    return {
        "methodology": implementation.get("methodology", "Agile with Scrum"),
        "phases": implementation.get("phases", []),
        "team_structure": implementation.get("team_structure", {}),
        "quality_gates": plan_data.get("quality_assurance", {}).get("quality_gates", []) if plan_data else []
    }

def _format_project_timeline(plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the project timeline section."""
    if not plan_data:
        return {"error": "No project plan data available"}
    
    timeline = plan_data.get("timeline", {})
    
    return {
        "total_duration": timeline.get("total_duration_weeks", 0),
        "start_date": timeline.get("start_date", ""),
        "end_date": timeline.get("end_date", ""),
        "phases": timeline.get("phases", []),
        "milestones": timeline.get("milestones", [])
    }

def _format_cost_breakdown(plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the cost breakdown section."""
    if not plan_data:
        return {"error": "No project plan data available"}
    
    cost_estimates = plan_data.get("cost_estimates", {})
    
    return {
        "total_cost": cost_estimates.get("total_cost", 0),
        "breakdown": {
            "labor_cost": cost_estimates.get("labor_cost", {}),
            "infrastructure_cost": cost_estimates.get("infrastructure_cost", {}),
            "third_party_cost": cost_estimates.get("third_party_cost", {}),
            "contingency": cost_estimates.get("contingency", {})
        },
        "payment_schedule": [
            {"milestone": "Project Start", "percentage": 25},
            {"milestone": "Phase 1 Complete", "percentage": 25},
            {"milestone": "Phase 2 Complete", "percentage": 25},
            {"milestone": "Project Completion", "percentage": 25}
        ]
    }

def _format_risk_assessment(plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the risk assessment section."""
    if not plan_data:
        return {"error": "No project plan data available"}
    
    risk_assessment = plan_data.get("risk_assessment", {})
    
    return {
        "overall_risk_level": risk_assessment.get("risk_level", "Medium"),
        "risk_score": risk_assessment.get("overall_risk_score", 0),
        "risks": risk_assessment.get("risks", []),
        "mitigation_strategies": risk_assessment.get("recommendations", [])
    }

def _format_quality_assurance(plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the quality assurance section."""
    if not plan_data:
        return {"error": "No project plan data available"}
    
    qa_plan = plan_data.get("quality_assurance", {})
    
    return {
        "testing_strategy": qa_plan.get("testing_strategy", {}),
        "quality_gates": qa_plan.get("quality_gates", []),
        "review_process": qa_plan.get("review_process", {}),
        "metrics": qa_plan.get("metrics", {})
    }

def _format_visualizations(visualizations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Format the diagrams and visualizations section."""
    formatted_viz = {}
    
    for viz in visualizations:
        viz_data = viz.get("metadata", {})
        diagram_type = viz_data.get("diagram_type", "unknown")
        formatted_viz[diagram_type] = {
            "description": viz_data.get("description", ""),
            "mermaid_code": viz_data.get("mermaid_code", ""),
            "memory_id": viz.get("id", "")
        }
    
    return formatted_viz

def _format_assumptions_constraints(strategy_data: Dict[str, Any], plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the assumptions and constraints section."""
    assumptions = strategy_data.get("assumptions", [])
    constraints = plan_data.get("constraints", []) if plan_data else []
    
    return {
        "assumptions": assumptions,
        "constraints": constraints,
        "dependencies": [
            "Client approval and sign-off",
            "Access to existing systems",
            "Timely feedback and communication",
            "Resource availability"
        ]
    }

def _create_next_steps() -> List[str]:
    """Create the next steps section."""
    return [
        "Review and approve the technical proposal",
        "Sign the project agreement",
        "Schedule project kickoff meeting",
        "Provide access to existing systems and documentation",
        "Assign project team members",
        "Begin project planning and setup phase"
    ]


def generate_proposal_summary() -> Dict[str, Any]:
    """
    Generate a summary of the technical proposal for quick review.
    
    Returns:
        Dictionary containing proposal summary
    """
    proposal = get_latest_memory("technical_proposal")
    if not proposal:
        return {"error": "No technical proposal found in memory"}
    
    proposal_data = proposal.get("metadata", {}).get("data", {})
    executive_summary = proposal_data.get("executive_summary", {})
    
    summary = {
        "project_name": "Technical Solution Implementation",
        "total_cost": executive_summary.get("total_cost", 0),
        "duration_weeks": executive_summary.get("duration", 0),
        "team_size": executive_summary.get("team_size", 0),
        "risk_level": executive_summary.get("risk_level", "Medium"),
        "key_features": executive_summary.get("key_features", []),
        "business_value": executive_summary.get("business_value", "")
    }
    
    return summary


def export_proposal_to_markdown() -> str:
    """
    Export the technical proposal to Markdown format.
    
    Returns:
        Markdown formatted proposal
    """
    proposal = get_latest_memory("technical_proposal")
    if not proposal:
        return "# Error: No technical proposal found in memory"
    
    proposal_data = proposal.get("metadata", {}).get("data", {})
    
    markdown = "# Technical Proposal\n\n"
    
    # Executive Summary
    exec_summary = proposal_data.get("executive_summary", {})
    markdown += "## Executive Summary\n\n"
    markdown += f"**Project Overview:** {exec_summary.get('project_overview', '')}\n\n"
    markdown += f"**Business Value:** {exec_summary.get('business_value', '')}\n\n"
    markdown += f"**Total Cost:** ${exec_summary.get('total_cost', 0):,.0f}\n\n"
    markdown += f"**Duration:** {exec_summary.get('duration', 0)} weeks\n\n"
    markdown += f"**Team Size:** {exec_summary.get('team_size', 0)} members\n\n"
    markdown += f"**Risk Level:** {exec_summary.get('risk_level', 'Medium')}\n\n"
    
    # Requirements Analysis
    req_analysis = proposal_data.get("requirements_analysis", {})
    markdown += "## Requirements Analysis\n\n"
    markdown += "### Functional Requirements\n"
    for req in req_analysis.get("functional_requirements", []):
        markdown += f"- {req}\n"
    markdown += "\n"
    
    # Proposed Solution
    solution = proposal_data.get("proposed_solution", {})
    markdown += "## Proposed Solution\n\n"
    markdown += f"{solution.get('overview', '')}\n\n"
    markdown += "### Key Features\n"
    for feature in solution.get("key_features", []):
        markdown += f"- {feature}\n"
    markdown += "\n"
    
    # Implementation Plan
    impl_plan = proposal_data.get("implementation_plan", {})
    markdown += "## Implementation Plan\n\n"
    markdown += f"**Methodology:** {impl_plan.get('methodology', '')}\n\n"
    markdown += "### Phases\n"
    for phase in impl_plan.get("phases", []):
        markdown += f"- **{phase.get('name', '')}:** {phase.get('duration', '')}\n"
    markdown += "\n"
    
    # Next Steps
    next_steps = proposal_data.get("next_steps", [])
    markdown += "## Next Steps\n\n"
    for step in next_steps:
        markdown += f"- {step}\n"
    markdown += "\n"
    
    return markdown

# Define the Technical Writer Agent
technical_writer_agent = Agent(
    name="TechnicalWriterAgent",
    description="""
    A specialized agent that creates comprehensive technical proposals and documentation.
    This agent is responsible for:
    
    1. Creating executive summaries for stakeholders
    2. Formatting requirements analysis in a clear, structured manner
    3. Presenting the proposed solution with business value
    4. Documenting technical architecture and implementation plans
    5. Creating project timelines and cost breakdowns
    6. Formatting risk assessments and quality assurance plans
    7. Integrating diagrams and visualizations
    8. Documenting assumptions, constraints, and next steps
    9. Exporting proposals in various formats (Markdown, etc.)
    
    The agent synthesizes information from all other agents to create
    professional, comprehensive technical proposals that are ready for
    client presentation and approval.
    
    When creating proposals:
    1. Gather all information from shared memory (tender analysis, solution strategy, project plan, visualizations)
    2. Create a clear, professional structure that flows logically
    3. Include an executive summary for stakeholders
    4. Present requirements analysis in a structured format
    5. Clearly articulate the proposed solution and its business value
    6. Document technical architecture and implementation plans
    7. Include project timeline and cost breakdown
    8. Present risk assessment and mitigation strategies
    9. Include quality assurance plans
    10. Integrate all diagrams and visualizations
    11. Document assumptions, constraints, and next steps
    12. Store the complete proposal in shared memory
    
    Focus on creating proposals that are:
    - Professional and well-structured
    - Clear and easy to understand
    - Comprehensive in scope
    - Ready for client presentation
    
    Always ensure the proposal addresses all client requirements and
    provides clear value propositions.
    """,
    model="gemini-2.0-flash-exp",
    tools=[
        search_memories,
        create_comprehensive_proposal,
        generate_proposal_summary,
        export_proposal_to_markdown
    ]
)
