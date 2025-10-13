from abc import abstractmethod
from typing import Optional, List 
import langchain.chains as chains
from langchain.llms import BaseLLM
from langchain.prompts import PromptTemplate
import requests
#import pdb


class RestLLM(BaseLLM):
    def _llm_type(self) -> str:
        return "ollama-rest"  # Or a different descriptive name

    def _generate(self, text: str, stop: Optional[List[str]] = None) -> str:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",  # Include the required model information
                "prompt": text,
                "stop": stop  
            }
        )

        if response.status_code == 200:
            # Assuming your response contains the generated text with a key like "output", adjust if necessary
            print(response.json)
            #return response.json()["output"] 
        else:
            raise Exception(f"Error calling REST endpoint: {response.text}")

    #def _generate(self, text: str, stop: Optional[List[str]] = None) -> str:
    #    response = requests.post(
    #        "http://localhost:11434/generate",
    #        json={
    #            "text": text,
    #            "stop": stop  # Include the stop sequence if provided
    #        }
    #    )

    #    if response.status_code == 200:
    #        return response.json()["output"]
    #    else:
    #        raise Exception(f"Error calling REST endpoint: {response.text}")

    def _call(self, text: str) -> str:
        return self._generate(text) 

# Continue with the same prompt template as before... 
prompt_template = """
The following is a friendly chat between a human and an AI.
Human: {text}
AI: {output}
"""
prompt = PromptTemplate(input_variables=["text"], template=prompt_template)

llm = RestLLM()  # Use our custom REST-based LLM

# Define the conversation flow
def chat_with_llama(text):
  #pdb.set_trace()
  response = llm(prompt.format(text=text, output=""))
  return response

# Start the chat loop (you could integrate this into a web interface, etc.)
while True:
  user_input = input("You: ")
  bot_response = chat_with_llama(user_input)
  print(f"Bot: {bot_response}") 