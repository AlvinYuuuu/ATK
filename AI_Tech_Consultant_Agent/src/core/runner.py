"""
Provides a reusable function for running agent interactions.
"""

from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import BaseSessionService
from google.genai import types


async def run_agent_interaction(
    agent: BaseAgent,
    session_service: BaseSessionService,
    user_id: str,
    session_id: str,
    initial_message_text: str,
) -> str:
    """
    Runs a single interaction with a given agent using a provided session service.

    Args:
        agent: The ADK agent to run.
        session_service: The session service instance (e.g., DatabaseSessionService).
        user_id: The ID for the user.
        session_id: The ID for the session.
        initial_message_text: The initial text message from the user.

    Returns:
        The agent's final text response.
    """
    runner = Runner(
        agent=agent,
        app_name="ai-tech-consultant-agent",
        session_service=session_service,
    )

    initial_message = types.Content(
        role="user", parts=[types.Part(text=initial_message_text)]
    )

    print(f"\n>>> Sending message to {agent.name} (Session: {session_id})...")

    final_response = "Agent did not produce a final response."

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=initial_message
    ):
        if event.is_final_response() and event.content:
            final_response = event.content.parts[0].text
            break

    print(f"\n<<< Agent Response: {final_response}")
    return final_response 