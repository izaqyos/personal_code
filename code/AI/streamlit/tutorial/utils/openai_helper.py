"""
Helper functions for interacting with the OpenAI API.
"""
import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(messages, model="gpt-4-turbo", temperature=0.7, max_tokens=None):
    """
    Get a response from the OpenAI API.
    
    Args:
        messages (list): List of message objects
        model (str): Model to use
        temperature (float): Temperature for generation
        max_tokens (int): Maximum tokens to generate
        
    Returns:
        str: Generated response text
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return "I'm sorry, I encountered an error. Please try again."

def get_streaming_response(messages, model="gpt-4-turbo", temperature=0.7, max_tokens=None):
    """
    Get a streaming response from the OpenAI API.
    
    Args:
        messages (list): List of message objects
        model (str): Model to use
        temperature (float): Temperature for generation
        max_tokens (int): Maximum tokens to generate
        
    Returns:
        generator: Stream of response chunks
    """
    try:
        stream = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        return stream
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None

def display_streaming_response(stream, placeholder):
    """
    Display a streaming response in the given placeholder.
    
    Args:
        stream: Stream from OpenAI API
        placeholder: Streamlit placeholder to update
    
    Returns:
        str: Complete response text
    """
    if not stream:
        return "I'm sorry, I encountered an error. Please try again."
        
    # Collect the full response while displaying chunks
    full_response = ""
    
    # Display the streaming response
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            placeholder.markdown(full_response + "▌")
    
    # Display the final response without the cursor
    placeholder.markdown(full_response)
    
    return full_response

def format_messages(user_input, chat_history=None, system_prompt=None):
    """
    Format messages for the OpenAI API.
    
    Args:
        user_input (str): User input text
        chat_history (list): Previous messages
        system_prompt (str): System prompt
        
    Returns:
        list: Formatted messages
    """
    messages = []
    
    # Add system prompt if provided
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add chat history if provided
    if chat_history:
        messages.extend(chat_history)
    
    # Add user input
    messages.append({"role": "user", "content": user_input})
    
    return messages 