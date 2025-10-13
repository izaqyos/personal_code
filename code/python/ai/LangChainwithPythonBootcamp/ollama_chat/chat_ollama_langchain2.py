from langchain.chains import ConversationChain
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage, SystemMessage

print("Initialize the Ollama model - hard coded to llama3")
ollama_model = Ollama(base_url="http://localhost:11434", model="llama3")

print("Initialize the ConversationBufferMemory")
memory = ConversationBufferMemory()

# System message to define the AI's personality
system_message = SystemMessage(
    content="You are a teenage girl. You enjoy listening to hard rock music, watching horror movies, and talking about your favorite bands and films."
)

print("Initialize the ConversationChain")
conversation_chain = ConversationChain(
    llm=ollama_model,
    verbose=True,  # Optional: Enable verbose output for debugging
    memory=memory
)

# Start the chat loop
while True:
    human_input = input("You: ")
    
    if human_input.lower() == "exit":
        break

    ai_response = conversation_chain.predict(input=human_input)
    
    print(f"AI: {ai_response}")
