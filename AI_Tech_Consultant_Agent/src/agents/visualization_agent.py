"""
Visualization Agent - Creates diagrams and visualizations for technical proposals.
"""

from typing import Dict, List, Any
from google.adk.agents import Agent
from src.tools.memory_tools import (
    get_latest_memory,
    store_visualization,
    search_memories
)
from src.tools.diagram_tools import (
    generate_architecture_diagram,
    generate_workflow_diagram,
    generate_sequence_diagram,
    generate_er_diagram
)

def create_system_architecture_diagram() -> Dict[str, Any]:
    """
    Create a system architecture diagram based on the solution strategy.
    
    Returns:
        Dictionary containing the diagram information
    """
    # Get solution strategy from memory
    solution_strategy = get_latest_memory("solution_strategy")
    if not solution_strategy:
        return {"error": "No solution strategy found in memory"}
    
    strategy_data = solution_strategy.get("metadata", {}).get("data", {})
    architecture = strategy_data.get("technical_architecture", {})
    tech_stack = strategy_data.get("technology_stack", {})
    
    # Create components for the diagram
    components = []
    
    # Frontend components
    frontend_tech = tech_stack.get("frontend", {})
    components.append({
        "name": "Web Interface",
        "type": "frontend",
        "description": f"{frontend_tech.get('framework', 'React')} + {frontend_tech.get('ui_library', 'Material-UI')}"
    })
    components.append({
        "name": "Mobile App",
        "type": "frontend",
        "description": "Cross-platform mobile application"
    })
    
    # Backend components
    backend_tech = tech_stack.get("backend", {})
    components.append({
        "name": "API Gateway",
        "type": "backend",
        "description": f"{backend_tech.get('framework', 'Express')} API Gateway"
    })
    components.append({
        "name": "Authentication Service",
        "type": "backend",
        "description": "JWT-based authentication"
    })
    components.append({
        "name": "Business Logic",
        "type": "backend",
        "description": f"{backend_tech.get('runtime', 'Node.js')} microservices"
    })
    
    # Database components
    db_tech = tech_stack.get("database", {})
    components.append({
        "name": "Primary Database",
        "type": "database",
        "description": f"{db_tech.get('primary', 'PostgreSQL')} database"
    })
    components.append({
        "name": "Cache Layer",
        "type": "database",
        "description": f"{db_tech.get('cache', 'Redis')} caching"
    })
    
    # Infrastructure components
    infra_tech = tech_stack.get("infrastructure", {})
    components.append({
        "name": "Cloud Infrastructure",
        "type": "external",
        "description": f"{infra_tech.get('cloud_provider', 'AWS')} cloud services"
    })
    
    # Generate the diagram
    mermaid_code = generate_architecture_diagram(components, "system")
    
    # Store in memory
    memory_id = store_visualization("system_architecture", mermaid_code, 
                                   "System architecture diagram showing all components and their relationships")
    
    return {
        "diagram_type": "system_architecture",
        "mermaid_code": mermaid_code,
        "description": "System architecture diagram showing all components and their relationships",
        "memory_id": memory_id
    }

def create_infrastructure_diagram() -> Dict[str, Any]:
    """
    Create an infrastructure diagram showing deployment and infrastructure components.
    
    Returns:
        Dictionary containing the diagram information
    """
    # Get solution strategy from memory
    solution_strategy = get_latest_memory("solution_strategy")
    if not solution_strategy:
        return {"error": "No solution strategy found in memory"}
    
    strategy_data = solution_strategy.get("metadata", {}).get("data", {})
    tech_stack = strategy_data.get("technology_stack", {})
    infra_tech = tech_stack.get("infrastructure", {})
    
    # Create infrastructure components
    components = [
        {
            "name": "Load Balancer",
            "type": "load_balancer",
            "description": "Application Load Balancer"
        },
        {
            "name": "Web Server",
            "type": "web_server",
            "description": "Nginx reverse proxy"
        },
        {
            "name": "Application Server",
            "type": "application_server",
            "description": f"{infra_tech.get('containerization', 'Docker')} containers"
        },
        {
            "name": "Database Server",
            "type": "database",
            "description": "Managed database service"
        },
        {
            "name": "File Storage",
            "type": "storage",
            "description": "Object storage service"
        }
    ]
    
    # Generate the diagram
    mermaid_code = generate_architecture_diagram(components, "infrastructure")
    
    # Store in memory
    memory_id = store_visualization("infrastructure", mermaid_code,
                                   "Infrastructure diagram showing deployment architecture")
    
    return {
        "diagram_type": "infrastructure",
        "mermaid_code": mermaid_code,
        "description": "Infrastructure diagram showing deployment architecture",
        "memory_id": memory_id
    }

