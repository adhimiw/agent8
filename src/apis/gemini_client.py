"""
Gemini API client for the Autonomous Personal Assistant.
Handles integration with Google's Gemini API for reasoning and generation.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import dspy

from config.settings import Settings
from core.logger import get_api_logger

logger = get_api_logger()

@dataclass
class GeminiResponse:
    """Response from Gemini API."""
    content: str
    usage: Dict[str, int]
    model: str
    finish_reason: str
    safety_ratings: Optional[List[Dict]] = None

class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_key = settings.api.gemini_api_key
        self.model_name = settings.api.gemini_model
        self.temperature = settings.api.gemini_temperature
        self.max_tokens = settings.api.gemini_max_tokens
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                top_p=0.8,
                top_k=40
            ),
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )
        
        logger.info("Gemini client initialized", model=self.model_name)
    
    async def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        **kwargs
    ) -> GeminiResponse:
        """Generate text using Gemini API."""
        try:
            # Prepare the prompt
            if system_instruction:
                full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"
            else:
                full_prompt = prompt
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
                **kwargs
            )
            
            # Extract response data
            content = response.text if response.text else ""
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
            }
            
            finish_reason = response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN"
            safety_ratings = [
                {
                    "category": rating.category.name,
                    "probability": rating.probability.name
                }
                for rating in response.candidates[0].safety_ratings
            ] if response.candidates and response.candidates[0].safety_ratings else None
            
            logger.info(
                "Gemini text generation completed",
                tokens_used=usage["total_tokens"],
                finish_reason=finish_reason
            )
            
            return GeminiResponse(
                content=content,
                usage=usage,
                model=self.model_name,
                finish_reason=finish_reason,
                safety_ratings=safety_ratings
            )
            
        except Exception as e:
            logger.error("Gemini text generation failed", error=str(e))
            raise
    
    async def generate_stream(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generate streaming text using Gemini API."""
        try:
            # Prepare the prompt
            if system_instruction:
                full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"
            else:
                full_prompt = prompt
            
            # Generate streaming response
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
                stream=True,
                **kwargs
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
            
            logger.info("Gemini streaming generation completed")
            
        except Exception as e:
            logger.error("Gemini streaming generation failed", error=str(e))
            raise
    
    async def analyze_image(
        self, 
        image_data: bytes, 
        prompt: str,
        mime_type: str = "image/jpeg"
    ) -> GeminiResponse:
        """Analyze an image using Gemini's multimodal capabilities."""
        try:
            # Create image part
            image_part = {
                "mime_type": mime_type,
                "data": image_data
            }
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                [prompt, image_part]
            )
            
            # Extract response data
            content = response.text if response.text else ""
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
            }
            
            finish_reason = response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN"
            
            logger.info(
                "Gemini image analysis completed",
                tokens_used=usage["total_tokens"],
                mime_type=mime_type
            )
            
            return GeminiResponse(
                content=content,
                usage=usage,
                model=self.model_name,
                finish_reason=finish_reason
            )
            
        except Exception as e:
            logger.error("Gemini image analysis failed", error=str(e))
            raise
    
    async def function_call(
        self, 
        prompt: str, 
        functions: List[Dict[str, Any]],
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute function calling with Gemini."""
        try:
            # Configure model with function declarations
            model_with_functions = genai.GenerativeModel(
                model_name=self.model_name,
                tools=functions,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens
                )
            )
            
            # Prepare the prompt
            if system_instruction:
                full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"
            else:
                full_prompt = prompt
            
            # Generate response
            response = await asyncio.to_thread(
                model_with_functions.generate_content,
                full_prompt
            )
            
            # Extract function calls
            function_calls = []
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        function_calls.append({
                            "name": part.function_call.name,
                            "arguments": dict(part.function_call.args)
                        })
            
            logger.info(
                "Gemini function calling completed",
                function_calls_count=len(function_calls)
            )
            
            return {
                "content": response.text if response.text else "",
                "function_calls": function_calls,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                    "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
                }
            }
            
        except Exception as e:
            logger.error("Gemini function calling failed", error=str(e))
            raise

class GeminiDSPyLM(dspy.LM):
    """DSPy language model wrapper for Gemini."""
    
    def __init__(self, gemini_client: GeminiClient):
        self.client = gemini_client
        super().__init__(model=gemini_client.model_name)
    
    def basic_request(self, prompt: str, **kwargs) -> List[Dict[str, Any]]:
        """Basic request implementation for DSPy."""
        try:
            # Run async method in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            response = loop.run_until_complete(
                self.client.generate_text(prompt, **kwargs)
            )
            
            return [{
                "text": response.content,
                "usage": response.usage
            }]
            
        except Exception as e:
            logger.error("DSPy Gemini request failed", error=str(e))
            raise
        finally:
            loop.close()
    
    def __call__(self, prompt: str, **kwargs) -> List[str]:
        """Call implementation for DSPy."""
        responses = self.basic_request(prompt, **kwargs)
        return [response["text"] for response in responses]
