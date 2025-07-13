"""
This file defines the TenderAnalysisAgent, a specialist agent responsible for
parsing and analyzing tender documents.
"""
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from src.tools.document_parsing_tools import parse_documents
from src.tools.memory_tools import save_memory
from .prompt import TENDER_ANALYSIS_PROMPT


TenderAnalysisAgent = LlmAgent(
    name="tender_analysis_agent",
    model=LiteLlm(model="vertex_ai/gemini-2.5-flash"),
    description="A specialist agent that analyzes the content of a tender document and extracts key information.",
    instruction=TENDER_ANALYSIS_PROMPT,
    tools=[
        save_memory,
        parse_documents,
    ],
) 