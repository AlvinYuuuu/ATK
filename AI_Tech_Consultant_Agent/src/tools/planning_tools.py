"""
Planning tools for project timeline and cost estimation.
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta



def create_project_timeline(phases: List[Dict[str, Any]], start_date: str = None) -> Dict[str, Any]:
    """
    Create a detailed project timeline based on phases and tasks.
    
    Args:
        phases: List of phase dictionaries with 'name', 'duration_weeks', 'tasks' keys
        start_date: Start date in YYYY-MM-DD format (defaults to today)
    
    Returns:
        Dictionary containing timeline information
    """
    if start_date is None:
        start_date = datetime.now().strftime("%Y-%m-%d")
    
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    timeline = {
        "start_date": start_date,
        "phases": [],
        "total_duration_weeks": 0,
        "milestones": []
    }
    
    for i, phase in enumerate(phases):
        phase_name = phase.get('name', f'Phase {i+1}')
        duration_weeks = phase.get('duration_weeks', 2)
        tasks = phase.get('tasks', [])
        
        phase_start = current_date
        phase_end = current_date + timedelta(weeks=duration_weeks)
        
        phase_info = {
            "name": phase_name,
            "start_date": phase_start.strftime("%Y-%m-%d"),
            "end_date": phase_end.strftime("%Y-%m-%d"),
            "duration_weeks": duration_weeks,
            "tasks": []
        }
        
        # Add tasks to phase
        task_duration = duration_weeks / max(len(tasks), 1)
        for j, task in enumerate(tasks):
            task_start = phase_start + timedelta(weeks=j * task_duration)
            task_end = task_start + timedelta(weeks=task_duration)
            
            task_info = {
                "name": task.get('name', f'Task {j+1}'),
                "description": task.get('description', ''),
                "start_date": task_start.strftime("%Y-%m-%d"),
                "end_date": task_end.strftime("%Y-%m-%d"),
                "duration_weeks": task_duration,
                "assigned_to": task.get('assigned_to', 'TBD'),
                "priority": task.get('priority', 'medium')
            }
            phase_info["tasks"].append(task_info)
        
        timeline["phases"].append(phase_info)
        timeline["total_duration_weeks"] += duration_weeks
        
        # Add milestone at end of phase
        milestone = {
            "name": f"Complete {phase_name}",
            "date": phase_end.strftime("%Y-%m-%d"),
            "description": f"All tasks in {phase_name} completed"
        }
        timeline["milestones"].append(milestone)
        
        current_date = phase_end
    
    timeline["end_date"] = current_date.strftime("%Y-%m-%d")
    
    return timeline


def estimate_project_costs(components: List[Dict[str, Any]], team_size: int = 5, duration_weeks: int = 12) -> Dict[str, Any]:
    """
    Estimate project costs based on components, team size, and duration.
    
    Args:
        components: List of component dictionaries with cost information
        team_size: Number of team members
        duration_weeks: Project duration in weeks
    
    Returns:
        Dictionary containing cost breakdown
    """
    # Labor costs (assuming average developer cost)
    hourly_rate = 75  # USD per hour
    hours_per_week = 40
    labor_cost = team_size * hourly_rate * hours_per_week * duration_weeks
    
    # Infrastructure costs
    infrastructure_cost = 0
    for component in components:
        component_type = component.get('type', 'software')
        if component_type == 'cloud_service':
            monthly_cost = component.get('monthly_cost', 100)
            infrastructure_cost += monthly_cost * (duration_weeks / 4)
        elif component_type == 'hardware':
            infrastructure_cost += component.get('one_time_cost', 0)
        elif component_type == 'software_license':
            license_cost = component.get('license_cost', 0)
            if component.get('recurring', False):
                infrastructure_cost += license_cost * (duration_weeks / 4)
            else:
                infrastructure_cost += license_cost
    
    # Third-party service costs
    third_party_cost = 0
    for component in components:
        if component.get('type') == 'third_party_service':
            monthly_cost = component.get('monthly_cost', 50)
            third_party_cost += monthly_cost * (duration_weeks / 4)
    
    # Contingency (20% of total)
    subtotal = labor_cost + infrastructure_cost + third_party_cost
    contingency = subtotal * 0.2
    
    total_cost = subtotal + contingency
    
    cost_breakdown = {
        "labor_cost": {
            "amount": labor_cost,
            "percentage": (labor_cost / total_cost) * 100,
            "description": f"Team of {team_size} for {duration_weeks} weeks"
        },
        "infrastructure_cost": {
            "amount": infrastructure_cost,
            "percentage": (infrastructure_cost / total_cost) * 100,
            "description": "Cloud services, hardware, and licenses"
        },
        "third_party_cost": {
            "amount": third_party_cost,
            "percentage": (third_party_cost / total_cost) * 100,
            "description": "External APIs and services"
        },
        "contingency": {
            "amount": contingency,
            "percentage": (contingency / total_cost) * 100,
            "description": "20% contingency buffer"
        },
        "total_cost": total_cost,
        "duration_weeks": duration_weeks,
        "team_size": team_size
    }
    
    return cost_breakdown


def create_resource_allocation(team_members: List[Dict[str, Any]], phases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create resource allocation plan for team members across project phases.
    
    Args:
        team_members: List of team member dictionaries with 'name', 'role', 'availability' keys
        phases: List of phase dictionaries with 'name', 'duration_weeks' keys
    
    Returns:
        Dictionary containing resource allocation plan
    """
    allocation = {
        "team_members": [],
        "phase_allocations": [],
        "utilization_summary": {}
    }
    
    # Process team members
    for member in team_members:
        member_info = {
            "name": member.get('name', 'Unknown'),
            "role": member.get('role', 'Developer'),
            "availability": member.get('availability', 1.0),  # Full-time equivalent
            "skills": member.get('skills', []),
            "total_hours": 0,
            "phases": []
        }
        allocation["team_members"].append(member_info)
    
    # Allocate resources to phases
    for i, phase in enumerate(phases):
        phase_name = phase.get('name', f'Phase {i+1}')
        duration_weeks = phase.get('duration_weeks', 2)
        required_roles = phase.get('required_roles', ['Developer'])
        
        phase_allocation = {
            "phase_name": phase_name,
            "duration_weeks": duration_weeks,
            "required_roles": required_roles,
            "allocated_members": []
        }
        
        # Allocate team members based on required roles
        for member in allocation["team_members"]:
            if member["role"] in required_roles:
                hours_allocated = member["availability"] * 40 * duration_weeks
                member["total_hours"] += hours_allocated
                
                member_allocation = {
                    "name": member["name"],
                    "role": member["role"],
                    "hours_allocated": hours_allocated,
                    "utilization": member["availability"]
                }
                phase_allocation["allocated_members"].append(member_allocation)
        
        allocation["phase_allocations"].append(phase_allocation)
    
    # Calculate utilization summary
    total_project_hours = sum(phase["duration_weeks"] * 40 for phase in phases)
    total_allocated_hours = sum(member["total_hours"] for member in allocation["team_members"])
    
    allocation["utilization_summary"] = {
        "total_project_hours": total_project_hours,
        "total_allocated_hours": total_allocated_hours,
        "utilization_rate": (total_allocated_hours / total_project_hours) * 100 if total_project_hours > 0 else 0
    }
    
    return allocation