def create_data_flow_diagram() -> Dict[str, Any]:
    """
    Create a data flow diagram showing how data moves through the system.
    
    Returns:
        Dictionary containing the diagram information
    """
    # Create data flow components
    components = [
        {
            "name": "User Input",
            "type": "data_source",
            "description": "User interactions and form submissions"
        },
        {
            "name": "API Gateway",
            "type": "process",
            "description": "Request routing and authentication"
        },
        {
            "name": "Business Logic",
            "type": "process",
            "description": "Data processing and business rules"
        },
        {
            "name": "Database",
            "type": "data_store",
            "description": "Persistent data storage"
        },
        {
            "name": "Cache",
            "type": "data_store",
            "description": "Temporary data storage"
        },
        {
            "name": "User Interface",
            "type": "destination",
            "description": "Response to user"
        }
    ]
    
    # Generate the diagram
    mermaid_code = generate_architecture_diagram(components, "data_flow")
    
    # Store in memory
    memory_id = store_visualization("data_flow", mermaid_code,
                                   "Data flow diagram showing how data moves through the system")
    
    return {
        "diagram_type": "data_flow",
        "mermaid_code": mermaid_code,
        "description": "Data flow diagram showing how data moves through the system",
        "memory_id": memory_id
    }

def create_project_workflow_diagram() -> Dict[str, Any]:
    """
    Create a workflow diagram showing the project implementation process.
    
    Returns:
        Dictionary containing the diagram information
    """
    # Get solution strategy from memory
    solution_strategy = get_latest_memory("solution_strategy")
    if not solution_strategy:
        return {"error": "No solution strategy found in memory"}
    
    strategy_data = solution_strategy.get("metadata", {}).get("data", {})
    implementation = strategy_data.get("implementation_approach", {})
    phases = implementation.get("phases", [])
    
    # Create workflow steps
    workflow_steps = [
        {
            "name": "Project Start",
            "type": "start",
            "description": "Project initiation and kickoff"
        }
    ]
    
    # Add phases as workflow steps
    for phase in phases:
        workflow_steps.append({
            "name": phase.get("name", "Phase"),
            "type": "process",
            "description": f"{phase.get('duration', '2 weeks')} - {', '.join(phase.get('deliverables', []))}"
        })
    
    workflow_steps.append({
        "name": "Project Completion",
        "type": "end",
        "description": "Final delivery and handover"
    })
    
    # Generate the diagram
    mermaid_code = generate_workflow_diagram(workflow_steps)
    
    # Store in memory
    memory_id = store_visualization("project_workflow", mermaid_code,
                                   "Project workflow diagram showing implementation phases")
    
    return {
        "diagram_type": "project_workflow",
        "mermaid_code": mermaid_code,
        "description": "Project workflow diagram showing implementation phases",
        "memory_id": memory_id
    }

def create_sequence_diagram() -> Dict[str, Any]:
    """
    Create a sequence diagram showing system interactions.
    
    Returns:
        Dictionary containing the diagram information
    """
    # Define participants
    participants = ["User", "Frontend", "API Gateway", "Backend Service", "Database"]
    
    # Define interactions
    interactions = [
        {
            "from": "User",
            "to": "Frontend",
            "message": "Submit request",
            "type": "->"
        },
        {
            "from": "Frontend",
            "to": "API Gateway",
            "message": "API call",
            "type": "->"
        },
        {
            "from": "API Gateway",
            "to": "Backend Service",
            "message": "Process request",
            "type": "->"
        },
        {
            "from": "Backend Service",
            "to": "Database",
            "message": "Query data",
            "type": "->"
        },
        {
            "from": "Database",
            "to": "Backend Service",
            "message": "Return data",
            "type": "-->"
        },
        {
            "from": "Backend Service",
            "to": "API Gateway",
            "message": "Return response",
            "type": "-->"
        },
        {
            "from": "API Gateway",
            "to": "Frontend",
            "message": "Return data",
            "type": "-->"
        },
        {
            "from": "Frontend",
            "to": "User",
            "message": "Display result",
            "type": "-->"
        }
    ]
    
    # Generate the diagram
    mermaid_code = generate_sequence_diagram(participants, interactions)
    
    # Store in memory
    memory_id = store_visualization("sequence", mermaid_code,
                                   "Sequence diagram showing system interactions")
    
    return {
        "diagram_type": "sequence",
        "mermaid_code": mermaid_code,
        "description": "Sequence diagram showing system interactions",
        "memory_id": memory_id
    }

