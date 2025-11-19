"""
OpenAI API Client - Handles all interactions with OpenAI's API
"""
import openai
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "errors": 0
        }
    
    def chat_completion(
        self, 
        messages: List[Dict], 
        model: str = "gpt-3.5-turbo", 
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Dict:
        """
        Send chat completion request to OpenAI API
        """
        try:
            self.usage_stats["total_requests"] += 1
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            
            # Extract usage information
            if response.usage:
                self.usage_stats["total_tokens"] += response.usage.total_tokens
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                }
            }
            
        except openai.APIConnectionError as e:
            logger.error(f"OpenAI API connection error: {e}")
            self.usage_stats["errors"] += 1
            return {
                "success": False,
                "error": f"Connection error: {e}",
                "content": "I'm having trouble connecting to the AI service. Please check your internet connection."
            }
            
        except openai.RateLimitError as e:
            logger.error(f"OpenAI API rate limit exceeded: {e}")
            self.usage_stats["errors"] += 1
            return {
                "success": False,
                "error": f"Rate limit exceeded: {e}",
                "content": "I'm receiving too many requests too quickly. Please wait a moment and try again."
            }
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            self.usage_stats["errors"] += 1
            return {
                "success": False,
                "error": f"API error: {e}",
                "content": "I encountered an error with the AI service. Please try again later."
            }
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self.usage_stats["errors"] += 1
            return {
                "success": False,
                "error": f"Unexpected error: {e}",
                "content": "An unexpected error occurred. Please try again."
            }
    
    def get_usage_stats(self) -> Dict:
        """Get usage statistics"""
        return self.usage_stats.copy()
    
    def validate_api_key(self) -> bool:
        """Validate the OpenAI API key"""
        try:
            # Make a simple request to validate the API key
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False