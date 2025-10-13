"""
Helper functions for interacting with the Anthropic Claude API.
"""
import os
import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic, AsyncAnthropic
import asyncio

# Load environment variables
load_dotenv()

# Set Anthropic API key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic_client = Anthropic(api_key=anthropic_api_key)

def get_claude_response(messages, model="claude-3-sonnet-20240229", temperature=0.7, max_tokens=None):
    """
    Get a response from the Anthropic Claude API.
    
    Args:
        messages (list): List of message objects
        model (str): Model to use
        temperature (float): Temperature for generation
        max_tokens (int): Maximum tokens to generate
        
    Returns:
        str: Generated response text
    """
    try:
        # Convert messages to Anthropic format
        system_prompt = None
        anthropic_messages = []
        
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "system":
                system_prompt = content
            elif role == "user":
                anthropic_messages.append({"role": "user", "content": content})
            elif role == "assistant":
                anthropic_messages.append({"role": "assistant", "content": content})
        
        # Create completion
        response = anthropic_client.messages.create(
            model=model,
            messages=anthropic_messages,
            system=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens or 4096,
        )
        
        return response.content[0].text
    except Exception as e:
        st.error(f"Error calling Anthropic API: {str(e)}")
        return "I'm sorry, I encountered an error. Please try again."

async def _get_streaming_response_async(messages, model="claude-3-sonnet-20240229", temperature=0.7, max_tokens=None):
    """Async helper for streaming responses"""
    async_client = AsyncAnthropic(api_key=anthropic_api_key)
    
    # Convert messages to Anthropic format
    system_prompt = None
    anthropic_messages = []
    
    for message in messages:
        role = message["role"]
        content = message["content"]
        
        if role == "system":
            system_prompt = content
        elif role == "user":
            anthropic_messages.append({"role": "user", "content": content})
        elif role == "assistant":
            anthropic_messages.append({"role": "assistant", "content": content})
    
    # Create streaming completion
    with await async_client.messages.stream(
        model=model,
        messages=anthropic_messages,
        system=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens or 4096,
    ) as stream:
        async for chunk in stream:
            if chunk.type == "content_block_delta" and chunk.delta.type == "text_delta":
                yield chunk.delta.text

def get_streaming_response(messages, model="claude-3-sonnet-20240229", temperature=0.7, max_tokens=None):
    """
    Get a streaming response from the Anthropic Claude API.
    
    Args:
        messages (list): List of message objects
        model (str): Model to use
        temperature (float): Temperature for generation
        max_tokens (int): Maximum tokens to generate
        
    Returns:
        generator: Stream of response chunks
    """
    try:
        # We need to wrap the async generator in a sync generator
        async_gen = _get_streaming_response_async(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Create event loop for async calls if needed
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Return a generator that yields from the async generator
        def sync_generator():
            while True:
                try:
                    # Get next value from async generator
                    next_value = loop.run_until_complete(async_gen.__anext__())
                    yield next_value
                except StopAsyncIteration:
                    break
        
        return sync_generator()
    except Exception as e:
        st.error(f"Error calling Anthropic API: {str(e)}")
        return None

def display_streaming_response(stream, placeholder):
    """
    Display a streaming response in the given placeholder.
    
    Args:
        stream: Stream from Anthropic API
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
        full_response += chunk
        placeholder.markdown(full_response + "▌")
    
    # Display the final response without the cursor
    placeholder.markdown(full_response)
    
    return full_response

def format_messages(user_input, chat_history=None, system_prompt=None):
    """
    Format messages for the Anthropic Claude API.
    
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