from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "NA"
model_name = "ollama/llama3.2" 
#model_name = "ollama/deepseek-r1:32b"  # don't run this, it's too slow

# Llama3:8b model
llm = ChatOpenAI(
    model = model_name,
    base_url = "http://localhost:11434/v1"
)

# Math Professor Agent
general_agent = Agent(
  role = "Math Professor",
  goal = """ Provide the solution to the students that are asking for mathematical
           questions and give them the answer.""",
  backstory = """ You are an excellent math professor that likes to solve math questions in a way that everyone can understand your solution""",
  allow_delegation = False,
  verbose = True,
  llm = llm
)

# Task
task = Task(description="""what is 3 + 5""",
            expected_output="A mathematically accurate solution to the student math question along with the way it was solved",
            agent = general_agent)

crew = Crew(
  agents=[general_agent],
  tasks=[task],
  verbose=True
)
result = crew.kickoff()

print(result)
