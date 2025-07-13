"""
Solution Strategy Agent - Designs technical solutions based on tender analysis.
"""

from typing import Dict, List, Any
from google.adk.agents import Agent
from litellm import LiteLLM
from src.tools.memory_tools import (
    get_latest_memory, 
    store_solution_strategy, 
    search_memories
)


def design_solution_strategy(tender_analysis_id: str = None) -> Dict[str, Any]:
    """
    Design a comprehensive solution strategy based on tender analysis.
    
    Args:
        tender_analysis_id: Memory ID of the tender analysis (optional, will use latest if not provided)
    
    Returns:
        Dictionary containing the solution strategy
    """
    # Get tender analysis from memory
    if tender_analysis_id:
        tender_analysis = get_latest_memory("tender_analysis")
    else:
        tender_analysis = get_latest_memory("tender_analysis")
    
    if not tender_analysis:
        return {"error": "No tender analysis found in memory"}
    
    analysis_data = tender_analysis.get("metadata", {}).get("data", {})
    requirements = analysis_data.get("requirements", {})
    
    # Design solution strategy
    strategy = {
        "solution_overview": _create_solution_overview(requirements),
        "technical_architecture": _design_technical_architecture(requirements),
        "technology_stack": _select_technology_stack(requirements),
        "implementation_approach": _define_implementation_approach(requirements),
        "risk_mitigation": _identify_risks_and_mitigation(requirements),
        "cost_estimates": _estimate_solution_costs(requirements),
        "timeline_estimate": _estimate_implementation_timeline(requirements),
        "success_metrics": _define_success_metrics(requirements),
        "assumptions": _document_assumptions(requirements)
    }
    
    # Store strategy in shared memory
    memory_id = store_solution_strategy(strategy)
    strategy["memory_id"] = memory_id
    
    return strategy

