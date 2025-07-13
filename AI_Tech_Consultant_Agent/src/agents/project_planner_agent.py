"""
Project Planner Agent - Creates project plans, timelines, and cost estimates.
"""

from typing import Dict, List, Any
from google.adk.agents import Agent
from litellm import LiteLLM
from src.tools.memory_tools import (
    get_latest_memory,
    store_project_plan,
    search_memories
)
from src.tools.planning_tools import (
    create_project_timeline,
    estimate_project_costs,
    create_resource_allocation,
    generate_risk_assessment,
    create_quality_assurance_plan
)


def create_comprehensive_project_plan() -> Dict[str, Any]:
    """
    Create a comprehensive project plan including timeline, costs, and resource allocation.
    
    Returns:
        Dictionary containing the complete project plan
    """
    # Get solution strategy from memory
    solution_strategy = get_latest_memory("solution_strategy")
    if not solution_strategy:
        return {"error": "No solution strategy found in memory"}
    
    strategy_data = solution_strategy.get("metadata", {}).get("data", {})
    implementation = strategy_data.get("implementation_approach", {})
    phases = implementation.get("phases", [])
    
    # Convert phases to timeline format
    timeline_phases = []
    for i, phase in enumerate(phases):
        phase_name = phase.get("name", f"Phase {i+1}")
        duration_text = phase.get("duration", "2-3 weeks")
        
        # Parse duration (simple parsing for "X-Y weeks" format)
        if "weeks" in duration_text:
            duration_parts = duration_text.split("-")
            if len(duration_parts) >= 2:
                duration_weeks = int(duration_parts[1].split()[0])
            else:
                duration_weeks = int(duration_parts[0].split()[0])
        else:
            duration_weeks = 3  # Default
        
        deliverables = phase.get("deliverables", [])
        tasks = []
        for j, deliverable in enumerate(deliverables):
            tasks.append({
                "name": f"Deliverable {j+1}",
                "description": deliverable,
                "assigned_to": "TBD",
                "priority": "high" if j == 0 else "medium"
            })
        
        timeline_phases.append({
            "name": phase_name,
            "duration_weeks": duration_weeks,
            "tasks": tasks
        })
    
    # Create project timeline
    timeline = create_project_timeline(timeline_phases)
    
    # Get team structure from implementation approach
    team_structure = implementation.get("team_structure", {})
    team_members = []
    
    for role, count in team_structure.items():
        for i in range(count):
            team_members.append({
                "name": f"{role.title()} {i+1}",
                "role": role.replace("_", " ").title(),
                "availability": 1.0,
                "skills": _get_skills_for_role(role)
            })
    
    # Create resource allocation
    resource_allocation = create_resource_allocation(team_members, timeline_phases)
    
    # Estimate costs
    tech_stack = strategy_data.get("technology_stack", {})
    components = _extract_components_from_tech_stack(tech_stack)
    cost_estimates = estimate_project_costs(components, len(team_members), timeline["total_duration_weeks"])
    
    # Generate risk assessment
    project_scope = strategy_data.get("solution_overview", {}).get("summary", "")
    risk_assessment = generate_risk_assessment(project_scope, timeline, team_members)
    
    # Create quality assurance plan
    qa_plan = create_quality_assurance_plan(timeline_phases)
    
    # Compile comprehensive project plan
    project_plan = {
        "project_overview": {
            "name": "Technical Solution Implementation",
            "description": strategy_data.get("solution_overview", {}).get("summary", ""),
            "objectives": strategy_data.get("solution_overview", {}).get("key_features", []),
            "success_criteria": strategy_data.get("success_metrics", {})
        },
        "timeline": timeline,
        "resource_allocation": resource_allocation,
        "cost_estimates": cost_estimates,
        "risk_assessment": risk_assessment,
        "quality_assurance": qa_plan,
        "assumptions": strategy_data.get("assumptions", []),
        "constraints": _identify_project_constraints(strategy_data)
    }
    
    # Store in memory
    memory_id = store_project_plan(project_plan)
    project_plan["memory_id"] = memory_id
    
    return project_plan

def _get_skills_for_role(role: str) -> List[str]:
    """Get skills for a specific role."""
    skills_map = {
        "project_manager": ["Project Management", "Agile", "Scrum", "Communication", "Risk Management"],
        "tech_lead": ["Architecture Design", "Code Review", "Technical Leadership", "System Design"],
        "frontend_developers": ["React", "JavaScript", "TypeScript", "CSS", "UI/UX"],
        "backend_developers": ["Node.js", "Python", "Database Design", "API Development", "Microservices"],
        "devops_engineer": ["Docker", "Kubernetes", "AWS", "CI/CD", "Infrastructure"],
        "qa_engineer": ["Testing", "Automation", "Quality Assurance", "Test Planning"]
    }
    return skills_map.get(role, ["General Development"])

