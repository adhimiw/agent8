"""
API Manager for coordinating multiple AI APIs.
Handles load balancing, fallbacks, and intelligent routing.
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass

from .gemini_client import GeminiClient, GeminiDSPyLM
from .perplexity_client import PerplexityClient, PerplexityDSPyLM
from config.settings import Settings
from core.logger import get_api_logger

logger = get_api_logger()

class APIType(Enum):
    """Types of API operations."""
    REASONING = "reasoning"
    SEARCH = "search"
    GENERATION = "generation"
    ANALYSIS = "analysis"
    FACT_CHECK = "fact_check"

@dataclass
class APIResponse:
    """Unified API response format."""
    content: str
    source: str
    usage: Dict[str, int]
    metadata: Dict[str, Any]
    citations: Optional[List[Dict]] = None

class APIManager:
    """Manages multiple AI APIs and provides intelligent routing."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        
        # Initialize clients
        self.gemini_client = GeminiClient(settings)
        self.perplexity_client = PerplexityClient(settings)
        
        # DSPy language models
        self.gemini_lm = GeminiDSPyLM(self.gemini_client)
        self.perplexity_lm = PerplexityDSPyLM(self.perplexity_client)
        
        # API routing configuration
        self.api_routing = {
            APIType.REASONING: [self.gemini_client],
            APIType.SEARCH: [self.perplexity_client],
            APIType.GENERATION: [self.gemini_client],
            APIType.ANALYSIS: [self.gemini_client, self.perplexity_client],
            APIType.FACT_CHECK: [self.perplexity_client]
        }
        
        logger.info("API Manager initialized with Gemini and Perplexity clients")
    
    async def route_request(
        self, 
        request_type: APIType, 
        prompt: str,
        **kwargs
    ) -> APIResponse:
        """Route request to the most appropriate API."""
        try:
            # Get available APIs for this request type
            available_apis = self.api_routing.get(request_type, [])
            
            if not available_apis:
                raise ValueError(f"No APIs available for request type: {request_type}")
            
            # Try primary API first
            primary_api = available_apis[0]
            
            try:
                return await self._execute_request(primary_api, request_type, prompt, **kwargs)
            except Exception as e:
                logger.warning(
                    "Primary API failed, trying fallback",
                    primary_api=primary_api.__class__.__name__,
                    error=str(e)
                )
                
                # Try fallback APIs
                for fallback_api in available_apis[1:]:
                    try:
                        return await self._execute_request(fallback_api, request_type, prompt, **kwargs)
                    except Exception as fallback_error:
                        logger.warning(
                            "Fallback API failed",
                            fallback_api=fallback_api.__class__.__name__,
                            error=str(fallback_error)
                        )
                        continue
                
                # If all APIs failed, raise the original error
                raise e
                
        except Exception as e:
            logger.error("API routing failed", request_type=request_type.value, error=str(e))
            raise
    
    async def _execute_request(
        self, 
        api_client: Union[GeminiClient, PerplexityClient],
        request_type: APIType,
        prompt: str,
        **kwargs
    ) -> APIResponse:
        """Execute request on specific API client."""
        
        if isinstance(api_client, GeminiClient):
            return await self._execute_gemini_request(request_type, prompt, **kwargs)
        elif isinstance(api_client, PerplexityClient):
            return await self._execute_perplexity_request(request_type, prompt, **kwargs)
        else:
            raise ValueError(f"Unknown API client type: {type(api_client)}")
    
    async def _execute_gemini_request(
        self, 
        request_type: APIType, 
        prompt: str, 
        **kwargs
    ) -> APIResponse:
        """Execute request using Gemini API."""
        
        if request_type in [APIType.REASONING, APIType.GENERATION, APIType.ANALYSIS]:
            response = await self.gemini_client.generate_text(prompt, **kwargs)
            
            return APIResponse(
                content=response.content,
                source="gemini",
                usage=response.usage,
                metadata={
                    "model": response.model,
                    "finish_reason": response.finish_reason,
                    "safety_ratings": response.safety_ratings
                }
            )
        else:
            raise ValueError(f"Gemini API does not support request type: {request_type}")
    
    async def _execute_perplexity_request(
        self, 
        request_type: APIType, 
        prompt: str, 
        **kwargs
    ) -> APIResponse:
        """Execute request using Perplexity API."""
        
        if request_type in [APIType.SEARCH, APIType.ANALYSIS, APIType.FACT_CHECK]:
            if request_type == APIType.FACT_CHECK:
                result = await self.perplexity_client.fact_check(prompt, **kwargs)
                return APIResponse(
                    content=result["verification"],
                    source="perplexity",
                    usage=result["usage"],
                    metadata={"timestamp": result["timestamp"]},
                    citations=result["citations"]
                )
            else:
                response = await self.perplexity_client.search_and_answer(prompt, **kwargs)
                return APIResponse(
                    content=response.content,
                    source="perplexity",
                    usage=response.usage,
                    metadata={
                        "model": response.model,
                        "finish_reason": response.finish_reason
                    },
                    citations=response.citations
                )
        else:
            raise ValueError(f"Perplexity API does not support request type: {request_type}")
    
    async def hybrid_request(
        self, 
        prompt: str, 
        use_search: bool = True,
        use_reasoning: bool = True,
        **kwargs
    ) -> Dict[str, APIResponse]:
        """Execute hybrid request using multiple APIs."""
        results = {}
        
        try:
            # Parallel execution of different API types
            tasks = []
            
            if use_search:
                tasks.append(
                    self.route_request(APIType.SEARCH, prompt, **kwargs)
                )
            
            if use_reasoning:
                tasks.append(
                    self.route_request(APIType.REASONING, prompt, **kwargs)
                )
            
            # Execute tasks concurrently
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            if use_search and len(responses) > 0:
                if isinstance(responses[0], Exception):
                    logger.error("Search request failed", error=str(responses[0]))
                else:
                    results["search"] = responses[0]
            
            if use_reasoning:
                reasoning_index = 1 if use_search else 0
                if len(responses) > reasoning_index:
                    if isinstance(responses[reasoning_index], Exception):
                        logger.error("Reasoning request failed", error=str(responses[reasoning_index]))
                    else:
                        results["reasoning"] = responses[reasoning_index]
            
            logger.info("Hybrid request completed", results_count=len(results))
            return results
            
        except Exception as e:
            logger.error("Hybrid request failed", error=str(e))
            raise
    
    async def synthesize_responses(
        self, 
        responses: Dict[str, APIResponse],
        synthesis_prompt: Optional[str] = None
    ) -> APIResponse:
        """Synthesize multiple API responses into a unified response."""
        try:
            # Prepare synthesis prompt
            if not synthesis_prompt:
                synthesis_prompt = "Synthesize the following information into a comprehensive response:"
            
            # Combine response contents
            combined_content = []
            all_citations = []
            total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            
            for source, response in responses.items():
                combined_content.append(f"From {source}:\n{response.content}")
                
                if response.citations:
                    all_citations.extend(response.citations)
                
                # Aggregate usage
                for key in total_usage:
                    total_usage[key] += response.usage.get(key, 0)
            
            # Create synthesis prompt
            full_prompt = f"{synthesis_prompt}\n\n" + "\n\n".join(combined_content)
            
            # Use Gemini for synthesis
            synthesis_response = await self.gemini_client.generate_text(
                full_prompt,
                system_instruction="You are an expert at synthesizing information from multiple sources. Provide a comprehensive, well-structured response that combines the best insights from all sources."
            )
            
            # Update usage with synthesis costs
            total_usage["prompt_tokens"] += synthesis_response.usage["prompt_tokens"]
            total_usage["completion_tokens"] += synthesis_response.usage["completion_tokens"]
            total_usage["total_tokens"] += synthesis_response.usage["total_tokens"]
            
            logger.info("Response synthesis completed", sources_count=len(responses))
            
            return APIResponse(
                content=synthesis_response.content,
                source="synthesized",
                usage=total_usage,
                metadata={
                    "sources": list(responses.keys()),
                    "synthesis_model": synthesis_response.model
                },
                citations=all_citations
            )
            
        except Exception as e:
            logger.error("Response synthesis failed", error=str(e))
            raise
    
    def get_dspy_lm(self, api_type: str = "gemini") -> Union[GeminiDSPyLM, PerplexityDSPyLM]:
        """Get DSPy language model for the specified API."""
        if api_type.lower() == "gemini":
            return self.gemini_lm
        elif api_type.lower() == "perplexity":
            return self.perplexity_lm
        else:
            raise ValueError(f"Unknown API type: {api_type}")
    
    async def close(self):
        """Close all API clients."""
        await self.perplexity_client.close()
        logger.info("API Manager closed")