def _create_solution_overview(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Create a high-level solution overview."""
    functional_reqs = requirements.get("functional_requirements", [])
    project_scope = requirements.get("project_scope", "")
    
    overview = {
        "summary": f"Comprehensive solution addressing {len(functional_reqs)} functional requirements",
        "key_features": functional_reqs[:5],  # Top 5 features
        "business_value": "Improved efficiency, cost reduction, and enhanced user experience",
        "differentiators": [
            "Modern, scalable architecture",
            "Integration with existing systems",
            "Comprehensive security measures",
            "User-friendly interface design"
        ]
    }
    
    return overview

def _design_technical_architecture(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Design the technical architecture."""
    tech_constraints = requirements.get("technical_constraints", [])
    
    architecture = {
        "layers": {
            "presentation_layer": {
                "components": ["Web Interface", "Mobile App", "Admin Dashboard"],
                "technologies": ["React", "React Native", "Material-UI"]
            },
            "business_logic_layer": {
                "components": ["API Gateway", "Microservices", "Authentication Service"],
                "technologies": ["Node.js", "Python", "JWT"]
            },
            "data_layer": {
                "components": ["Primary Database", "Cache", "File Storage"],
                "technologies": ["PostgreSQL", "Redis", "AWS S3"]
            }
        },
        "integration_points": [
            "REST APIs for external integrations",
            "Webhook support for real-time updates",
            "Database connectors for legacy systems"
        ],
        "security_measures": [
            "OAuth 2.0 authentication",
            "Data encryption at rest and in transit",
            "Regular security audits",
            "Compliance with industry standards"
        ]
    }
    
    return architecture

def _select_technology_stack(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Select appropriate technology stack."""
    tech_constraints = requirements.get("technical_constraints", [])
    
    # Base technology stack
    stack = {
        "frontend": {
            "framework": "React.js",
            "ui_library": "Material-UI",
            "state_management": "Redux Toolkit",
            "build_tool": "Vite"
        },
        "backend": {
            "runtime": "Node.js",
            "framework": "Express.js",
            "language": "TypeScript",
            "api_design": "REST + GraphQL"
        },
        "database": {
            "primary": "PostgreSQL",
            "cache": "Redis",
            "orm": "Prisma"
        },
        "infrastructure": {
            "cloud_provider": "AWS",
            "containerization": "Docker",
            "orchestration": "Kubernetes",
            "ci_cd": "GitHub Actions"
        },
        "monitoring": {
            "logging": "ELK Stack",
            "metrics": "Prometheus + Grafana",
            "tracing": "Jaeger"
        }
    }
    
    # Adjust based on constraints
    for constraint in tech_constraints:
        constraint_lower = constraint.lower()
        if "python" in constraint_lower:
            stack["backend"]["runtime"] = "Python"
            stack["backend"]["framework"] = "FastAPI"
        elif "java" in constraint_lower:
            stack["backend"]["runtime"] = "Java"
            stack["backend"]["framework"] = "Spring Boot"
        elif "azure" in constraint_lower:
            stack["infrastructure"]["cloud_provider"] = "Azure"
        elif "gcp" in constraint_lower:
            stack["infrastructure"]["cloud_provider"] = "Google Cloud Platform"
    
    return stack

def _define_implementation_approach(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Define the implementation approach."""
    approach = {
        "methodology": "Agile with Scrum",
        "phases": [
            {
                "name": "Discovery & Planning",
                "duration": "2-3 weeks",
                "deliverables": ["Detailed requirements", "Technical design", "Project plan"]
            },
            {
                "name": "Development Phase 1",
                "duration": "4-6 weeks",
                "deliverables": ["Core functionality", "Basic UI", "API endpoints"]
            },
            {
                "name": "Development Phase 2",
                "duration": "4-6 weeks",
                "deliverables": ["Advanced features", "Integration", "Testing"]
            },
            {
                "name": "Testing & Deployment",
                "duration": "2-3 weeks",
                "deliverables": ["QA testing", "Production deployment", "Documentation"]
            }
        ],
        "team_structure": {
            "project_manager": 1,
            "tech_lead": 1,
            "frontend_developers": 2,
            "backend_developers": 2,
            "devops_engineer": 1,
            "qa_engineer": 1
        }
    }
    
    return approach

def _identify_risks_and_mitigation(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Identify risks and mitigation strategies."""
    risks = [
        {
            "risk": "Scope creep during development",
            "impact": "Medium",
            "probability": "Medium",
            "mitigation": "Regular scope reviews, change control process"
        },
        {
            "risk": "Integration challenges with existing systems",
            "impact": "High",
            "probability": "Medium",
            "mitigation": "Early integration testing, proof of concept"
        },
        {
            "risk": "Performance issues under load",
            "impact": "High",
            "probability": "Low",
            "mitigation": "Load testing, performance monitoring, scaling strategy"
        },
        {
            "risk": "Security vulnerabilities",
            "impact": "High",
            "probability": "Low",
            "mitigation": "Security reviews, penetration testing, secure coding practices"
        }
    ]
    
    return {"risks": risks}

def _estimate_solution_costs(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Estimate solution costs."""
    budget_constraints = requirements.get("budget_constraints", [])
    
    # Base cost estimates
    costs = {
        "development": {
            "team_costs": 120000,  # 6 people * 10 weeks * $2000/week
            "description": "Development team costs"
        },
        "infrastructure": {
            "cloud_services": 5000,  # Monthly costs for 3 months
            "description": "Cloud infrastructure and services"
        },
        "third_party": {
            "licenses": 3000,  # Software licenses and tools
            "description": "Third-party software and services"
        },
        "contingency": {
            "amount": 25600,  # 20% contingency
            "description": "Contingency buffer"
        }
    }
    
    total_cost = sum(cost.get("amount", cost) for cost in costs.values())
    costs["total"] = total_cost
    
    return costs

def _estimate_implementation_timeline(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Estimate implementation timeline."""
    timeline_constraints = requirements.get("timeline_constraints", [])
    
    timeline = {
        "total_duration": "14-18 weeks",
        "phases": [
            {"name": "Discovery & Planning", "duration": "2-3 weeks"},
            {"name": "Development Phase 1", "duration": "4-6 weeks"},
            {"name": "Development Phase 2", "duration": "4-6 weeks"},
            {"name": "Testing & Deployment", "duration": "2-3 weeks"}
        ],
        "milestones": [
            {"week": 3, "milestone": "Requirements finalized and approved"},
            {"week": 9, "milestone": "Core functionality completed"},
            {"week": 15, "milestone": "All features completed and tested"},
            {"week": 18, "milestone": "Production deployment"}
        ]
    }
    
    return timeline

def _define_success_metrics(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Define success metrics for the solution."""
    metrics = {
        "technical_metrics": [
            "System uptime: 99.9%",
            "Response time: < 2 seconds",
            "Page load time: < 3 seconds",
            "API response time: < 500ms"
        ],
        "business_metrics": [
            "User adoption rate: > 80%",
            "Task completion rate: > 90%",
            "User satisfaction score: > 4.5/5",
            "Reduction in manual processes: > 50%"
        ],
        "project_metrics": [
            "On-time delivery",
            "Within budget",
            "All requirements met",
            "Zero critical bugs in production"
        ]
    }
    
    return metrics

def _document_assumptions(requirements: Dict[str, Any]) -> List[str]:
    """Document assumptions made during solution design."""
    assumptions = [
        "Client has existing IT infrastructure and team",
        "Client will provide necessary access to existing systems",
        "Client will participate in regular review meetings",
        "Client will provide timely feedback and approvals",
        "No major regulatory changes during implementation",
        "Team availability and skills as specified",
        "Third-party services and APIs remain available"
    ]
    
    return assumptions

# Define the Solution Strategy Agent
solution_strategy_agent = Agent(
    name="SolutionStrategyAgent",
    description="""
    A specialized agent that designs comprehensive technical solutions based on 
    tender analysis. This agent is responsible for:
    
    1. Creating solution overview and business value proposition
    2. Designing technical architecture and system components
    3. Selecting appropriate technology stack
    4. Defining implementation approach and methodology
    5. Identifying risks and mitigation strategies
    6. Estimating costs and timeline
    7. Defining success metrics
    8. Documenting assumptions and constraints
    
    The agent leverages Votee's technology stack and partnerships to create
    innovative, cost-effective solutions that meet client requirements.
    
    When designing a solution:
    1. Review the tender analysis from shared memory
    2. Create a solution that addresses all requirements
    3. Consider Votee's technology stack and partnerships
    4. Design scalable and maintainable architecture
    5. Provide realistic cost and timeline estimates
    6. Identify potential risks and mitigation strategies
    7. Define clear success metrics
    8. Document all assumptions made
    
    Focus on creating innovative solutions that provide clear business value
    while being technically sound and feasible to implement.
    
    Always consider the client's constraints and preferences when making
    technical decisions.
    """,
    model="gemini-2.0-flash-exp",
    tools=[design_solution_strategy, search_memories]
)