def _extract_components_from_tech_stack(tech_stack: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract components from technology stack for cost estimation."""
    components = []
    
    # Infrastructure components
    infra = tech_stack.get("infrastructure", {})
    if infra.get("cloud_provider"):
        components.append({
            "type": "cloud_service",
            "name": f"{infra.get('cloud_provider')} Services",
            "monthly_cost": 200
        })
    
    # Database components
    db = tech_stack.get("database", {})
    if db.get("primary"):
        components.append({
            "type": "cloud_service",
            "name": f"{db.get('primary')} Database",
            "monthly_cost": 150
        })
    
    # Third-party services
    components.append({
        "type": "third_party_service",
        "name": "Monitoring Services",
        "monthly_cost": 50
    })
    
    components.append({
        "type": "third_party_service",
        "name": "Development Tools",
        "monthly_cost": 30
    })
    
    return components

def _identify_project_constraints(strategy_data: Dict[str, Any]) -> List[str]:
    """Identify project constraints from strategy data."""
    constraints = []
    
    # Timeline constraints
    timeline_estimate = strategy_data.get("timeline_estimate", {})
    if timeline_estimate.get("total_duration"):
        constraints.append(f"Project must be completed within {timeline_estimate['total_duration']}")
    
    # Budget constraints
    cost_estimates = strategy_data.get("cost_estimates", {})
    if cost_estimates.get("total"):
        constraints.append(f"Project budget: ${cost_estimates['total']:,.0f}")
    
    # Technical constraints
    tech_stack = strategy_data.get("technology_stack", {})
    if tech_stack.get("infrastructure", {}).get("cloud_provider"):
        constraints.append(f"Must use {tech_stack['infrastructure']['cloud_provider']} cloud platform")
    
    # Quality constraints
    constraints.extend([
        "Must meet security compliance requirements",
        "Must achieve 99.9% uptime",
        "Must support specified number of concurrent users"
    ])
    
    return constraints


def update_project_timeline(phase_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Update the project timeline based on new information or changes.
    
    Args:
        phase_updates: List of updates to phases with 'phase_name', 'new_duration', 'new_tasks' keys
    
    Returns:
        Updated project timeline
    """
    # Get current project plan
    project_plan = get_latest_memory("project_plan")
    if not project_plan:
        return {"error": "No project plan found in memory"}
    
    plan_data = project_plan.get("metadata", {}).get("data", {})
    current_timeline = plan_data.get("timeline", {})
    current_phases = current_timeline.get("phases", [])
    
    # Apply updates
    for update in phase_updates:
        phase_name = update.get("phase_name")
        new_duration = update.get("new_duration")
        new_tasks = update.get("new_tasks", [])
        
        for phase in current_phases:
            if phase.get("name") == phase_name:
                if new_duration:
                    phase["duration_weeks"] = new_duration
                if new_tasks:
                    phase["tasks"] = new_tasks
                break
    
    # Recalculate timeline
    updated_timeline = create_project_timeline(current_phases)
    
    # Update project plan
    plan_data["timeline"] = updated_timeline
    memory_id = store_project_plan(plan_data)
    
    return {
        "updated_timeline": updated_timeline,
        "memory_id": memory_id
    }


def generate_project_summary() -> Dict[str, Any]:
    """
    Generate a summary of the project plan for stakeholders.
    
    Returns:
        Dictionary containing project summary
    """
    # Get project plan from memory
    project_plan = get_latest_memory("project_plan")
    if not project_plan:
        return {"error": "No project plan found in memory"}
    
    plan_data = project_plan.get("metadata", {}).get("data", {})
    
    summary = {
        "project_name": plan_data.get("project_overview", {}).get("name", "Technical Solution Implementation"),
        "duration": plan_data.get("timeline", {}).get("total_duration_weeks", 0),
        "team_size": len(plan_data.get("resource_allocation", {}).get("team_members", [])),
        "total_cost": plan_data.get("cost_estimates", {}).get("total_cost", 0),
        "risk_level": plan_data.get("risk_assessment", {}).get("risk_level", "Unknown"),
        "key_milestones": plan_data.get("timeline", {}).get("milestones", []),
        "main_risks": [risk["risk"] for risk in plan_data.get("risk_assessment", {}).get("risks", [])[:3]]
    }
    
    return summary

# Define the Project Planner Agent
project_planner_agent = Agent(
    name="ProjectPlannerAgent",
    description="""
    A specialized agent that creates comprehensive project plans, timelines, 
    and cost estimates for technical solutions. This agent is responsible for:
    
    1. Creating detailed project timelines with phases and milestones
    2. Estimating project costs including labor, infrastructure, and third-party services
    3. Planning resource allocation and team structure
    4. Identifying and assessing project risks
    5. Creating quality assurance plans
    6. Documenting project assumptions and constraints
    7. Generating project summaries for stakeholders
    
    The agent uses the solution strategy to create realistic, actionable
    project plans that can be executed by development teams.
    
    When creating project plans:
    1. Review the solution strategy from shared memory
    2. Create realistic timelines based on the implementation approach
    3. Estimate costs accurately considering all components
    4. Plan resource allocation based on team structure
    5. Identify potential risks and mitigation strategies
    6. Create quality assurance plans
    7. Document all assumptions and constraints
    8. Store the complete plan in shared memory
    
    Focus on creating plans that are:
    - Realistic and achievable
    - Well-documented and clear
    - Comprehensive in scope
    - Aligned with the technical solution
    
    Always consider the client's constraints and preferences when planning
    timelines and resource allocation.
    """,
    model="gemini-2.0-flash-exp",
    tools=[
        search_memories,
        create_comprehensive_project_plan,
        update_project_timeline,
        generate_project_summary
    ]
)
