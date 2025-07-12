"""
Diagram generation tools for creating Mermaid diagrams and visualizations.
"""

from typing import Dict, List, Any


def generate_architecture_diagram(components: List[Dict[str, Any]], diagram_type: str = "system") -> str:
    """
    Generate a Mermaid architecture diagram based on system components.
    
    Args:
        components: List of component dictionaries with 'name', 'type', 'description' keys
        diagram_type: Type of architecture diagram ('system', 'infrastructure', 'data_flow')
    
    Returns:
        Mermaid diagram code as string
    """
    if diagram_type == "system":
        return _generate_system_architecture(components)
    elif diagram_type == "infrastructure":
        return _generate_infrastructure_diagram(components)
    elif diagram_type == "data_flow":
        return _generate_data_flow_diagram(components)
    else:
        return _generate_system_architecture(components)

def _generate_system_architecture(components: List[Dict[str, Any]]) -> str:
    """Generate a system architecture diagram."""
    mermaid_code = ["graph TD"]
    
    # Add components
    for i, component in enumerate(components):
        name = component.get('name', f'Component_{i}')
        component_type = component.get('type', 'component')
        description = component.get('description', '')
        
        # Style based on component type
        if component_type == 'frontend':
            mermaid_code.append(f"    {name}[{name}<br/>{description}]")
        elif component_type == 'backend':
            mermaid_code.append(f"    {name}({name}<br/>{description})")
        elif component_type == 'database':
            mermaid_code.append(f"    {name}[({name}<br/>{description})]")
        elif component_type == 'external':
            mermaid_code.append(f"    {name}{{{name}<br/>{description}}}")
        else:
            mermaid_code.append(f"    {name}[{name}<br/>{description}]")
    
    # Add connections (simplified - could be enhanced with actual relationship data)
    for i in range(len(components) - 1):
        mermaid_code.append(f"    {components[i]['name']} --> {components[i+1]['name']}")
    
    return "\n".join(mermaid_code)

def _generate_infrastructure_diagram(components: List[Dict[str, Any]]) -> str:
    """Generate an infrastructure diagram."""
    mermaid_code = ["graph TD"]
    
    # Group components by infrastructure layer
    layers = {
        'load_balancer': [],
        'web_server': [],
        'application_server': [],
        'database': [],
        'storage': [],
        'external': []
    }
    
    for component in components:
        component_type = component.get('type', 'application_server')
        if component_type in layers:
            layers[component_type].append(component)
        else:
            layers['application_server'].append(component)
    
    # Add components by layer
    for layer_name, layer_components in layers.items():
        if layer_components:
            mermaid_code.append(f"    subgraph {layer_name.replace('_', ' ').title()}")
            for component in layer_components:
                name = component.get('name', 'Component')
                description = component.get('description', '')
                mermaid_code.append(f"        {name}[{name}<br/>{description}]")
            mermaid_code.append("    end")
    
    # Add connections between layers
    layer_order = ['load_balancer', 'web_server', 'application_server', 'database', 'storage']
    for i in range(len(layer_order) - 1):
        current_layer = layer_order[i]
        next_layer = layer_order[i + 1]
        if layers[current_layer] and layers[next_layer]:
            mermaid_code.append(f"    {layers[current_layer][0]['name']} --> {layers[next_layer][0]['name']}")
    
    return "\n".join(mermaid_code)

def _generate_data_flow_diagram(components: List[Dict[str, Any]]) -> str:
    """Generate a data flow diagram."""
    mermaid_code = ["graph LR"]
    
    # Add data sources, processes, and destinations
    for i, component in enumerate(components):
        name = component.get('name', f'Component_{i}')
        component_type = component.get('type', 'process')
        description = component.get('description', '')
        
        if component_type == 'data_source':
            mermaid_code.append(f"    {name}([{name}<br/>{description}])")
        elif component_type == 'process':
            mermaid_code.append(f"    {name}({name}<br/>{description})")
        elif component_type == 'data_store':
            mermaid_code.append(f"    {name}[({name}<br/>{description})]")
        elif component_type == 'destination':
            mermaid_code.append(f"    {name}{{{name}<br/>{description}}}")
        else:
            mermaid_code.append(f"    {name}({name}<br/>{description})")
    
    # Add data flow connections
    for i in range(len(components) - 1):
        mermaid_code.append(f"    {components[i]['name']} -->|data| {components[i+1]['name']}")
    
    return "\n".join(mermaid_code)


