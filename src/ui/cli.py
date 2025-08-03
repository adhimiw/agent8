"""
Command Line Interface for the Autonomous Personal Assistant.
Provides interactive CLI for user interaction.
"""

import asyncio
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt

from config.settings import Settings
from core.orchestrator import AssistantOrchestrator
from core.logger import get_logger

logger = get_logger("cli")
console = Console()

class CLIInterface:
    """Command line interface for the assistant."""
    
    def __init__(self, orchestrator: AssistantOrchestrator, settings: Settings):
        self.orchestrator = orchestrator
        self.settings = settings
        self.running = False
    
    async def start(self):
        """Start the CLI interface."""
        logger.info("Starting CLI interface")
        self.running = True
        
        console.print("💬 CLI interface ready. Type 'help' for commands.")
        
        while self.running:
            try:
                user_input = await asyncio.to_thread(
                    Prompt.ask, 
                    "[bold cyan]Assistant[/bold cyan]"
                )
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                else:
                    console.print(f"You said: {user_input}")
                    # Placeholder for command processing
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error("CLI error", error=str(e))
    
    async def shutdown(self):
        """Shutdown the CLI interface."""
        logger.info("Shutting down CLI interface")
        self.running = False
    
    def _show_help(self):
        """Show help information."""
        console.print("""
Available commands:
- help: Show this help message
- exit/quit/bye: Exit the assistant
        """)
