"""
All of your local models are automatically served on localhost:11434
Run ollama run <name-of-model> to start interacting via the command line directly
"""

from langchain_community.llms import Ollama

llm = Ollama(model="llama2")

def basic_interaction():
    """
    Performs a basic interaction with the language model.

    This function sends a query to the language model to get a joke. The response is printed to the console.
    Then, another query is sent to get another joke. The response is printed to the console in chunks.

    Parameters:
    None

    Returns:
    None
    """
    resp = llm.invoke("Tell me a joke")
    print(resp)

    query = "Why is the sky blue?"
    for chunks in llm.stream(query):
        print(chunks, end="")
    print("")

def generate_api():
    prompts = ["why is the sun so hot?", "who is charlie brown?", "who invented hanoi towers riddle"]
    resp = llm.generate(prompts)
    print(f"Schema: {resp.schema()}")
    print(f"llm_output: {resp.llm_output}")
    print(f"generations: {resp.generations}")
    for i,gen in enumerate(resp.generations):
        print(f"prompt: {prompts[i]} | response: {gen[0].text}")

def main():
    """
    Calls the basic_interaction function.
    """
    #basic_interaction()
    generate_api()

main()