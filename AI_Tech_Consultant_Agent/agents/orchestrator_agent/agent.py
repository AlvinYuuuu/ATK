"""
Orchestrator Agent for ADK Web Interface
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.append(str(src_path))

from agents.orchestrator_agent import orchestrator_agent

# Export the agent for ADK web interface
root_agent = orchestrator_agent 