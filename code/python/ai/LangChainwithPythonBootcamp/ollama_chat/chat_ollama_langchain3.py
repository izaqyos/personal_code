from langchain.chains import ConversationChain
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# --- Configuration ---

base_url = "http://localhost:11434"
model_name = "llama2" 

system_message = "You are a teenage girl. You enjoy listening to hard rock music, watching horror movies, and talking about your favorite bands and films."

# --- Initialization ---

print("Initializing Ollama model ...")
llm = Ollama(base_url=base_url, model=model_name)
memory = ConversationBufferMemory()

# Prompt Templates
system_message_prompt = SystemMessagePromptTemplate.from_template(
    system_message
)
human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")

chat_prompt_template = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

# Conversation Chain
conversation = ConversationChain(
    llm=llm, 
    memory=memory,
    prompt=chat_prompt_template
)

# --- Chat Loop ---

print("\nStart chatting! Type 'exit' to quit.")
while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    response = conversation.predict(question=question)
    print(f"AI: {response}")
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# --- Configuration ---

base_url = "http://localhost:11434"
model_name = "llama2" 

system_message = "You are a teenage girl. You enjoy listening to hard rock music, watching horror movies, and talking about your favorite bands and films."

# --- Initialization ---

print("Initializing Ollama model ...")
llm = Ollama(base_url=base_url, model=model_name)
memory = ConversationBufferMemory()

# Prompt Templates
system_message_prompt = SystemMessagePromptTemplate.from_template(
    system_message
)
human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")

chat_prompt_template = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

# Conversation Chain
conversation = ConversationChain(
    llm=llm, 
    memory=memory,
    prompt=chat_prompt_template
)

# --- Chat Loop ---

print("\nStart chatting! Type 'exit' to quit.")
while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    response = conversation.predict(question=question)
    print(f"AI: {response}")

