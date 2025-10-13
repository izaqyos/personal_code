import streamlit as st
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_helper import get_claude_response, format_messages
from utils.ui_components import (
    display_chat_message, 
    initialize_chat_state, 
    add_message_to_history, 
    create_chat_input
)

# Page configuration
st.set_page_config(
    page_title="Simple Chat | AI Assistant Tutorial",
    page_icon="💬",
    layout="wide"
)

# Title
st.title("💬 Simple Chat Interface")

# Description
st.markdown("""
This example demonstrates a basic chat interface using Streamlit and the Anthropic Claude API.
It showcases how to:
- Create a simple chat UI
- Handle user input
- Call the Claude API
- Display assistant responses
- Maintain conversation history

Perfect for simple AI assistants and chatbots.
""")

# Add a divider
st.divider()

# Initialize chat state
initialize_chat_state()

# Model settings sidebar
with st.sidebar:
    st.subheader("Model Configuration")
    model = st.selectbox(
        "Select Model",
        ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        index=1
    )
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness: 0 is deterministic, 1 is creative"
    )
    
    # System prompt
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "System Instructions",
        value="You are a helpful AI assistant. Answer the user's questions clearly and concisely.",
        height=100
    )
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
st.subheader("Chat")
for message in st.session_state.messages:
    display_chat_message(message["role"], message["content"])

# User input
user_input = create_chat_input("Ask me anything...")

# Submit button
submit_button = st.button("Send")

# Process input and generate response
if submit_button and user_input:
    # Add user message to chat
    add_message_to_history("user", user_input)
    
    # Display user message
    display_chat_message("user", user_input)
    
    # Prepare messages for API call
    messages = []
    
    # Add system prompt if provided
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add chat history
    for message in st.session_state.messages:
        messages.append(message)
    
    # Display a spinner while generating response
    with st.spinner("Thinking..."):
        response = get_claude_response(
            messages=messages,
            model=model,
            temperature=temperature
        )
    
    # Add assistant response to chat
    add_message_to_history("assistant", response)
    
    # Display assistant response
    display_chat_message("assistant", response)
    
    # Clear input field
    st.rerun()

# Code explanation
with st.expander("See Code Explanation"):
    st.markdown("""
    ### Key Components

    1. **Session State**: We use `st.session_state` to maintain chat history between interactions.
    
    2. **User Interface**:
       - `create_chat_input()`: Creates a text input field for user messages
       - `display_chat_message()`: Renders chat messages with proper styling
       
    3. **Message Handling**:
       - `add_message_to_history()`: Adds messages to the session state
       - Messages are formatted into the Claude-compatible format before API calls
       
    4. **Claude Integration**:
       - `get_claude_response()`: Calls the Anthropic Claude API
       - We include the system prompt and conversation history in each request
       
    5. **Interaction Flow**:
       - User types message and clicks send
       - Message is added to history and displayed
       - API call is made with complete context
       - Response is received, added to history, and displayed
       - Input field is cleared for next interaction
    """)

# Additional tips
st.info("""
**Tips for Implementation**:
- Use a consistent message format for all chat interactions
- Consider how to handle API errors gracefully
- For production applications, add rate limiting and proper error handling
- Consider implementing typing indicators for more natural interactions
""") 