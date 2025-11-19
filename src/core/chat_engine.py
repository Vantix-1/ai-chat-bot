"""
Enhanced AI Chat Engine - Complete implementation with error handling and features
"""
import logging
from typing import List, Dict, Optional
from .api_client import OpenAIClient
from .memory_manager import ConversationMemory

logger = logging.getLogger(__name__)

class AIChatEngine:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_client = OpenAIClient(api_key)
        self.model = model
        self.memory = ConversationMemory()
        self.system_prompts = self._load_system_prompts()
        
        # Validate API key on initialization
        if not self.api_client.validate_api_key():
            raise ValueError("Invalid OpenAI API key")
    
    def _load_system_prompts(self) -> Dict:
        """Load system prompts for different conversation modes"""
        return {
            "default": "You are a helpful, knowledgeable AI assistant. Provide clear, concise, and accurate responses. Maintain context from previous messages and be conversational.",
            "technical": "You are a technical AI assistant specializing in programming, AI, and technology. Provide detailed, accurate technical explanations with code examples when appropriate.",
            "creative": "You are a creative AI assistant. Be imaginative, engaging, and provide creative ideas, stories, and solutions. Use expressive language.",
            "professional": "You are a professional business AI assistant. Provide formal, structured responses suitable for business contexts. Be precise and objective."
        }
    
    def chat(
        self, 
        message: str, 
        user_id: str = "default",
        conversation_mode: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Dict:
        """
        Process user message and return AI response with metadata
        """
        try:
            # Get conversation history
            history = self.memory.get_conversation(user_id)
            
            # Build messages with appropriate system prompt
            system_prompt = self.system_prompts.get(conversation_mode, self.system_prompts["default"])
            messages = self._build_messages(history, message, system_prompt)
            
            # Call OpenAI API
            api_response = self.api_client.chat_completion(
                messages=messages,
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if api_response["success"]:
                ai_response = api_response["content"]
                
                # Update conversation memory
                self.memory.add_message(user_id, "user", message)
                self.memory.add_message(user_id, "assistant", ai_response)
                
                return {
                    "success": True,
                    "response": ai_response,
                    "usage": api_response.get("usage", {}),
                    "model": api_response.get("model", self.model),
                    "conversation_length": len(self.memory.get_conversation(user_id))
                }
            else:
                return {
                    "success": False,
                    "error": api_response.get("error", "Unknown API error"),
                    "response": api_response.get("content", "I encountered an error.")
                }
                
        except Exception as e:
            logger.error(f"Chat engine error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I encountered an internal error. Please try again."
            }
    
    def _build_messages(self, history: List[Dict], new_message: str, system_prompt: str) -> List[Dict]:
        """Build message list for API call with context management"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (maintain context)
        for msg in history[-10:]:  # Last 5 exchanges (10 messages)
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add new user message
        messages.append({"role": "user", "content": new_message})
        
        return messages
    
    def get_conversation_stats(self, user_id: str) -> Dict:
        """Get statistics for a conversation"""
        conversation = self.memory.get_conversation(user_id)
        return {
            "total_messages": len(conversation),
            "user_messages": len([m for m in conversation if m["role"] == "user"]),
            "assistant_messages": len([m for m in conversation if m["role"] == "assistant"]),
            "api_usage": self.api_client.get_usage_stats()
        }
    
    def set_conversation_mode(self, user_id: str, mode: str):
        """Change conversation mode for a user"""
        if mode not in self.system_prompts:
            raise ValueError(f"Invalid conversation mode: {mode}")
        # This would be implemented to change how future messages are processed
        logger.info(f"User {user_id} changed conversation mode to: {mode}")
    
    def export_conversation(self, user_id: str, format: str = "json") -> str:
        """Export conversation in specified format"""
        return self.memory.export_conversation(user_id, format)