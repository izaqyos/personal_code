"""
Reusable UI components for Streamlit applications.
"""
import streamlit as st

def display_chat_message(role, content, avatar=None):
    """
    Display a chat message with the specified role and content.
    
    Args:
        role (str): The role of the message sender ('user' or 'assistant')
        content (str): The message content
        avatar (str, optional): Avatar symbol to display
    """
    with st.container():
        col1, col2 = st.columns([1, 12])
        
        # Set default avatars if none provided
        if not avatar:
            avatar = "👤" if role == "user" else "🤖"
            
        with col1:
            st.markdown(f"""
            <div class="avatar {role}">
                {avatar}
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="chat-message {role}">
                <div class="message">
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_chat_history(chat_history):
    """
    Display the entire chat history.
    
    Args:
        chat_history (list): List of message dictionaries with 'role' and 'content'
    """
    for message in chat_history:
        display_chat_message(message["role"], message["content"])

def initialize_chat_state():
    """
    Initialize session state for chat functionality.
    
    Returns:
        None
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []

def add_message_to_history(role, content):
    """
    Add a message to the chat history in session state.
    
    Args:
        role (str): The role of the message sender ('user' or 'assistant')
        content (str): The message content
    """
    st.session_state.messages.append({"role": role, "content": content})

def create_chat_input(placeholder=None, key="chat_input"):
    """
    Create a chat input field.
    
    Args:
        placeholder (str, optional): Placeholder text for the input field
        key (str): Unique key for the input field
        
    Returns:
        str: User input text
    """
    placeholder = placeholder or "Type your message here..."
    return st.text_area(
        label="",
        placeholder=placeholder,
        key=key,
        max_chars=2000,
        height=100
    )

def create_sidebar_config():
    """
    Create a sidebar with common configuration options.
    
    Returns:
        dict: Configuration options
    """
    with st.sidebar:
        st.subheader("Model Configuration")
        model = st.selectbox(
            "Select Model",
            ["gpt-4-turbo", "gpt-3.5-turbo"],
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
        
        st.subheader("Chat Options")
        stream = st.toggle("Stream responses", value=True)
        memory = st.toggle("Enable memory", value=True)
        
        return {
            "model": model,
            "temperature": temperature,
            "stream": stream,
            "memory": memory
        } 