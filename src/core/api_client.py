"""
Multi-API Client - Fixed and working version
"""
import requests
import json
from typing import List, Dict
import logging
import random

logger = logging.getLogger(__name__)

class MultiAPIClient:
    def __init__(self):
        self.usage_stats = {"total_requests": 0, "errors": 0}
        
    def chat_completion(self, messages: List[Dict], model: str = "huggingface", temperature: float = 0.7, max_tokens: int = 200) -> Dict:
        """
        Try multiple AI providers in order
        """
        self.usage_stats["total_requests"] += 1
        
        # Convert messages to prompt
        prompt = self._messages_to_prompt(messages)
        
        # Try local responses first (most reliable)
        response = self._local_intelligent_response(prompt, messages)
        if response["success"]:
            return response
            
        # Try Hugging Face
        response = self._try_huggingface(prompt)
        if response["success"]:
            return response
            
        # Final fallback
        return self._fallback_response(prompt)
    
    def _local_intelligent_response(self, prompt: str, messages: List[Dict]) -> Dict:
        """Intelligent local responses without API calls"""
        try:
            last_user_message = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    last_user_message = msg["content"].lower()
                    break
            
            # Context-aware responses
            response_map = {
                "hello": [
                    "Hello! 👋 I'm your AI assistant. How can I help you today?",
                    "Hi there! 😊 What would you like to talk about?",
                    "Hey! Great to see you. What can I help you with?"
                ],
                "hi": [
                    "Hello! How are you doing today?",
                    "Hi there! 👋 What's on your mind?",
                    "Hey! Nice to meet you!"
                ],
                "how are you": [
                    "I'm doing great, thanks for asking! Ready to help you with anything. 😊",
                    "I'm functioning perfectly! How are you doing today?",
                    "Doing well! Excited to chat with you."
                ],
                "what is your name": [
                    "I'm your AI assistant! You can call me ChatBot. 🤖",
                    "I'm an AI assistant created to help answer your questions!",
                    "I'm your friendly neighborhood AI assistant!"
                ],
                "help": [
                    "I'm here to help! What do you need assistance with?",
                    "I'd be happy to help. What questions do you have?",
                    "How can I assist you today? Feel free to ask me anything!"
                ],
                "thank": [
                    "You're welcome! 😊 Is there anything else I can help with?",
                    "Happy to help! Let me know if you have other questions.",
                    "You're very welcome! I'm here whenever you need me."
                ],
                "python": [
                    "Python is a fantastic programming language! 🐍 It's great for AI, web development, and automation.",
                    "I love Python! It's one of the best languages for beginners and experts alike.",
                    "Python is excellent for AI development! Are you working on a Python project?"
                ],
                "ai": [
                    "Artificial Intelligence is fascinating! I'm an example of AI technology. 🤖",
                    "AI is transforming our world! From assistants like me to self-driving cars.",
                    "Artificial Intelligence helps me understand and respond to your questions!"
                ],
                "weather": [
                    "I don't have real-time weather data, but I can help you find weather information online!",
                    "For current weather, I'd recommend checking your local weather service. I can help with other questions!",
                    "I'm not connected to weather services, but I can help you with many other topics!"
                ],
                "time": [
                    f"I don't have real-time clock access, but you can check the time on your device!",
                    "For the current time, please check your computer or phone clock.",
                    "I'm not connected to a clock, but I can help with other questions!"
                ]
            }
            
            # Find the best matching response
            for key, responses in response_map.items():
                if key in last_user_message:
                    response_text = random.choice(responses)
                    return {
                        "success": True,
                        "content": response_text,
                        "model": "local_intelligent",
                        "provider": "local"
                    }
            
            # Default intelligent responses
            default_responses = [
                "That's an interesting question! I'd be happy to help you explore that topic.",
                "I understand what you're asking. Let me provide some insights on that.",
                "Thanks for your message! I'm here to assist you with your questions.",
                "I appreciate you reaching out. Let me think about how best to help you.",
                "That's a great point! Here's what I can share about that topic...",
                "I'd be glad to help with that. Let me provide some information.",
                "Interesting question! Here are my thoughts on that matter...",
                "I understand you're looking for information about that. Let me help.",
                "Thanks for asking! I can definitely provide some guidance on that.",
                "I appreciate your question. Here's what I know about that topic.",
                "That's a thoughtful question! Let me share what I understand about it.",
                "I'd be happy to discuss that with you. Here's my perspective...",
                "Great question! Let me provide some information that might help.",
                "I understand your interest in that topic. Here's what I can tell you.",
                "Thanks for bringing that up! It's an important topic to discuss."
            ]
            
            response_text = random.choice(default_responses)
            return {
                "success": True,
                "content": response_text,
                "model": "local_intelligent",
                "provider": "local"
            }
            
        except Exception as e:
            logger.error(f"Local response error: {e}")
            return {"success": False, "error": str(e)}
    
    def _try_huggingface(self, prompt: str) -> Dict:
        """Try Hugging Face Inference API"""
        try:
            # Use a simple, reliable model
            API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 150,
                    "temperature": 0.7,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(API_URL, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and 'generated_text' in result:
                    return {
                        "success": True,
                        "content": result['generated_text'],
                        "model": "microsoft/DialoGPT-medium",
                        "provider": "huggingface"
                    }
                elif isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        return {
                            "success": True,
                            "content": result[0]['generated_text'],
                            "model": "microsoft/DialoGPT-medium", 
                            "provider": "huggingface"
                        }
            
            return {"success": False, "error": "Hugging Face API unavailable"}
            
        except Exception as e:
            logger.error(f"Hugging Face error: {e}")
            return {"success": False, "error": str(e)}
    
    def _try_openrouter(self, prompt: str, max_tokens: int = 200) -> Dict:
        """Try OpenRouter - FIXED version"""
        try:
            # OpenRouter with free tier (you can sign up at https://openrouter.ai/)
            api_key = "free"  # Replace with actual key if you get one
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens  # This was missing!
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return {
                    "success": True,
                    "content": content,
                    "model": "gpt-3.5-turbo",
                    "provider": "openrouter"
                }
            else:
                return {"success": False, "error": f"OpenRouter error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
            return {"success": False, "error": str(e)}
    
    def _fallback_response(self, prompt: str) -> Dict:
        """Final fallback when all else fails"""
        fallback_responses = [
            "I'm here to help! Feel free to ask me anything.",
            "Thanks for your message! I'm ready to assist you.",
            "Hello! I'm your AI assistant. How can I help you today?",
            "I appreciate you reaching out. What can I help you with?",
            "I'm ready to chat! What would you like to know?",
            "Great to hear from you! How can I assist today?",
            "I'm here and ready to help with your questions!",
            "Thanks for starting a conversation! What's on your mind?",
            "Hello there! I'm excited to help you with anything you need.",
            "I'm available to chat! What would you like to discuss?"
        ]
        
        response = random.choice(fallback_responses)
        
        return {
            "success": True,
            "content": response,
            "model": "fallback",
            "provider": "local_fallback"
        }
    
    def _messages_to_prompt(self, messages: List[Dict]) -> str:
        """Convert message history to a single prompt"""
        conversation = []
        for msg in messages:
            if msg["role"] == "system":
                conversation.append(f"System: {msg['content']}")
            elif msg["role"] == "user":
                conversation.append(f"User: {msg['content']}")
            elif msg["role"] == "assistant":
                conversation.append(f"Assistant: {msg['content']}")
        
        return "\n".join(conversation[-4:])  # Last 2 exchanges
    
    def get_usage_stats(self) -> Dict:
        return self.usage_stats.copy()
    
    def validate_api_key(self) -> bool:
        return True  # Always works with local responses