"""
Perplexity API client for the Autonomous Personal Assistant.
Handles integration with Perplexity's Sonar API for real-time search and research.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass

import httpx
import dspy

from config.settings import Settings
from core.logger import get_api_logger

logger = get_api_logger()

@dataclass
class PerplexityResponse:
    """Response from Perplexity API."""
    content: str
    citations: List[Dict[str, Any]]
    usage: Dict[str, int]
    model: str
    finish_reason: str

class PerplexityClient:
    """Client for interacting with Perplexity's Sonar API."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_key = settings.api.perplexity_api_key
        self.model_name = settings.api.perplexity_model
        self.temperature = settings.api.perplexity_temperature
        self.max_tokens = settings.api.perplexity_max_tokens
        
        # API configuration
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # HTTP client
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=60.0
        )
        
        logger.info("Perplexity client initialized", model=self.model_name)
    
    async def search_and_answer(
        self, 
        query: str, 
        system_message: Optional[str] = None,
        return_citations: bool = True,
        return_images: bool = False,
        search_domain_filter: Optional[List[str]] = None,
        **kwargs
    ) -> PerplexityResponse:
        """Search and answer using Perplexity's Sonar API."""
        try:
            # Prepare messages
            messages = []
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            messages.append({
                "role": "user", 
                "content": query
            })
            
            # Prepare request payload
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "return_citations": return_citations,
                "return_images": return_images,
                **kwargs
            }
            
            # Add domain filter if specified
            if search_domain_filter:
                payload["search_domain_filter"] = search_domain_filter
            
            # Make API request
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract response data
            choice = data["choices"][0]
            content = choice["message"]["content"]
            finish_reason = choice["finish_reason"]
            
            # Extract citations
            citations = []
            if return_citations and "citations" in data:
                citations = data["citations"]
            
            # Extract usage
            usage = data.get("usage", {})
            
            logger.info(
                "Perplexity search completed",
                tokens_used=usage.get("total_tokens", 0),
                citations_count=len(citations),
                finish_reason=finish_reason
            )
            
            return PerplexityResponse(
                content=content,
                citations=citations,
                usage=usage,
                model=self.model_name,
                finish_reason=finish_reason
            )
            
        except Exception as e:
            logger.error("Perplexity search failed", error=str(e))
            raise
    
    async def search_stream(
        self, 
        query: str, 
        system_message: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream search results from Perplexity API."""
        try:
            # Prepare messages
            messages = []
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            messages.append({
                "role": "user", 
                "content": query
            })
            
            # Prepare request payload
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": True,
                **kwargs
            }
            
            # Make streaming API request
            async with self.client.stream("POST", "/chat/completions", json=payload) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # Remove "data: " prefix
                        
                        if data_str.strip() == "[DONE]":
                            break
                        
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and data["choices"]:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue
            
            logger.info("Perplexity streaming search completed")
            
        except Exception as e:
            logger.error("Perplexity streaming search failed", error=str(e))
            raise
    
    async def research_topic(
        self, 
        topic: str, 
        focus_areas: Optional[List[str]] = None,
        time_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Conduct comprehensive research on a topic."""
        try:
            # Build research query
            query_parts = [f"Research and analyze: {topic}"]
            
            if focus_areas:
                query_parts.append(f"Focus on: {', '.join(focus_areas)}")
            
            if time_range:
                query_parts.append(f"Time range: {time_range}")
            
            query_parts.append("Provide comprehensive analysis with key findings, trends, and insights.")
            
            research_query = " ".join(query_parts)
            
            # System message for research
            system_message = """You are a research assistant. Provide comprehensive, well-structured research with:
1. Executive summary
2. Key findings
3. Current trends
4. Supporting evidence with citations
5. Implications and insights
6. Recommendations for further research"""
            
            # Conduct research
            response = await self.search_and_answer(
                query=research_query,
                system_message=system_message,
                return_citations=True,
                max_tokens=4096
            )
            
            logger.info(
                "Topic research completed",
                topic=topic,
                citations_count=len(response.citations)
            )
            
            return {
                "topic": topic,
                "analysis": response.content,
                "citations": response.citations,
                "usage": response.usage,
                "timestamp": asyncio.get_event_loop().time()
            }
            
        except Exception as e:
            logger.error("Topic research failed", topic=topic, error=str(e))
            raise
    
    async def fact_check(
        self, 
        statement: str, 
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fact-check a statement using real-time information."""
        try:
            # Build fact-check query
            query = f"Fact-check this statement: {statement}"
            if context:
                query += f"\n\nContext: {context}"
            
            # System message for fact-checking
            system_message = """You are a fact-checker. Analyze the statement and provide:
1. Verification status (True/False/Partially True/Unverifiable)
2. Supporting evidence with citations
3. Contradicting evidence if any
4. Confidence level
5. Additional context or nuances"""
            
            # Conduct fact-check
            response = await self.search_and_answer(
                query=query,
                system_message=system_message,
                return_citations=True
            )
            
            logger.info("Fact-check completed", statement_length=len(statement))
            
            return {
                "statement": statement,
                "verification": response.content,
                "citations": response.citations,
                "usage": response.usage,
                "timestamp": asyncio.get_event_loop().time()
            }
            
        except Exception as e:
            logger.error("Fact-check failed", error=str(e))
            raise
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

class PerplexityDSPyLM(dspy.LM):
    """DSPy language model wrapper for Perplexity."""
    
    def __init__(self, perplexity_client: PerplexityClient):
        self.client = perplexity_client
        super().__init__(model=perplexity_client.model_name)
    
    def basic_request(self, prompt: str, **kwargs) -> List[Dict[str, Any]]:
        """Basic request implementation for DSPy."""
        try:
            # Run async method in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            response = loop.run_until_complete(
                self.client.search_and_answer(prompt, **kwargs)
            )
            
            return [{
                "text": response.content,
                "citations": response.citations,
                "usage": response.usage
            }]
            
        except Exception as e:
            logger.error("DSPy Perplexity request failed", error=str(e))
            raise
        finally:
            loop.close()
    
    def __call__(self, prompt: str, **kwargs) -> List[str]:
        """Call implementation for DSPy."""
        responses = self.basic_request(prompt, **kwargs)
        return [response["text"] for response in responses]
