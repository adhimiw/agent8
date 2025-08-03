#!/usr/bin/env python3
"""
Test script for API integrations.
Validates that Gemini and Perplexity APIs are working correctly.
"""

import asyncio
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config.settings import get_settings
from apis.gemini_client import GeminiClient
from apis.perplexity_client import PerplexityClient
from apis.api_manager import APIManager, APIType

console = Console()

async def test_gemini_api():
    """Test Gemini API functionality."""
    console.print("🧠 Testing Gemini API...", style="bold cyan")
    
    try:
        settings = get_settings()
        client = GeminiClient(settings)
        
        # Test basic text generation
        response = await client.generate_text(
            "Explain what an autonomous AI assistant is in one sentence."
        )
        
        console.print("✅ Gemini API working correctly", style="green")
        console.print(f"Response: {response.content[:100]}...")
        console.print(f"Tokens used: {response.usage['total_tokens']}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ Gemini API test failed: {e}", style="red")
        return False

async def test_perplexity_api():
    """Test Perplexity API functionality."""
    console.print("🔍 Testing Perplexity API...", style="bold cyan")
    
    try:
        settings = get_settings()
        client = PerplexityClient(settings)
        
        # Test search and answer
        response = await client.search_and_answer(
            "What are the latest developments in AI assistants in 2024?"
        )
        
        console.print("✅ Perplexity API working correctly", style="green")
        console.print(f"Response: {response.content[:100]}...")
        console.print(f"Citations: {len(response.citations)}")
        console.print(f"Tokens used: {response.usage.get('total_tokens', 0)}")
        
        await client.close()
        return True
        
    except Exception as e:
        console.print(f"❌ Perplexity API test failed: {e}", style="red")
        return False

async def test_api_manager():
    """Test API Manager functionality."""
    console.print("🎛️ Testing API Manager...", style="bold cyan")
    
    try:
        settings = get_settings()
        manager = APIManager(settings)
        
        # Test routing
        reasoning_response = await manager.route_request(
            APIType.REASONING,
            "What is 2+2? Answer with just the number."
        )
        
        search_response = await manager.route_request(
            APIType.SEARCH,
            "What is the current weather like?"
        )
        
        # Test hybrid request
        hybrid_results = await manager.hybrid_request(
            "Explain quantum computing and find recent news about it",
            use_search=True,
            use_reasoning=True
        )
        
        console.print("✅ API Manager working correctly", style="green")
        console.print(f"Reasoning response: {reasoning_response.content[:50]}...")
        console.print(f"Search response: {search_response.content[:50]}...")
        console.print(f"Hybrid results: {len(hybrid_results)} responses")
        
        await manager.close()
        return True
        
    except Exception as e:
        console.print(f"❌ API Manager test failed: {e}", style="red")
        return False

async def run_comprehensive_test():
    """Run comprehensive API tests."""
    console.print(Panel.fit(
        "🧪 API Integration Test Suite",
        subtitle="Testing Gemini, Perplexity, and API Manager",
        border_style="blue"
    ))
    
    results = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Test Gemini API
        task1 = progress.add_task("Testing Gemini API...", total=None)
        results["gemini"] = await test_gemini_api()
        progress.update(task1, completed=True)
        
        # Test Perplexity API
        task2 = progress.add_task("Testing Perplexity API...", total=None)
        results["perplexity"] = await test_perplexity_api()
        progress.update(task2, completed=True)
        
        # Test API Manager
        task3 = progress.add_task("Testing API Manager...", total=None)
        results["api_manager"] = await test_api_manager()
        progress.update(task3, completed=True)
    
    # Display results table
    table = Table(title="API Test Results")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Notes")
    
    for component, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        notes = "Working correctly" if success else "Check configuration"
        table.add_row(component.title(), status, notes)
    
    console.print(table)
    
    # Overall result
    all_passed = all(results.values())
    if all_passed:
        console.print("🎉 All API tests passed!", style="bold green")
        console.print("Your autonomous assistant is ready to run!", style="green")
    else:
        console.print("⚠️ Some tests failed. Please check your configuration.", style="yellow")
        console.print("Run: python scripts/setup.py to reconfigure", style="cyan")
    
    return all_passed

async def main():
    """Main test function."""
    try:
        success = await run_comprehensive_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n❌ Tests cancelled by user", style="yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"❌ Test suite failed: {e}", style="bold red")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
