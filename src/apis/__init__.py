"""
API integration module for the Autonomous Personal Assistant.
Handles integration with Gemini, Perplexity, and other external APIs.
"""

from .gemini_client import GeminiClient
from .perplexity_client import PerplexityClient
from .api_manager import APIManager

__all__ = [
    "GeminiClient",
    "PerplexityClient", 
    "APIManager"
]
