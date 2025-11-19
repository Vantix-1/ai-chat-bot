"""
Enhanced Conversation Memory Manager - Complete implementation
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConversationMemory:
    def __init__(self, max_history: int = 20, data_dir: str = "data/conversations"):
        self.max_history = max_history
        self.data_dir = data_dir
        self.conversations: Dict[str, List[Dict]] = {}
        os.makedirs(data_dir, exist_ok=True)
        
    def add_message(self, user_id: str, role: str, content: str):
        """Add a message to conversation history"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
            
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "message_id": len(self.conversations[user_id]) + 1
        }
        
        self.conversations[user_id].append(message)
        
        # Trim history if too long
        if len(self.conversations[user_id]) > self.max_history * 2:
            self.conversations[user_id] = self.conversations[user_id][-self.max_history * 2:]
            
        logger.debug(f"Added message to user {user_id}: {role} - {content[:50]}...")
    
    def get_conversation(self, user_id: str) -> List[Dict]:
        """Get conversation history for user"""
        return self.conversations.get(user_id, [])
    
    def get_last_n_messages(self, user_id: str, n: int) -> List[Dict]:
        """Get last N messages from conversation"""
        conversation = self.get_conversation(user_id)
        return conversation[-n:] if conversation else []
    
    def clear_conversation(self, user_id: str):
        """Clear conversation history for user"""
        if user_id in self.conversations:
            self.conversations[user_id] = []
            logger.info(f"Cleared conversation for user {user_id}")
    
    def save_conversation(self, user_id: str, filename: Optional[str] = None):
        """Save conversation to JSON file"""
        if user_id not in self.conversations or not self.conversations[user_id]:
            logger.warning(f"No conversation to save for user {user_id}")
            return None
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{user_id}_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            conversation_data = {
                "user_id": user_id,
                "exported_at": datetime.now().isoformat(),
                "total_messages": len(self.conversations[user_id]),
                "messages": self.conversations[user_id]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved conversation for user {user_id} to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save conversation for user {user_id}: {e}")
            return None
    
    def load_conversation(self, user_id: str, filepath: str) -> bool:
        """Load conversation from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)
            
            self.conversations[user_id] = conversation_data.get("messages", [])
            logger.info(f"Loaded conversation for user {user_id} from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load conversation for user {user_id}: {e}")
            return False
    
    def export_conversation(self, user_id: str, format: str = "json") -> Optional[str]:
        """Export conversation in specified format"""
        if format == "json":
            return self._export_json(user_id)
        elif format == "text":
            return self._export_text(user_id)
        else:
            logger.error(f"Unsupported export format: {format}")
            return None
    
    def _export_json(self, user_id: str) -> Optional[str]:
        """Export conversation as JSON string"""
        if user_id not in self.conversations:
            return None
            
        conversation_data = {
            "user_id": user_id,
            "exported_at": datetime.now().isoformat(),
            "total_messages": len(self.conversations[user_id]),
            "messages": self.conversations[user_id]
        }
        
        return json.dumps(conversation_data, indent=2, ensure_ascii=False)
    
    def _export_text(self, user_id: str) -> Optional[str]:
        """Export conversation as readable text"""
        if user_id not in self.conversations:
            return None
            
        text_lines = [f"Conversation with {user_id}"]
        text_lines.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        text_lines.append("-" * 50)
        
        for msg in self.conversations[user_id]:
            role = "You" if msg["role"] == "user" else "Assistant"
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
            text_lines.append(f"[{timestamp}] {role}: {msg['content']}")
        
        return "\n".join(text_lines)
    
    def get_user_ids(self) -> List[str]:
        """Get list of all user IDs with conversations"""
        return list(self.conversations.keys())