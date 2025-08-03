#!/usr/bin/env python3
"""
Setup script for the Autonomous Personal Assistant.
Configures API keys, initializes databases, and sets up the environment.
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config.settings import get_settings
from apis.gemini_client import GeminiClient
from apis.perplexity_client import PerplexityClient

console = Console()

class SetupManager:
    """Manages the setup process for the autonomous assistant."""
    
    def __init__(self):
        self.env_file = Path(__file__).parent.parent / ".env"
        self.env_example = Path(__file__).parent.parent / ".env.example"
        self.config = {}
    
    def run_setup(self):
        """Run the complete setup process."""
        console.print(Panel.fit(
            Text("🤖 Autonomous Personal Assistant Setup", style="bold blue"),
            subtitle="Let's configure your AI assistant",
            border_style="blue"
        ))
        
        try:
            # Check if .env exists
            if self.env_file.exists():
                if not Confirm.ask("🔄 .env file already exists. Do you want to reconfigure?"):
                    console.print("✅ Setup cancelled. Using existing configuration.")
                    return
            
            # Copy from example if needed
            if not self.env_file.exists() and self.env_example.exists():
                console.print("📋 Creating .env file from template...")
                self._copy_env_template()
            
            # Configure API keys
            self._configure_api_keys()
            
            # Test API connections
            if Confirm.ask("🧪 Would you like to test API connections?"):
                asyncio.run(self._test_api_connections())
            
            # Setup directories
            self._setup_directories()
            
            # Display summary
            self._display_setup_summary()
            
            console.print("🎉 Setup completed successfully!", style="bold green")
            console.print("You can now run: python src/main.py", style="cyan")
            
        except KeyboardInterrupt:
            console.print("\n❌ Setup cancelled by user", style="yellow")
        except Exception as e:
            console.print(f"❌ Setup failed: {e}", style="bold red")
            raise
    
    def _copy_env_template(self):
        """Copy .env.example to .env."""
        try:
            with open(self.env_example, 'r') as src:
                content = src.read()
            
            with open(self.env_file, 'w') as dst:
                dst.write(content)
            
            console.print("✅ Created .env file from template")
            
        except Exception as e:
            console.print(f"❌ Failed to create .env file: {e}", style="red")
            raise
    
    def _configure_api_keys(self):
        """Configure API keys interactively."""
        console.print("\n🔑 API Key Configuration", style="bold yellow")
        console.print("Please provide your API keys. You can get them from:")
        console.print("• Gemini API: https://ai.google.dev/")
        console.print("• Perplexity API: https://www.perplexity.ai/settings/api")
        
        # Read current .env file
        current_config = self._read_env_file()
        
        # Configure Gemini API
        console.print("\n🧠 Gemini API Configuration", style="bold cyan")
        gemini_key = Prompt.ask(
            "Enter your Gemini API key",
            default=current_config.get("GEMINI_API_KEY", ""),
            password=True
        )
        
        if gemini_key and gemini_key != current_config.get("GEMINI_API_KEY", ""):
            self.config["GEMINI_API_KEY"] = gemini_key
        
        # Configure Perplexity API
        console.print("\n🔍 Perplexity API Configuration", style="bold cyan")
        perplexity_key = Prompt.ask(
            "Enter your Perplexity API key",
            default=current_config.get("PERPLEXITY_API_KEY", ""),
            password=True
        )
        
        if perplexity_key and perplexity_key != current_config.get("PERPLEXITY_API_KEY", ""):
            self.config["PERPLEXITY_API_KEY"] = perplexity_key
        
        # Update .env file
        if self.config:
            self._update_env_file(self.config)
            console.print("✅ API keys configured successfully")
    
    def _read_env_file(self) -> Dict[str, str]:
        """Read current .env file."""
        config = {}
        
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        
        return config
    
    def _update_env_file(self, updates: Dict[str, str]):
        """Update .env file with new values."""
        # Read current content
        lines = []
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                lines = f.readlines()
        
        # Update existing keys or add new ones
        updated_keys = set()
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and '=' in stripped:
                key = stripped.split('=', 1)[0].strip()
                if key in updates:
                    lines[i] = f"{key}={updates[key]}\n"
                    updated_keys.add(key)
        
        # Add new keys that weren't found
        for key, value in updates.items():
            if key not in updated_keys:
                lines.append(f"{key}={value}\n")
        
        # Write back to file
        with open(self.env_file, 'w') as f:
            f.writelines(lines)
    
    async def _test_api_connections(self):
        """Test API connections."""
        console.print("\n🧪 Testing API Connections", style="bold yellow")
        
        try:
            # Load settings with new API keys
            os.environ.update(self.config)
            settings = get_settings()
            
            # Test Gemini API
            console.print("Testing Gemini API...", end=" ")
            try:
                gemini_client = GeminiClient(settings)
                response = await gemini_client.generate_text(
                    "Say 'Hello from Gemini!' in exactly those words."
                )
                if "Hello from Gemini!" in response.content:
                    console.print("✅", style="green")
                else:
                    console.print("⚠️ Unexpected response", style="yellow")
            except Exception as e:
                console.print(f"❌ {str(e)}", style="red")
            
            # Test Perplexity API
            console.print("Testing Perplexity API...", end=" ")
            try:
                perplexity_client = PerplexityClient(settings)
                response = await perplexity_client.search_and_answer(
                    "What is the current year?"
                )
                if response.content:
                    console.print("✅", style="green")
                else:
                    console.print("⚠️ Empty response", style="yellow")
                
                await perplexity_client.close()
            except Exception as e:
                console.print(f"❌ {str(e)}", style="red")
            
        except Exception as e:
            console.print(f"❌ API testing failed: {e}", style="red")
    
    def _setup_directories(self):
        """Create necessary directories."""
        console.print("\n📁 Setting up directories...", style="bold yellow")
        
        directories = [
            "data",
            "data/chroma_db",
            "data/memory",
            "data/workspace",
            "data/repositories",
            "data/cache",
            "logs",
            "backups"
        ]
        
        project_root = Path(__file__).parent.parent
        
        for dir_name in directories:
            dir_path = project_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            console.print(f"✅ Created {dir_name}")
    
    def _display_setup_summary(self):
        """Display setup summary."""
        console.print("\n📊 Setup Summary", style="bold green")
        
        table = Table(title="Configuration Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Notes")
        
        # Check API keys
        current_config = self._read_env_file()
        
        gemini_status = "✅ Configured" if current_config.get("GEMINI_API_KEY") else "❌ Missing"
        perplexity_status = "✅ Configured" if current_config.get("PERPLEXITY_API_KEY") else "❌ Missing"
        
        table.add_row("Gemini API", gemini_status, "For reasoning and generation")
        table.add_row("Perplexity API", perplexity_status, "For search and research")
        table.add_row("Directories", "✅ Created", "Data, logs, and cache directories")
        table.add_row("Environment", "✅ Ready", ".env file configured")
        
        console.print(table)

def main():
    """Main setup function."""
    setup_manager = SetupManager()
    setup_manager.run_setup()

if __name__ == "__main__":
    main()
