"""
Core module for the Autonomous Personal Assistant.
Contains the main orchestration logic and core components.
"""

from .orchestrator import AssistantOrchestrator
from .logger import setup_logging

__all__ = [
    "AssistantOrchestrator",
    "setup_logging"
]
