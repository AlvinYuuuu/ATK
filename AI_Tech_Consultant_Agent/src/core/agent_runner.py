"""
Simple wrapper for ADK agents to provide an easy-to-use interface.
"""

import asyncio
from typing import Dict, Any, Optional
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import BaseAgent
from google.genai.types import Content


class SimpleAgentRunner:
    """
    A simple wrapper around ADK Runner to make agents easier to use.
    """
    
    def __init__(self, agent: BaseAgent, app_name: str = "ai_tech_consultant"):
        """
        Initialize the agent runner.
        
        Args:
            agent: The ADK agent to run
            app_name: The application name
        """
        self.agent = agent
        self.app_name = app_name
        self.session_service = InMemorySessionService()
        
        # Create default session before initializing runner
        asyncio.run(self._create_default_session())
        
        self.runner = Runner(
            app_name=app_name,
            agent=agent,
            session_service=self.session_service
        )
    
    async def _create_default_session(self):
        """Create the default session asynchronously."""
        try:
            await self.session_service.create_session(
                app_name=self.app_name,
                user_id="default_user",
                session_id="default_session"
            )
            print("Default session created successfully")
        except Exception as e:
            print(f"Error creating default session: {e}")
    
    async def _ensure_session_exists(self, user_id: str, session_id: str):
        """
        Ensure that a session exists for the given user_id and session_id.
        Creates the session if it doesn't exist.
        """
        try:
            # Try to get the session to see if it exists
            session = await self.session_service.get_session(
                app_name=self.app_name,
                user_id=user_id,
                session_id=session_id
            )
            print(f"Session found: {session_id}")
        except ValueError:
            # Session doesn't exist, create it
            print(f"Creating new session: {session_id}")
            await self.session_service.create_session(
                app_name=self.app_name,
                user_id=user_id,
                session_id=session_id
            )
            print(f"Session created successfully: {session_id}")
            # Verify session was created
            try:
                await self.session_service.get_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id
                )
                print(f"Session verification successful: {session_id}")
            except Exception as e:
                print(f"Session verification failed: {e}")
                raise
    
    def run(self, message: str, user_id: str = "default_user", session_id: str = "default_session") -> Dict[str, Any]:
        """
        Run the agent with a simple message.
        
        Args:
            message: The message to send to the agent
            user_id: The user ID for the session
            session_id: The session ID for the session
            
        Returns:
            Dictionary containing the agent's response
        """
        print(f"Starting run with session_id: {session_id}")
        # Ensure session exists before running
        asyncio.run(self._ensure_session_exists(user_id, session_id))
        
        # Create a simple text content
        content = Content(parts=[{"text": message}])
        print(f"Running agent with session_id: {session_id}")
        # Run the agent
        events = list(self.runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ))
        print(f"events: {events}")  
        # Extract the response from events
        response = self._extract_response_from_events(events)
        
        return {
            "status": "completed",
            "response": response,
            "events": events
        }
    
    def _extract_response_from_events(self, events) -> str:
        """Extract the response text from events."""
        response_parts = []
        
        for event in events:
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_parts.append(part.text)
        
        return "\n".join(response_parts) if response_parts else "No response generated"
    
    async def run_async(self, message: str, user_id: str = "default_user", session_id: str = "default_session") -> Dict[str, Any]:
        """
        Run the agent asynchronously.
        
        Args:
            message: The message to send to the agent
            user_id: The user ID for the session
            session_id: The session ID for the session
            
        Returns:
            Dictionary containing the agent's response
        """
        # Ensure session exists before running
        await self._ensure_session_exists(user_id, session_id)
        
        content = Content(parts=[{"text": message}])
        
        events = []
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            events.append(event)
        
        response = self._extract_response_from_events(events)
        
        return {
            "status": "completed",
            "response": response,
            "events": events
        }
    
    def close(self):
        """Close the runner."""
        asyncio.run(self.runner.close())


def create_simple_runner(agent: BaseAgent, app_name: str = "ai_tech_consultant") -> SimpleAgentRunner:
    """
    Create a simple agent runner for easy use.
    
    Args:
        agent: The ADK agent to wrap
        app_name: The application name
        
    Returns:
        SimpleAgentRunner instance
    """
    return SimpleAgentRunner(agent, app_name) 