def generate_risk_assessment(project_scope: str, timeline: Dict[str, Any], team_info: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a risk assessment for the project.
    
    Args:
        project_scope: Description of project scope
        timeline: Project timeline information
        team_info: Information about the team
    
    Returns:
        Dictionary containing risk assessment
    """
    risks = []
    
    # Timeline risks
    if timeline.get("total_duration_weeks", 0) > 20:
        risks.append({
            "category": "Timeline",
            "risk": "Long project duration",
            "impact": "High",
            "probability": "Medium",
            "mitigation": "Break into smaller phases with regular checkpoints"
        })
    
    # Team risks
    team_size = len(team_info)
    if team_size < 3:
        risks.append({
            "category": "Team",
            "risk": "Small team size",
            "impact": "Medium",
            "probability": "High",
            "mitigation": "Consider additional resources or extend timeline"
        })
    
    # Scope risks
    if len(project_scope) > 500:  # Simple heuristic for scope complexity
        risks.append({
            "category": "Scope",
            "risk": "Complex project scope",
            "impact": "High",
            "probability": "Medium",
            "mitigation": "Implement agile methodology with regular scope reviews"
        })
    
    # Technology risks
    risks.append({
        "category": "Technology",
        "risk": "Integration complexity",
        "impact": "Medium",
        "probability": "Medium",
        "mitigation": "Early prototyping and proof of concept"
    })
    
    # Calculate overall risk score
    risk_scores = {"Low": 1, "Medium": 2, "High": 3}
    total_risk_score = sum(risk_scores[risk["impact"]] * risk_scores[risk["probability"]] for risk in risks)
    max_possible_score = len(risks) * 9  # 3 * 3 for high impact and probability
    overall_risk_score = (total_risk_score / max_possible_score) * 100 if max_possible_score > 0 else 0
    
    risk_assessment = {
        "risks": risks,
        "overall_risk_score": overall_risk_score,
        "risk_level": "High" if overall_risk_score > 70 else "Medium" if overall_risk_score > 40 else "Low",
        "recommendations": [
            "Implement regular risk reviews",
            "Establish clear communication channels",
            "Create contingency plans for high-impact risks"
        ]
    }
    
    return risk_assessment


def create_quality_assurance_plan(project_phases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a quality assurance plan for the project.
    
    Args:
        project_phases: List of project phases with their characteristics
    
    Returns:
        Dictionary containing QA plan
    """
    qa_plan = {
        "testing_strategy": {
            "unit_testing": "Automated unit tests for all components",
            "integration_testing": "API and component integration testing",
            "system_testing": "End-to-end system validation",
            "user_acceptance_testing": "Client validation of requirements"
        },
        "quality_gates": [],
        "review_process": {
            "code_reviews": "Mandatory for all code changes",
            "design_reviews": "Before major architectural decisions",
            "security_reviews": "For all external integrations",
            "performance_reviews": "Before production deployment"
        },
        "metrics": {
            "code_coverage": "Target: 80% minimum",
            "defect_density": "Target: < 1 defect per 100 lines of code",
            "response_time": "Target: < 2 seconds for 95% of requests",
            "availability": "Target: 99.9% uptime"
        }
    }
    
    # Add quality gates for each phase
    for i, phase in enumerate(project_phases):
        phase_name = phase.get('name', f'Phase {i+1}')
        qa_plan["quality_gates"].append({
            "phase": phase_name,
            "criteria": [
                "All requirements implemented",
                "Unit tests passing",
                "Code review completed",
                "Documentation updated"
            ],
            "approval_required": True
        })
    
    return qa_plan
