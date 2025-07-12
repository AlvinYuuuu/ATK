"""
Memory tools for agents to interact with the shared memory system.
"""

from typing import Dict, List, Any, Optional
from src.core.shared_memory import shared_memory

def search_memories(query: str, memory_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search for information in the shared memory system.
    
    Args:
        query: The search query to find relevant information
        memory_type: Optional filter for specific memory types (e.g., 'tender_analysis', 'solution_strategy')
    
    Returns:
        List of memory objects containing id, content, and metadata
    """
    return shared_memory.search_memories(query, memory_type)

def get_latest_memory(memory_type: str) -> Optional[Dict[str, Any]]:
    """
    Get the most recent memory of a specific type.
    
    Args:
        memory_type: The type of memory to retrieve (e.g., 'tender_analysis', 'solution_strategy')
    
    Returns:
        The latest memory object or None if not found
    """
    return shared_memory.get_latest_memory(memory_type)

def get_all_memories(memory_type: str) -> List[Dict[str, Any]]:
    """
    Get all memories of a specific type.
    
    Args:
        memory_type: The type of memory to retrieve
    
    Returns:
        List of all memory objects of the specified type
    """
    return shared_memory.get_all_memories(memory_type)

def store_tender_analysis(analysis: Dict[str, Any]) -> str:
    """
    Store tender analysis results in shared memory.
    
    Args:
        analysis: Dictionary containing the tender analysis data
    
    Returns:
        Memory ID of the stored analysis
    """
    return shared_memory.store_tender_analysis(analysis)

def store_solution_strategy(strategy: Dict[str, Any]) -> str:
    """
    Store solution strategy in shared memory.
    
    Args:
        strategy: Dictionary containing the solution strategy data
    
    Returns:
        Memory ID of the stored strategy
    """
    return shared_memory.store_solution_strategy(strategy)

def store_visualization(diagram_type: str, mermaid_code: str, description: str) -> str:
    """
    Store visualization diagram in shared memory.
    
    Args:
        diagram_type: Type of diagram (e.g., 'architecture', 'workflow', 'infrastructure')
        mermaid_code: Mermaid syntax code for the diagram
        description: Description of what the diagram shows
    
    Returns:
        Memory ID of the stored visualization
    """
    return shared_memory.store_visualization(diagram_type, mermaid_code, description)

def store_project_plan(plan: Dict[str, Any]) -> str:
    """
    Store project plan in shared memory.
    
    Args:
        plan: Dictionary containing the project plan data
    
    Returns:
        Memory ID of the stored plan
    """
    return shared_memory.store_project_plan(plan)

def store_technical_proposal(proposal: Dict[str, Any]) -> str:
    """
    Store technical proposal in shared memory.
    
    Args:
        proposal: Dictionary containing the technical proposal data
    
    Returns:
        Memory ID of the stored proposal
    """
    return shared_memory.store_technical_proposal(proposal)

def get_context_summary() -> str:
    """
    Get a summary of all stored information for context.
    
    Returns:
        Summary string of all available information
    """
    return shared_memory.get_context_summary()
