"""
Main entry point for the AI Tech Consultant Agent application.
This script launches a Gradio web interface for interacting with the agent,
with support for multiple, persistent chat sessions.
"""

import argparse
import asyncio
import uuid
from typing import List, Tuple
import os

import gradio as gr
from google.adk.events import Event, EventActions
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types as genai_types

from src.agents import OrchestratorAgent
from src.agents.runner import initialize_runner_and_session


# --- Constants & Services ---
APP_NAME = "ai-tech-consultant-agent"
USER_ID = "gradio-user"  # In a real multi-user app, this would be dynamic.

# The runner and session service are initialized together.
runner, session_service = initialize_runner_and_session(app_name=APP_NAME)


# --- Backend Session Management Functions ---

async def get_session_list() -> List[str]:
    """Fetches the list of existing session IDs, sorted by last update time."""
    print("Fetching session list...")
    try:
        response = await session_service.list_sessions(
            app_name=APP_NAME, user_id=USER_ID
        )
        # Sort sessions by last_update_time, most recent first.
        sorted_sessions = sorted(
            response.sessions, key=lambda s: s.last_update_time, reverse=True
        )
        session_ids = [s.id for s in sorted_sessions]
        print(f"Found sessions: {session_ids}")
        return session_ids
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return []


async def load_chat_history(session_id: str) -> List[Tuple[str | None, str | None]]:
    """Loads and formats the chat history for a given session."""
    if not session_id:
        return []

    print(f"Loading chat history for session: {session_id}")
    try:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except Exception as e:
        print(f"Error loading session {session_id}: {e}")
        # Return empty history but maybe log the error more formally
        return []

    history = []
    if session and session.events:
        user_message = None
        # The ADK saves user and model turns as separate events. We need to pair them up.
        for event in session.events:
            # Simple text content is in event.content.parts[0].text
            content_text = None
            if event.content and event.content.parts:
                content_text = event.content.parts[0].text

            if event.author == "user":
                user_message = content_text
            elif event.author == "model" and user_message is not None:
                model_response = content_text
                history.append((user_message, model_response))
                user_message = None  # Reset for the next pair

    print(f"Loaded history with {len(history)} pairs.")
    return history


# --- Gradio UI Event Handlers ---

async def handle_chat_interaction(text_input, file_objs, history, session_id):
    """
    Handles a single user-bot interaction, including file uploads.
    This function is a generator to allow for streaming responses.
    """
    # --- Immediate UI update ---
    # Show the user's message and clear the input fields right away.
    if file_objs:
        file_paths = [f.name for f in file_objs]
        file_names = [os.path.basename(p) for p in file_paths]
        display_message = (
            f"Received files: `{file_names}`.\\n\\n" f"User message: {text_input}"
        )
        history.append((display_message, "Analyzing..."))
    else:
        history.append((text_input, "Analyzing..."))

    # Yield the updated history and clear inputs. The `None`s are placeholders for outputs
    # we aren't updating at this exact moment.
    yield history, session_id, gr.update(value=""), gr.update(value=None)
    # -------------------------

    # --- Prepare message for the agent, including context ---
    context_parts = [f"The user's session_id is: {session_id}."]
    if file_objs:
        file_paths = [f.name for f in file_objs]
        # Format as a simple comma-separated string for easier parsing by the LLM
        context_parts.append(f"Files have been uploaded and are available at paths: {','.join(file_paths)}")
    
    context_block = f"---CONTEXT--- {' '.join(context_parts)}"
    final_message_for_agent = f"{text_input}\\n\\n{context_block}"
    
    print(f"Message being sent to agent: {final_message_for_agent}")
    
    content_for_agent = genai_types.Content(
        role="user", parts=[genai_types.Part(text=final_message_for_agent)]
    )

    final_response_text = None
    try:
        # Execute the agent
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content_for_agent,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
        
        if final_response_text is None:
            final_response_text = "Error: Agent did not produce a final response."

    except Exception as e:
        print(f"An error occurred during agent execution: {e}")
        final_response_text = f"An unexpected error occurred: {e}"

    history[-1] = (history[-1][0], final_response_text)
    
    # --- Final UI update ---
    # Yield the final history and None for the other outputs that don't need changing.
    yield history, session_id, None, None
    # ---------------------


