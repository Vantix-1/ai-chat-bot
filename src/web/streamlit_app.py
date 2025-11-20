"""
Streamlit Web Interface - Modern chat UI for AI assistant
"""
import streamlit as st
import os
import sys

# ABSOLUTE PATH SOLUTION
PROJECT_ROOT = r"C:\Users\mitch\OneDrive\Documents\GitHub\ai-chat-bot"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import modules
try:
    from src.core.chat_engine import AIChatEngine
    from src.utils.config_loader import load_config
except ImportError as e:
    st.error(f"❌ Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_engine' not in st.session_state:
    try:
        config = load_config()
        st.session_state.chat_engine = AIChatEngine(
            api_key=config['openai_api_key'],
            model=config.get('model', 'gpt-3.5-turbo')
        )
        st.success("✅ AI Chat Bot initialized successfully!")
    except Exception as e:
        st.error(f"❌ Failed to initialize chat engine: {e}")
        
        # Show helpful instructions
        st.markdown("""
        ### 🔧 Setup Instructions:
        
        1. **Get an OpenAI API Key:**
           - Visit https://platform.openai.com/api-keys
           - Create an account if needed
           - Click "Create new secret key"
           - Copy the key (starts with `sk-`)
        
        2. **Create a `.env` file in your project root:**
        ```env
        OPENAI_API_KEY=sk-your-actual-key-here
        MODEL=gpt-3.5-turbo
        MAX_HISTORY=20
        TEMPERATURE=0.7
        MAX_TOKENS=500
        ```
        
        3. **Restart the application**
        """)
        
        # Debug information
        with st.expander("🔧 Debug Information"):
            st.write(f"**Project Root:** {PROJECT_ROOT}")
            st.write(f"**Current Directory:** {os.getcwd()}")
            
            # Check if .env file exists
            env_path = os.path.join(PROJECT_ROOT, ".env")
            st.write(f"**.env File Exists:** {os.path.exists(env_path)}")
            
            if os.path.exists(env_path):
                st.write("**.env Content:**")
                try:
                    with open(env_path, 'r') as f:
                        st.code(f.read())
                except Exception as read_error:
                    st.write(f"Could not read .env: {read_error}")
            
            # Check environment variables
            st.write("**Environment Variables:**")
            st.write(f"OPENAI_API_KEY: {'***' + os.getenv('OPENAI_API_KEY', 'NOT SET')[-4:] if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
        
        st.stop()

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b3137;
        border-left: 4px solid #00d4ff;
    }
    .chat-message.assistant {
        background-color: #1a1a2e;
        border-left: 4px solid #764ba2;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chat Settings")
    st.markdown("---")
    
    # Model selection
    model_option = st.selectbox(
        "AI Model",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0
    )
    
    # Conversation controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Chat"):
            st.session_state.messages = []
            st.session_state.chat_engine.memory.clear_conversation("user")
            st.rerun()
    
    with col2:
        if st.button("📊 Stats"):
            stats = st.session_state.chat_engine.get_conversation_stats("user")
            st.write(f"Messages: {stats['total_messages']}")
            st.write(f"API Requests: {stats['api_usage']['total_requests']}")
    
    st.markdown("---")
    st.markdown("### Conversation Info")
    st.info(f"Messages in history: {len(st.session_state.messages)}")

# Main chat interface
st.title("🤖 AI Chat Assistant")
st.markdown("Chat with an intelligent AI assistant powered by OpenAI")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user">
                <div class="message-header">👤 You</div>
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant">
                <div class="message-header">🤖 Assistant</div>
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    with st.spinner("🤖 Thinking..."):
        response = st.session_state.chat_engine.chat(prompt, "user")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update the display
    st.rerun()