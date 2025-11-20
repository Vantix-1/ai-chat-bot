# 🤖 AI Chat Bot - Intelligent Local Assistant
<p align="center"> <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=for-the-badge" /> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=for-the-badge" /> <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white&style=for-the-badge" /> <img src="https://img.shields.io/badge/No_API_Keys_Required-00ff99?style=for-the-badge" /> <img src="https://img.shields.io/badge/Production_Ready-blueviolet?style=for-the-badge" /> </p>

---

# 🚀 Overview

---
A modern, production-ready AI chat application built with Streamlit and FastAPI that provides intelligent conversations without requiring any external API keys or paid services. Perfect for developers learning AI integration, portfolio projects, or anyone wanting a private, self-contained chat assistant.

https://via.placeholder.com/AI+Chat+Bot+Interface

---

# ✨ Features

---

🎯 No API Keys Required - Intelligent local responses with context awareness

💬 Conversation Memory - Remains context-aware across multiple messages

🎨 Modern UI - Cyberpunk-themed Streamlit interface

🚀 FastAPI Backend - RESTful API for integration with other applications

📊 Usage Analytics - Track conversation statistics and metrics

💾 Export Conversations - Save chat history as JSON or text

🐳 Docker Ready - Containerized deployment

🔧 Modular Architecture - Easy to extend and customize

---

# 🏗️ Architecture

---

```text
ai-chat-bot/
├── src/
│   ├── core/                 # AI Engine
│   │   ├── chat_engine.py    # Main chat logic
│   │   ├── simple_client.py  # Local AI responses
│   │   └── memory_manager.py # Conversation memory
│   ├── web/                  # Web Interfaces
│   │   ├── streamlit_app.py  # Main web UI
│   │   └── fastapi_server.py # REST API backend
│   └── utils/                # Utilities
│       └── config_loader.py  # Configuration management
├── data/
│   └── conversations/        # Saved chat sessions
├── tests/                    # Test suite
└── docs/                     # Documentation
```
---
# 🛠️ Quick Start
---
Prerequisites:
-Python 3.11 or higher
-Git
---

# Installation & Setup
# Method 1: Standard Installation (Recommended)

---

bash

# 1. Clone the repository
```
git clone https://github.com/Vantix-1/ai-chat-bot.git
cd ai-chat-bot
```

# 2. Create virtual environment
```
python -m venv venv
```

# 3. Activate virtual environment
```
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

# 4. Install dependencies
```
pip install -r requirements.txt
```

# 5. Run the application
```
streamlit run src/web/streamlit_app.py
```

---

# Method 2: Docker Installation

----

bash
# 1. Clone and navigate to project
```
git clone https://github.com/Vantix-1/ai-chat-bot.git
cd ai-chat-bot
```

# 2. Build and run with Docker Compose
```
docker-compose up -d
```

# 3. Access the application at http://localhost:8501

---

# Method 3: Developer Installation

---

bash


# Clone and setup for development
```
git clone https://github.com/Vantix-1/ai-chat-bot.git
cd ai-chat-bot
```

# Create virtual environment
```
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

# Install with development dependencies
```
pip install -r requirements.txt
pip install -e .
```

# Run with auto-reload for development
```
streamlit run src/web/streamlit_app.py
```
---

# 🎯 Usage
---

Web Interface (Recommended)


Start the application:

bash
```
streamlit run src/web/streamlit_app.py
Open your browser to http://localhost:8501
```

# Start chatting! The AI will respond intelligently to your messages

---

# API Usage
---
-Start the FastAPI backend:

bash
```
uvicorn src.web.fastapi_server:app --reload --port 8000
```


-Then interact with the API:

bash
```
# Send a chat message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?", "user_id": "test_user"}'

```

```
# Get conversation stats
curl "http://localhost:8000/conversation/test_user/stats"

```
```
# Clear conversation
curl -X DELETE "http://localhost:8000/conversation/test_user"
```

---
# API documentation available at:
---
```
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
```
---
# 🔧 Configuration
Environment Variables
```
Create a .env file in the project root (optional - works without it):

env
# Optional: For future API integrations
OPENAI_API_KEY=your_key_here
MODEL=gpt-3.5-turbo
MAX_HISTORY=20
TEMPERATURE=0.7
MAX_TOKENS=500

# Server Configuration
PORT=8501
HOST=0.0.0.0
DEBUG=True
Customizing Responses
Edit src/core/simple_client.py to customize the AI responses:

python
# Add your own response categories
self.responses["your_topic"] = [
    "Custom response 1",
    "Custom response 2",
    # Add more responses...
]

```
---

# 🚀 Deployment
---
Production with Docker
bash
# Build the image
```
docker build -t ai-chat-bot .
```

# Run the container
```
docker run -p 8501:8501 -p 8000:8000 ai-chat-bot
Cloud Deployment
Deploy to Heroku
bash
```
# Create Heroku app
```
heroku create your-ai-chat-bot
```

# Set buildpacks
```
heroku buildpacks:add heroku/python
```

# Deploy
```
git push heroku main
Deploy to Railway
bash
```
# Install Railway CLI
```
npm install -g @railway/cli
```

# Deploy
```
railway up
```
---

# 🧪 Testing
---
Run the test suite:

bash
```
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_chat_engine.py
```
---

# 📊 Features in Detail
---
```
Intelligent Local Responses

Context-aware conversations

Multiple response categories

Smart topic detection

Natural conversation flow

Conversation Management
Persistent chat history

Multi-user support

Export capabilities (JSON/Text)

Conversation statistics

Modern Web Interface
Responsive design

Real-time updates

Dark theme

Mobile-friendly
```
---



# 🔄 API Reference
---
```
Chat Endpoint
http
POST /chat
Content-Type: application/json

{
  "message": "Your message here",
  "user_id": "optional_user_id",
  "conversation_mode": "default"
}
Response Format
json
{
  "success": true,
  "response": "AI response text",
  "model": "local_smart",
  "conversation_length": 5
}
```
---


# 🛠️ Development
---
Project Structure
```text
src/
├── core/           # Business logic
├── web/            # Web interfaces  
├── utils/          # Utilities
└── tests/          # Test suite
```


# Adding New Features
---
```
New AI Provider:

Add to src/core/api_client.py

Implement the provider interface

Update the provider selection logic

New UI Component:

Modify src/web/streamlit_app.py

Add new Streamlit components

Update session state management

New API Endpoint:

Add to src/web/fastapi_server.py

Define Pydantic models

Implement endpoint logic
```
---


# 🤝 Contributing
---
```
We welcome contributions! Please see our Contributing Guide for details.

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request
```
---


# 📝 License
---
```
This project is licensed under the MIT License - see the LICENSE file for details.
```
---

# 🙏 Acknowledgments
---
```
Built with Streamlit for the web interface

Backend powered by FastAPI

Inspired by modern AI application architecture

Part of the AI Developer Roadmap 2025-2026
```

# 📞 Support
---
```
Documentation: GitHub Wiki

Issues: GitHub Issues

Discussions: GitHub Discussions
```

# 🚀 Next Steps
---
```
Ready to enhance your AI Chat Bot? Check out these advanced features:

Add voice interface (speech-to-text)

Implement file upload and analysis

Add user authentication

Integrate with external AI APIs

Deploy to cloud platform

Add analytics dashboard
```
---

# Built with ❤️ by Vance Frommer as part of the AI Developer Journey

<p align="center"> <i>If you find this project helpful, please give it a ⭐ on GitHub!</i> </p>