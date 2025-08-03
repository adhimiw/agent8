"""
Main entry point for the Autonomous Personal Assistant.
Initializes all components and starts the assistant.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import Optional

import uvloop
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import get_settings
from core.orchestrator import AssistantOrchestrator
from core.logger import setup_logging
from security.encryption import SecurityManager
from ui.cli import CLIInterface

console = Console()
logger = logging.getLogger(__name__)

class AutonomousAssistant:
    """Main application class for the Autonomous Personal Assistant."""
    
    def __init__(self):
        self.settings = get_settings()
        self.orchestrator: Optional[AssistantOrchestrator] = None
        self.cli: Optional[CLIInterface] = None
        self.security_manager: Optional[SecurityManager] = None
        self.running = False
        
    async def initialize(self):
        """Initialize all components of the assistant."""
        try:
            console.print(Panel.fit(
                Text("🤖 Autonomous Personal Assistant", style="bold blue"),
                subtitle="Initializing...",
                border_style="blue"
            ))
            
            # Setup logging
            setup_logging(self.settings)
            logger.info("Starting Autonomous Personal Assistant")
            
            # Initialize security manager
            console.print("🔐 Initializing security manager...")
            self.security_manager = SecurityManager(self.settings)
            await self.security_manager.initialize()
            
            # Initialize orchestrator
            console.print("🧠 Initializing AI orchestrator...")
            self.orchestrator = AssistantOrchestrator(self.settings)
            await self.orchestrator.initialize()
            
            # Initialize CLI interface
            console.print("💻 Initializing CLI interface...")
            self.cli = CLIInterface(self.orchestrator, self.settings)
            
            console.print("✅ Initialization complete!", style="bold green")
            
        except Exception as e:
            logger.error(f"Failed to initialize assistant: {e}")
            console.print(f"❌ Initialization failed: {e}", style="bold red")
            raise
    
    async def start(self):
        """Start the autonomous assistant."""
        if not self.orchestrator:
            raise RuntimeError("Assistant not initialized. Call initialize() first.")
        
        try:
            self.running = True
            
            # Display startup banner
            self._display_banner()
            
            # Start the orchestrator
            console.print("🚀 Starting autonomous operations...")
            await self.orchestrator.start()
            
            # Start CLI interface
            if self.cli:
                await self.cli.start()
            
            # Keep running until shutdown
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            console.print("\n🛑 Shutdown requested by user", style="yellow")
        except Exception as e:
            logger.error(f"Error during execution: {e}")
            console.print(f"❌ Error: {e}", style="bold red")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Gracefully shutdown the assistant."""
        console.print("🔄 Shutting down assistant...", style="yellow")
        self.running = False
        
        try:
            if self.orchestrator:
                await self.orchestrator.shutdown()
            
            if self.cli:
                await self.cli.shutdown()
            
            console.print("✅ Shutdown complete", style="bold green")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            console.print(f"❌ Shutdown error: {e}", style="bold red")
    
    def _display_banner(self):
        """Display the startup banner."""
        banner_text = Text()
        banner_text.append("🤖 ", style="bold blue")
        banner_text.append("Autonomous Personal Assistant", style="bold white")
        banner_text.append(" v1.0.0", style="dim white")
        
        status_text = Text()
        status_text.append("Status: ", style="bold")
        status_text.append("ACTIVE", style="bold green")
        
        mode_text = Text()
        mode_text.append("Mode: ", style="bold")
        if self.settings.app.autonomous_mode:
            mode_text.append("AUTONOMOUS", style="bold cyan")
        else:
            mode_text.append("MANUAL", style="bold yellow")
        
        features_text = Text()
        features_text.append("Features: ", style="bold")
        enabled_features = []
        if self.settings.features.enable_email_processing:
            enabled_features.append("Email")
        if self.settings.features.enable_calendar_integration:
            enabled_features.append("Calendar")
        if self.settings.features.enable_github_monitoring:
            enabled_features.append("GitHub")
        if self.settings.features.enable_slack_notifications:
            enabled_features.append("Slack")
        if self.settings.features.enable_notion_sync:
            enabled_features.append("Notion")
        
        features_text.append(", ".join(enabled_features), style="green")
        
        panel_content = Text()
        panel_content.append(banner_text)
        panel_content.append("\n\n")
        panel_content.append(status_text)
        panel_content.append("\n")
        panel_content.append(mode_text)
        panel_content.append("\n")
        panel_content.append(features_text)
        
        console.print(Panel(
            panel_content,
            title="🚀 System Status",
            border_style="green",
            padding=(1, 2)
        ))

def setup_signal_handlers(assistant: AutonomousAssistant):
    """Setup signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        console.print(f"\n🛑 Received signal {signum}, shutting down...", style="yellow")
        asyncio.create_task(assistant.shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """Main entry point."""
    # Use uvloop for better performance on Unix systems
    if sys.platform != "win32":
        uvloop.install()
    
    assistant = AutonomousAssistant()
    setup_signal_handlers(assistant)
    
    try:
        await assistant.initialize()
        await assistant.start()
    except Exception as e:
        console.print(f"❌ Fatal error: {e}", style="bold red")
        logger.exception("Fatal error in main")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="bold blue")
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="bold red")
        sys.exit(1)