async def create_new_chat_session():
    """Creates a new session, saves it, and updates the UI."""
    new_session_id = str(uuid.uuid4())
    print(f"Creating and saving new chat session: {new_session_id}")

    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=new_session_id
    )

    all_sessions = await get_session_list()
    return (
        [],  # Clear chatbot
        new_session_id,  # Update session_id state
        gr.update(choices=all_sessions, value=new_session_id),  # Update dropdown
        gr.update(interactive=True, placeholder="Type your message..."), # Enable text input
        gr.update(interactive=True), # Enable file uploader
        gr.update(interactive=True), # Enable send button
    )


async def switch_active_session(evt: gr.SelectData):
    """Switches the active session upon user selection from dropdown."""
    session_id = evt.value
    if not session_id:
        return (
            [],
            None,
            gr.update(interactive=False, placeholder="Select a chat to begin"),
            gr.update(interactive=False),
            gr.update(interactive=False),
        )

    print(f"Switching to session: {session_id}")
    history = await load_chat_history(session_id)
    return (
        history,
        session_id,
        gr.update(interactive=True, placeholder="Type your message..."),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


async def on_ui_load():
    """Populates the session dropdown when the UI first loads."""
    sessions = await get_session_list()
    return gr.update(choices=sessions)


# --- Gradio UI Layout ---

with gr.Blocks(
    theme=gr.themes.Default(primary_hue="blue"),
    title="Genson - AI Technical Consultant",
) as demo:
    session_id_state = gr.State(None)

    gr.Markdown("# Genson - Votee's AI Technical Consultant")
    gr.Markdown(
        "Start a `New Chat` or select a previous conversation from the dropdown to continue."
    )

    with gr.Row():
        session_dropdown = gr.Dropdown(
            label="Previous Sessions",
            scale=3,
            interactive=True,
        )
        new_chat_button = gr.Button("➕ New Chat", scale=1)

    chatbot = gr.Chatbot(
        label="Chat History",
        height=500,
        avatar_images=(None, "https://i.imgur.com/TdcY2x3.png"),
    )

    with gr.Row(equal_height=True):
        chat_input_text = gr.Textbox(
        show_label=False,
        placeholder="Select a chat or start a new one to begin.",
            scale=4,
            interactive=False,
        )
        file_uploader = gr.File(
            label="Upload Document(s)",
            file_types=[".pdf", ".doc", ".docx"],
            file_count="multiple",
            scale=1,
            interactive=False,
        )

    submit_button = gr.Button("Send", variant="primary", interactive=False, scale=1)


    # --- Wire UI Components to Event Handlers ---

    # When the UI loads, populate the session dropdown
    demo.load(on_ui_load, None, session_dropdown)

    # When the "New Chat" button is clicked
    new_chat_button.click(
        create_new_chat_session,
        None,
        [chatbot, session_id_state, session_dropdown, chat_input_text, file_uploader, submit_button],
    )

    # When a session is selected from the dropdown
    session_dropdown.select(
        switch_active_session, None, [chatbot, session_id_state, chat_input_text, file_uploader, submit_button]
    )

    # Define the list of outputs for the chat handler
    outputs = [chatbot, session_id_state, chat_input_text, file_uploader]

    # When the user submits a message (via button or enter)
    submit_button.click(
        handle_chat_interaction,
        [chat_input_text, file_uploader, chatbot, session_id_state],
        outputs,
    )
    chat_input_text.submit(
        handle_chat_interaction,
        [chat_input_text, file_uploader, chatbot, session_id_state],
        outputs,
    )
    
    # After submission, clear the inputs
    submit_handler = submit_button.click(
        lambda: (gr.update(value=""), gr.update(value=None)), None, [chat_input_text, file_uploader]
    )


def launch_app():
    """Launches the Gradio web interface."""
    demo.launch()


if __name__ == "__main__":
    print("Launching Gradio interface...")
    # The `main()` function is for command-line execution.
    # We call `launch_app()` here to start the web UI.
    launch_app()
