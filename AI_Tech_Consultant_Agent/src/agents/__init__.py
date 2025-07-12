"""
This package contains all the specialist agents for the system.

The __init__.py file is used to export the agents so they can be
easily imported elsewhere in the application.

Example:
from agents import OrchestratorAgent
"""

from .orchestrator import OrchestratorAgent

# As more agents are created in their own subdirectories,
# they should be exported here as well.
# from .tender_analysis import TenderAnalysisAgent
# from .solution_strategy import SolutionStrategyAgent