def generate_workflow_diagram(workflow_steps: List[Dict[str, Any]]) -> str:
    """
    Generate a Mermaid workflow diagram.
    
    Args:
        workflow_steps: List of workflow step dictionaries with 'name', 'type', 'description' keys
    
    Returns:
        Mermaid workflow diagram code as string
    """
    mermaid_code = ["graph TD"]
    
    for i, step in enumerate(workflow_steps):
        name = step.get('name', f'Step_{i}')
        step_type = step.get('type', 'process')
        description = step.get('description', '')
        
        if step_type == 'start':
            mermaid_code.append(f"    {name}([{name}<br/>{description}])")
        elif step_type == 'decision':
            mermaid_code.append(f"    {name}{{{name}<br/>{description}}}")
        elif step_type == 'end':
            mermaid_code.append(f"    {name}([{name}<br/>{description}])")
        else:
            mermaid_code.append(f"    {name}({name}<br/>{description})")
    
    # Add connections
    for i in range(len(workflow_steps) - 1):
        current_step = workflow_steps[i]
        next_step = workflow_steps[i + 1]
        
        if current_step.get('type') == 'decision':
            # For decisions, we might want to add conditional labels
            mermaid_code.append(f"    {current_step['name']} -->|Yes| {next_step['name']}")
        else:
            mermaid_code.append(f"    {current_step['name']} --> {next_step['name']}")
    
    return "\n".join(mermaid_code)


def generate_sequence_diagram(participants: List[str], interactions: List[Dict[str, Any]]) -> str:
    """
    Generate a Mermaid sequence diagram.
    
    Args:
        participants: List of participant names
        interactions: List of interaction dictionaries with 'from', 'to', 'message' keys
    
    Returns:
        Mermaid sequence diagram code as string
    """
    mermaid_code = ["sequenceDiagram"]
    
    # Add participants
    for participant in participants:
        mermaid_code.append(f"    participant {participant}")
    
    # Add interactions
    for interaction in interactions:
        from_participant = interaction.get('from', participants[0])
        to_participant = interaction.get('to', participants[1])
        message = interaction.get('message', '')
        interaction_type = interaction.get('type', '->')
        
        if interaction_type == '->':
            mermaid_code.append(f"    {from_participant}->>{to_participant}: {message}")
        elif interaction_type == '-->':
            mermaid_code.append(f"    {from_participant}-->{to_participant}: {message}")
        elif interaction_type == '->>+':
            mermaid_code.append(f"    {from_participant}->>+{to_participant}: {message}")
        elif interaction_type == '->>-':
            mermaid_code.append(f"    {from_participant}->>-{to_participant}: {message}")
        else:
            mermaid_code.append(f"    {from_participant}->>{to_participant}: {message}")
    
    return "\n".join(mermaid_code)


def generate_er_diagram(entities: List[Dict[str, Any]]) -> str:
    """
    Generate a Mermaid entity-relationship diagram.
    
    Args:
        entities: List of entity dictionaries with 'name', 'attributes' keys
    
    Returns:
        Mermaid ER diagram code as string
    """
    mermaid_code = ["erDiagram"]
    
    for entity in entities:
        name = entity.get('name', 'Entity')
        attributes = entity.get('attributes', [])
        
        # Add entity definition
        entity_def = f"    {name} {{"
        for attr in attributes:
            attr_name = attr.get('name', 'attribute')
            attr_type = attr.get('type', 'string')
            attr_constraint = attr.get('constraint', '')
            
            if attr_constraint:
                entity_def += f"\n        {attr_type} {attr_name} {attr_constraint}"
            else:
                entity_def += f"\n        {attr_type} {attr_name}"
        
        entity_def += "\n    }"
        mermaid_code.append(entity_def)
    
    # Add relationships (simplified - could be enhanced with actual relationship data)
    for i in range(len(entities) - 1):
        mermaid_code.append(f"    {entities[i]['name']} ||--o{{ {entities[i+1]['name']} : relates")
    
    return "\n".join(mermaid_code)
