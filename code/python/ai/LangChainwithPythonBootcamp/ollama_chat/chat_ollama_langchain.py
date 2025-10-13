"""
pip install langchain
pip install langchain-community # For ChatOllama
"""

from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage

# Initialize the ChatOllama model (adjust the model name as needed)
chat_model = ChatOllama(model="llama2")

# Create a conversation history to track messages
chat_history = []

while True:
    human_input = input("You: ")
    
    # Break the loop when user enters "exit"
    if human_input.lower() == "exit":
        break

    # Add the human message to the chat history
    chat_history.append(HumanMessage(content=human_input))
    
    # Get the AI's response
    ai_response = chat_model(chat_history)
    
    # Add the AI's message to the chat history
    chat_history.append(AIMessage(content=ai_response.content))
    
    # Print the AI's response
    print(f"AI: {ai_response.content}")
