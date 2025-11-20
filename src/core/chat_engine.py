"""
AI Chat Engine - Updated for free APIs
"""
from .api_client import MultiAPIClient
from .memory_manager import ConversationMemory
from typing import List, Dict

class AIChatEngine:
    def __init__(self, api_key: str = "free", model: str = "huggingface"):
        self.api_client = MultiAPIClient()
        self.model = model
        self.memory = ConversationMemory()
        self.system_prompts = self._load_system_prompts()
    
    def _load_system_prompts(self) -> Dict:
        return {
            "default": "You are a helpful, knowledgeable AI assistant.",
            "technical": "You are a technical AI assistant specializing in programming and technology.",
            "creative": "You are a creative AI assistant. Be imaginative and engaging.",
            "professional": "You are a professional business AI assistant."
        }
    
    def chat(self, message: str, user_id: str = "default", conversation_mode: str = "default") -> str:
        """
        Process user message and return AI response
        """
        try:
            # Get conversation history
            history = self.memory.get_conversation(user_id)
            
            # Build messages
            system_prompt = self.system_prompts.get(conversation_mode, self.system_prompts["default"])
            messages = self._build_messages(history, message, system_prompt)
            
            # Call API
            api_response = self.api_client.chat_completion(messages=messages)
            
            if api_response["success"]:
                ai_response = api_response["content"]
                
                # Update conversation memory
                self.memory.add_message(user_id, "user", message)
                self.memory.add_message(user_id, "assistant", ai_response)
                
                return ai_response
            else:
                return f"I apologize, but I'm having trouble connecting to AI services right now. Please try again in a moment."
                
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def _build_messages(self, history: List[Dict], new_message: str, system_prompt: str) -> List[Dict]:
        """Build message list for API call"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in history[-6:]:  # Last 3 exchanges
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