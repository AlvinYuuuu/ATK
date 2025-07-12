"""
The OrchestratorAgent is the master agent that coordinates the entire
proposal generation workflow.
"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .prompt import INSTRUCTION

# For the initial setup, the Orchestrator is a simple LLM agent
# that can be used to test the basic functionality of the system.
# In later sprints, this will be replaced with a more complex
# workflow agent (e.g., SequentialAgent or a custom BaseAgent).
OrchestratorAgent = Agent(
    name="OrchestratorAgent",
    model=LiteLlm(model="vertex_ai/gemini-2.5-flash"), # Using a powerful model for coordination
    description="The master agent that coordinates the proposal generation process.",
    instruction=INSTRUCTION,
    # In the future, sub_agents and tools will be added here.
    # tools=[...],
    # sub_agents=[...],
) 