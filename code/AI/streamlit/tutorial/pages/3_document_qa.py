import streamlit as st
import sys
import os
import pandas as pd
import tempfile

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_helper import get_claude_response, format_messages
from utils.ui_components import display_chat_message

# Page configuration
st.set_page_config(
    page_title="Document Q&A | AI Assistant Tutorial",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 Document Q&A Interface")

# Description
st.markdown("""
This example demonstrates how to build a document question-answering interface.
It lets users upload a document (text, CSV, or PDF) and ask questions about it.
The AI assistant analyzes the document and provides relevant answers.

This pattern is useful for:
- Customer support with documentation
- Research assistance
- Data analysis and interpretation
- Knowledge base querying
""")

# Add a divider
st.divider()

# Initialize session state
if "doc_content" not in st.session_state:
    st.session_state.doc_content = None
if "doc_qa_messages" not in st.session_state:
    st.session_state.doc_qa_messages = []

# Sidebar configuration
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
        value=0.3,
        step=0.1,
        help="Lower temperatures are better for factual Q&A"
    )
    
    # System prompt settings
    st.subheader("System Prompt")
    system_prompt_template = st.text_area(
        "System Instructions",
        value="You are a document analysis assistant. Answer questions about the following document content. Only use information from the document to answer questions. If the answer is not in the document, say so.",
        height=100
    )
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.doc_qa_messages = []
        st.rerun()

# Document upload section
st.subheader("Upload Document")
uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "pdf"])

# Process uploaded file
if uploaded_file is not None:
    # Display file info
    st.write(f"Uploaded: {uploaded_file.name} ({uploaded_file.type})")
    
    # Process different file types
    if uploaded_file.type == "text/plain":
        # Text files
        content = uploaded_file.read().decode()
        st.session_state.doc_content = content
        
        # Preview
        with st.expander("Document Preview"):
            st.text(content[:1000] + ("..." if len(content) > 1000 else ""))
            
    elif uploaded_file.type == "text/csv":
        # CSV files
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.doc_content = df.to_string()
            
            # Preview
            with st.expander("Document Preview (CSV)"):
                st.dataframe(df.head())
                
        except Exception as e:
            st.error(f"Error processing CSV: {str(e)}")
            
    elif uploaded_file.type == "application/pdf":
        # PDF files - simplified, would need PyPDF2 or similar in real implementation
        st.warning("PDF support is simulated in this example. Install PyPDF2 for real PDF processing.")
        
        # Simulated content
        st.session_state.doc_content = f"[This is simulated content for {uploaded_file.name}. In a real app, you would use PyPDF2 or a similar library to extract text from PDFs.]"
        
        # Fake preview
        with st.expander("Document Preview (PDF)"):
            st.text(st.session_state.doc_content)
    
    # Document stats
    if st.session_state.doc_content:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Characters", len(st.session_state.doc_content))
        with col2:
            st.metric("Words", len(st.session_state.doc_content.split()))
        with col3:
            st.metric("Lines", st.session_state.doc_content.count('\n') + 1)

# Q&A Interface
st.subheader("Ask Questions")

# Disable Q&A if no document
if st.session_state.doc_content is None:
    st.info("Please upload a document first to ask questions about it.")
    st.stop()

# Display chat history
if st.session_state.doc_qa_messages:
    for message in st.session_state.doc_qa_messages:
        display_chat_message(message["role"], message["content"])

# User input
user_question = st.text_input("Ask a question about the document:")
submit_question = st.button("Ask")

# Process question
if submit_question and user_question:
    # Add user question to chat
    st.session_state.doc_qa_messages.append({"role": "user", "content": user_question})
    
    # Display user question
    display_chat_message("user", user_question)
    
    # Prepare prompt with document content
    prompt = f"{system_prompt_template}\n\nDocument content:\n{st.session_state.doc_content}\n\nQuestion: {user_question}"
    
    # Prepare messages for API call
    messages = [
        {"role": "system", "content": prompt},
    ]
    
    # Add previous Q&A context if available (last 3 exchanges)
    for message in st.session_state.doc_qa_messages[-6:]:  # 3 exchanges = 6 messages
        if message["role"] != "system":
            messages.append(message)
    
    # Get response
    with st.spinner("Analyzing document..."):
        response = get_claude_response(
            messages=messages,
            model=model,
            temperature=temperature
        )
    
    # Add response to chat
    st.session_state.doc_qa_messages.append({"role": "assistant", "content": response})
    
    # Display response
    display_chat_message("assistant", response)
    
    # Rerun to clear input
    st.rerun()

# Code explanation
with st.expander("See Code Explanation"):
    st.markdown("""
    ### Key Features of Document Q&A
    
    1. **Document Processing**:
       - Handles multiple file formats (text, CSV, PDF)
       - Extracts content for AI analysis
       - Shows document previews and statistics
       
    2. **Prompt Engineering**:
       - Combines system instructions, document content, and user question
       - Uses lower temperature for more factual responses
       - Maintains conversational context for follow-up questions
       
    3. **User Interface**:
       - Clear separation between document upload and Q&A sections
       - Interactive chat interface for questions and answers
       - Document preview with expandable sections
       
    4. **Implementation Notes**:
       - For larger documents, consider chunking and embeddings-based retrieval
       - PDF processing requires additional libraries (PyPDF2, pdf2text, etc.)
       - For production use, add document caching and more robust error handling
    """)

# Implementation tips
st.info("""
**Tips for Production Document Q&A Systems**:

1. For large documents, implement a vector database with embeddings
2. Use retrieval-augmented generation (RAG) for more accurate answers
3. Consider adding document summarization as a first step
4. Implement document chunking strategies for better context management
5. Add document highlighting to show where answers come from
""") 