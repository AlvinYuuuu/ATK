"""
Initializes and configures the main application runner and session service.
"""
from typing import Optional, Tuple
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from src.agents import OrchestratorAgent
from src.core.config import settings

# --- Global Services ---
_session_service: Optional[DatabaseSessionService] = None

def get_session_service() -> DatabaseSessionService:
    """
    Initializes and returns a singleton instance of the DatabaseSessionService.
    The service is configured using the DATABASE_URL from the application settings.
    """
    global _session_service
    if _session_service is None:
        if not settings.DATABASE_URL:
            raise ValueError(
                "DATABASE_URL is not set. Please check your .env file or environment variables."
            )
        print(f"Initializing session service with DB: {settings.DATABASE_URL}")
        _session_service = DatabaseSessionService(db_url=settings.DATABASE_URL)
    return _session_service


def initialize_runner_and_session(
    app_name: str,
) -> Tuple[Runner, DatabaseSessionService]:
    """
    Creates and configures the main ADK Runner and SessionService.

    Args:
        app_name: The name of the application.

    Returns:
        A tuple containing the configured Runner and SessionService instances.
    """
    session_service = get_session_service()
    runner = Runner(
        agent=OrchestratorAgent,
        app_name=app_name,
        session_service=session_service,
    )
    print(f"INFO: ADK Runner initialized for app: '{app_name}'.")
    return runner, session_service 