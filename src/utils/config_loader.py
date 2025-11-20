"""
Configuration Loader - Updated for free APIs
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

def load_config() -> Dict[str, Any]:
    """Load configuration - now works without API key"""
    
    # Try to load .env file
    load_dotenv()
    
    # Configuration with sensible defaults
    config = {
        'openai_api_key': os.getenv('OPENAI_API_KEY', 'free'),
        'model': os.getenv('MODEL', 'huggingface'),
        'max_history': int(os.getenv('MAX_HISTORY', '20')),
        'temperature': float(os.getenv('TEMPERATURE', '0.7')),
        'max_tokens': int(os.getenv('MAX_TOKENS', '200'))
    }
    
    # No longer require API key since we use free services
    return config