import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Assistant Tutorial",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    with open("styles/main.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Try to load CSS, create file if it doesn't exist
try:
    load_css()
except FileNotFoundError:
    os.makedirs("styles", exist_ok=True)
    with open("styles/main.css", "w") as f:
        f.write("""
        .chat-message {
            padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
        .chat-message.user {
            background-color: #f0f2f6;
        }
        .chat-message.assistant {
            background-color: #e6f7ff;
        }
        .chat-message .avatar {
            width: 40px; height: 40px; border-radius: 50%; margin-right: 1rem;
            display: flex; align-items: center; justify-content: center;
        }
        .chat-message .avatar.user {
            background-color: #4285f4;
            color: white;
        }
        .chat-message .avatar.assistant {
            background-color: #34a853;
            color: white;
        }
        .chat-message .message {
            flex-grow: 1;
            word-break: break-word;
        }
        """)
    load_css()

# Main page content
st.title("🤖 Streamlit AI Assistant Tutorial")
st.markdown("""
Welcome to this tutorial on building AI assistants with Streamlit!

Use the sidebar to navigate between different examples:

- **Simple Chat**: Basic chatbot interface
- **Advanced Chat**: Chat with memory and context
- **Document Q&A**: Ask questions about documents
- **Data Visualization**: Visualize data with AI insights

Each example demonstrates different aspects of building AI UIs with Streamlit.
""")

# Show features and capabilities
st.subheader("Key Features Demonstrated")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - 💬 Chat interfaces
    - 📊 Data visualization
    - 📄 Document processing
    - 🧠 Memory and context management
    """)

with col2:
    st.markdown("""
    - 🔑 API key security
    - 🎨 Custom UI components
    - 💾 Session state management
    - 🔄 Streaming responses
    """)

# Instructions
st.subheader("How to Use This Tutorial")
st.info("""
1. Navigate to each example page using the sidebar
2. Explore the code to understand how it works
3. Try modifying the examples to experiment with different features
4. Use these patterns in your own projects
""")

# API keys setup
st.subheader("API Keys Setup")
st.warning("""
Some examples require API keys (like Anthropic Claude). 
Create a `.env` file in the project root with your keys:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
```
""")

# Link to documentation
st.markdown("---")
st.markdown("""
📚 **Resources:**
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [GitHub Repository](https://github.com/yourusername/streamlit-ai-tutorial)
""") 