def create_database_er_diagram() -> Dict[str, Any]:
    """
    Create an entity-relationship diagram for the database design.
    
    Returns:
        Dictionary containing the diagram information
    """
    # Define entities for a typical system
    entities = [
        {
            "name": "User",
            "attributes": [
                {"name": "id", "type": "int", "constraint": "PK"},
                {"name": "email", "type": "varchar", "constraint": "UNIQUE"},
                {"name": "password_hash", "type": "varchar"},
                {"name": "created_at", "type": "timestamp"},
                {"name": "updated_at", "type": "timestamp"}
            ]
        },
        {
            "name": "Project",
            "attributes": [
                {"name": "id", "type": "int", "constraint": "PK"},
                {"name": "name", "type": "varchar"},
                {"name": "description", "type": "text"},
                {"name": "status", "type": "varchar"},
                {"name": "created_at", "type": "timestamp"}
            ]
        },
        {
            "name": "Task",
            "attributes": [
                {"name": "id", "type": "int", "constraint": "PK"},
                {"name": "title", "type": "varchar"},
                {"name": "description", "type": "text"},
                {"name": "status", "type": "varchar"},
                {"name": "priority", "type": "varchar"},
                {"name": "due_date", "type": "date"}
            ]
        }
    ]
    
    # Generate the diagram
    mermaid_code = generate_er_diagram(entities)
    
    # Store in memory
    memory_id = store_visualization("database_er", mermaid_code,
                                   "Database entity-relationship diagram")
    
    return {
        "diagram_type": "database_er",
        "mermaid_code": mermaid_code,
        "description": "Database entity-relationship diagram",
        "memory_id": memory_id
    }

def create_all_diagrams() -> Dict[str, Any]:
    """
    Create all necessary diagrams for the technical proposal.
    
    Returns:
        Dictionary containing all created diagrams
    """
    diagrams = {}
    
    # Create all diagrams
    try:
        diagrams["system_architecture"] = create_system_architecture_diagram()
    except Exception as e:
        diagrams["system_architecture"] = {"error": str(e)}
    
    try:
        diagrams["infrastructure"] = create_infrastructure_diagram()
    except Exception as e:
        diagrams["infrastructure"] = {"error": str(e)}
    
    try:
        diagrams["data_flow"] = create_data_flow_diagram()
    except Exception as e:
        diagrams["data_flow"] = {"error": str(e)}
    
    try:
        diagrams["project_workflow"] = create_project_workflow_diagram()
    except Exception as e:
        diagrams["project_workflow"] = {"error": str(e)}
    
    try:
        diagrams["sequence"] = create_sequence_diagram()
    except Exception as e:
        diagrams["sequence"] = {"error": str(e)}
    
    try:
        diagrams["database_er"] = create_database_er_diagram()
    except Exception as e:
        diagrams["database_er"] = {"error": str(e)}
    
    return {
        "total_diagrams": len(diagrams),
        "successful_diagrams": len([d for d in diagrams.values() if "error" not in d]),
        "diagrams": diagrams
    }

# Define the Visualization Agent
visualization_agent = Agent(
    name="VisualizationAgent",
    description="""
    A specialized agent that creates visual diagrams and charts for technical proposals.
    This agent is responsible for:
    
    1. Creating system architecture diagrams
    2. Generating infrastructure deployment diagrams
    3. Designing data flow diagrams
    4. Creating project workflow diagrams
    5. Generating sequence diagrams for system interactions
    6. Creating database entity-relationship diagrams
    7. Storing all diagrams in shared memory for the proposal
    
    The agent uses Mermaid syntax to create professional, clear visualizations
    that help stakeholders understand the technical solution.
    
    When creating diagrams:
    1. Review the solution strategy from shared memory
    2. Create diagrams that clearly communicate the technical solution
    3. Use appropriate diagram types for different aspects of the system
    4. Ensure diagrams are professional and easy to understand
    5. Store all diagrams in shared memory for the proposal
    6. Use Mermaid syntax for all diagram generation
    
    Focus on creating visualizations that help stakeholders understand:
    - System architecture and component relationships
    - Infrastructure and deployment structure
    - Data flow and system interactions
    - Project workflow and implementation phases
    - Database design and relationships
    
    Always ensure diagrams are accurate and reflect the actual solution design.
    """,
    tools=[
        create_system_architecture_diagram,
        create_infrastructure_diagram,
        create_data_flow_diagram,
        create_project_workflow_diagram,
        create_sequence_diagram,
        create_database_er_diagram,
        create_all_diagrams
    ]
)
