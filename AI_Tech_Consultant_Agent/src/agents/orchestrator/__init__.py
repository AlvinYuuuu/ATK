"""
This file defines the OrchestratorAgent, the master agent responsible for
coordinating tasks and delegating to specialist agents.
"""
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from src.agents.tender_analysis import TenderAnalysisAgent
from src.tools.memory_tools import search_memory
from .prompt import ORCHESTRATOR_PROMPT

OrchestratorAgent = LlmAgent(
    name="orchestrator_agent",
    model=LiteLlm(model="vertex_ai/gemini-2.5-flash"),
    description="A master agent that orchestrates the workflow by breaking down tasks and coordinating with other agents.",
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        AgentTool(agent=TenderAnalysisAgent),
        search_memory,
    ],
) 