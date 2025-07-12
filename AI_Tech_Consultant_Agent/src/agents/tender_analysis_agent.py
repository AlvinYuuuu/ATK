"""
Tender Analysis Agent - Analyzes tender documents and extracts requirements.
"""

from typing import Dict, List, Any
from google.adk.agents import Agent
from src.tools.memory_tools import store_tender_analysis, search_memories
from src.tools.document_parsing_tools import (
    extract_text_from_file,
    extract_requirements_from_text,
    identify_missing_information,
    analyze_document_structure
)


def analyze_tender_document(file_path: str = None, text_content: str = None) -> Dict[str, Any]:
    """
    Analyze a tender document to extract requirements and key information.
    
    Args:
        file_path: Path to the tender document file
        text_content: Direct text content if file path is not provided
    
    Returns:
        Dictionary containing comprehensive tender analysis
    """
    # Extract text content
    if file_path:
        text_content = extract_text_from_file(file_path)
    elif not text_content:
        return {"error": "Either file_path or text_content must be provided"}
    
    # Perform comprehensive analysis
    requirements = extract_requirements_from_text(text_content)
    missing_info = identify_missing_information(text_content)
    structure_analysis = analyze_document_structure(text_content)
    
    # Create comprehensive analysis
    analysis = {
        "document_content": text_content[:1000] + "..." if len(text_content) > 1000 else text_content,
        "requirements": requirements,
        "missing_information": missing_info,
        "structure_analysis": structure_analysis,
        "analysis_timestamp": "2024-01-01T00:00:00Z",  # This would be dynamic in real implementation
        "confidence_score": _calculate_confidence_score(requirements, missing_info, structure_analysis)
    }
    
    # Store analysis in shared memory
    memory_id = store_tender_analysis(analysis)
    analysis["memory_id"] = memory_id
    
    return analysis

def _calculate_confidence_score(requirements: Dict[str, Any], missing_info: List[str], structure_analysis: Dict[str, Any]) -> float:
    """Calculate confidence score for the analysis."""
    score = 0.0
    
    # Base score from document structure
    score += structure_analysis.get("document_quality_score", 0) / 100.0 * 0.3
    
    # Score based on completeness of requirements
    total_requirements = sum(len(req) for req in requirements.values() if isinstance(req, list))
    if total_requirements > 0:
        score += min(total_requirements / 20.0, 1.0) * 0.4  # Cap at 20 requirements
    
    # Penalty for missing information
    missing_penalty = min(len(missing_info) * 0.1, 0.3)
    score -= missing_penalty
    
    return max(0.0, min(1.0, score))

# Define the Tender Analysis Agent
tender_analysis_agent = Agent(
    name="TenderAnalysisAgent",
    description="""
    A specialized agent that analyzes tender documents to extract requirements, 
    identify constraints, and understand client needs. This agent is responsible for:
    
    1. Parsing and extracting text from various document formats
    2. Identifying functional and non-functional requirements
    3. Extracting budget and timeline constraints
    4. Analyzing document structure and quality
    5. Identifying missing information that needs clarification
    6. Storing analysis results in shared memory for other agents
    
    The agent uses pattern matching and text analysis to systematically extract
    all relevant information from tender documents.
    
    When analyzing a tender document:
    1. Extract all requirements (functional, non-functional, technical constraints)
    2. Identify budget and timeline information
    3. Understand the client's background and project scope
    4. Analyze the document structure and quality
    5. Identify any missing information that needs clarification
    6. Store the complete analysis in shared memory
    
    Always be thorough and systematic in your analysis. If information is unclear
    or missing, make note of it so the Orchestrator can request clarification.
    
    Focus on extracting actionable information that will help the Solution Strategy
    Agent create an appropriate technical solution.
    """,
    tools=[analyze_tender_document]
)
