import streamlit as st
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_helper import get_streaming_response, display_streaming_response, format_messages, get_claude_response
from utils.ui_components import (
    display_chat_message, 
    initialize_chat_state, 
    add_message_to_history, 
    create_chat_input,
    create_sidebar_config
)

# Page configuration
st.set_page_config(
    page_title="Advanced Chat | AI Assistant Tutorial",
    page_icon="🚀",
    layout="wide"
)

# Title and description
st.title("🚀 Advanced Chat Interface")
st.markdown("""
This example demonstrates an advanced chat interface with streaming responses, session management,
and a more sophisticated UI. It showcases:

- Streaming responses for a more natural chat experience
- Conversation memory management
- Advanced UI with configurable settings
- System prompt templates
""")

# Add a divider
st.divider()

# Initialize chat state
initialize_chat_state()

# Custom session state initialization
if "persona" not in st.session_state:
    st.session_state.persona = "Helpful Assistant"
if "greeting" not in st.session_state:
    st.session_state.greeting = "Hello! How can I help you today?"

# Sidebar configuration
with st.sidebar:
    # Configuration options
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
    
    # Streaming option
    stream = st.toggle("Stream responses", value=True)
    
    # Persona selection
    st.subheader("Assistant Persona")
    persona = st.selectbox(
        "Select Persona",
        [
            "Helpful Assistant",
            "Python Expert",
            "UX Designer",
            "Data Scientist",
            "Custom"
        ]
    )
    
    # System prompt templates
    system_prompts = {
        "Helpful Assistant": "You are a helpful AI assistant. Answer the user's questions clearly and concisely.",
        "Python Expert": "You are a Python programming expert. Help the user write efficient, readable code. Provide examples when appropriate.",
        "UX Designer": "You are a UX design expert. Help the user create intuitive interfaces with a focus on user experience and accessibility.",
        "Data Scientist": "You are a data science expert. Help the user analyze data, build models, and interpret results.",
        "Custom": ""
    }
    
    # Custom system prompt
    if persona == "Custom":
        system_prompt = st.text_area(
            "Custom System Instructions",
            value="",
            height=150
        )
    else:
        st.session_state.persona = persona
        system_prompt = system_prompts[persona]
        st.text_area(
            "System Instructions",
            value=system_prompt,
            height=150,
            disabled=True
        )
    
    # Greeting message
    st.session_state.greeting = st.text_input(
        "Greeting Message",
        value=st.session_state.greeting
    )
    
    # Memory management
    st.subheader("Memory Management")
    max_history = st.slider(
        "Max Conversation Turns",
        min_value=1,
        max_value=20,
        value=10,
        help="Maximum number of conversation turns to keep in memory"
    )
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat area
st.subheader("Chat")

# Display greeting message if chat is empty
if not st.session_state.messages:
    display_chat_message("assistant", st.session_state.greeting)

# Display chat history
for message in st.session_state.messages:
    display_chat_message(message["role"], message["content"])

# User input
user_input = create_chat_input("Type your message here...")

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
    
    # Add system prompt
    messages.append({"role": "system", "content": system_prompt})
    
    # Add limited chat history (for memory management)
    history_limit = max_history * 2  # Each turn has 2 messages (user + assistant)
    for message in st.session_state.messages[-history_limit:]:
        messages.append(message)
    
    # Create placeholder for streaming response
    response_placeholder = st.empty()
    
    # Get streaming response if enabled
    if stream:
        with st.spinner("Thinking..."):
            stream_obj = get_streaming_response(
                messages=messages,
                model=model,
                temperature=temperature
            )
            
            # Display streaming response
            response = display_streaming_response(stream_obj, response_placeholder)
    else:
        # Display a spinner while generating response
        with st.spinner("Thinking..."):
            response = get_claude_response(
                messages=messages,
                model=model,
                temperature=temperature
            )
            response_placeholder.markdown(response)
    
    # Add assistant response to chat
    add_message_to_history("assistant", response)
    
    # Clear input field
    st.rerun()

# Code explanation
with st.expander("See Code Explanation"):
    st.markdown("""
    ### Key Advanced Features
    
    1. **Streaming Responses**:
       - Uses the Claude streaming API for a more natural chat experience
       - Responses appear incrementally, simulating real-time typing
       - Provides immediate feedback to the user
       
    2. **Memory Management**:
       - Limits conversation history to a configurable number of turns
       - Prevents context window overflows with large conversation histories
       - Optimizes token usage for API calls
       
    3. **Persona System**:
       - Pre-defined system prompt templates for different assistant personas
       - Custom persona option for user-defined behavior
       - Consistent assistant identity across conversations
       
    4. **UI Enhancements**:
       - Customizable greeting message
       - Toggle between streaming and non-streaming modes
       - More configuration options in the sidebar
       
    5. **Component Reuse**:
       - Leverages shared UI components from the `utils` module
       - Demonstrates how to build modular Streamlit applications
    """)

# Additional tips
st.warning("""
**Implementation Notes**:
- Streaming responses require handling the Claude API differently than standard responses
- Memory management is crucial for long conversations to avoid context window limits
- Consider adding conversation export/import features for production applications
- For real applications, add proper authentication and rate limiting
""") 