"""
Main entry point for the AI Tech Consultant Agent application.
This script launches a Gradio web interface for interacting with the agent.
"""

import gradio as gr
import asyncio

from google.adk.sessions import DatabaseSessionService

# This imports all the necessary configurations and initializes them.
from src.core.config import settings
from src.core.runner import run_agent_interaction
from src.agents import OrchestratorAgent

# --- Persistent Session Setup ---
# Use a database session service for persistent memory across restarts.
session_service = DatabaseSessionService(db_url=settings.DATABASE_URL)
USER_ID = "gradio-user"
SESSION_ID = "persistent-chat-session" # A single, named session for the UI


async def ensure_session_exists():
    """Checks if the persistent session exists and creates it if not."""
    print(f"Ensuring session '{SESSION_ID}' exists for user '{USER_ID}'...")
    try:
        session = await session_service.get_session(
            app_name="ai-tech-consultant-agent",
            user_id=USER_ID,
            session_id=SESSION_ID
        )
        if session is None:
            raise ValueError("Session not found.")
        print("Session found.")
        print(session)
    except ValueError:
        print("Session not found. Creating a new one...")
        session =await session_service.create_session(
            app_name="ai-tech-consultant-agent",
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
        print("New session created.")
        print(session)

async def handle_chat_interaction(message, history):
    """
    Handles the user's message and file uploads from the Gradio interface.
    """
    text_input = message["text"]
    files = message["files"]

    if files:
        file_names = [f.name for f in files]
        ack_message = f"Received file(s): {', '.join(file_names)}. "
        text_input = ack_message + text_input

    response = await run_agent_interaction(
        agent=OrchestratorAgent,
        session_service=session_service,
        user_id=USER_ID,
        session_id=SESSION_ID,
        initial_message_text=text_input,
    )
    return response

# Build the Gradio interface
demo = gr.ChatInterface(
    fn=handle_chat_interaction,
    title="Genson - Votee's AI Technical Consultant",
    description="Upload a tender document and chat with the agent to generate a proposal.",
    multimodal=True,
    examples=[
        ["Hello, who are you?"],
        ["Can you help me with a proposal?"],
    ],
)

def startup():
    """A synchronous function to run async setup tasks before the server starts."""
    print("Running one-time startup tasks...")
    # Run the async function to ensure the session exists in the database
    asyncio.run(ensure_session_exists())
    print("Startup complete. Session is ready.")

if __name__ == "__main__":
    # Perform all necessary setup before launching the web server.
    startup()
    
    print("Launching Gradio interface... Go to http://127.0.0.1:7860")
    # demo.launch() is a blocking call that starts the server.
    demo.launch()
