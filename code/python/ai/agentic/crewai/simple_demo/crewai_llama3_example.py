from crewai import Agent, Task, Crew, Process
from langchain_ollama import OllamaLLM

writer = Agent(
  role='Senior Writer',
  goal='Write compelling short stories',
  backstory="""You are a renowned writer known for your captivating stories.
  You have a knack for creating engaging narratives that leave readers wanting more.""",
  verbose=True,
  allow_delegation=False,
  llm=OllamaLLM(model="ollama/llama3"),
)

editor = Agent(
  role='Editor',
  goal='Review and refine stories to ensure they are well-written and engaging',
  backstory="""You are a meticulous editor with an eye for detail.
  You ensure that every story is polished to perfection.""",
  verbose=True,
  allow_delegation=True,
  llm=OllamaLLM(model="ollama/llama3"),
)

# Define tasks
task_write = Task(
  description='Write a short story about a robot who discovers he has feelings. The story should be no longer than 500 words.',
  agent=writer,
  expected_output="A compelling short story, no longer than 500 words, about a robot discovering its feelings."
)

task_review = Task(
  description='Review the story and provide feedback on how to improve it. Make sure to check for grammar, flow, and engagement. Suggest to make it no longer than 300 words',
  agent=editor,
  expected_output="Constructive feedback on the story with specific suggestions for improvement, focusing on grammar, flow, and engagement. The feedback should aim to reduce the story to under 300 words."
)

# Create a crew
crew = Crew(
  agents=[writer, editor],
  tasks=[task_write, task_review],
  process=Process.sequential, # Agents work on tasks one after another
  verbose=1 # You can set it to 1 or 2 to different logging levels
)

# Run the crew
result = crew.kickoff()

print("######################")
print("Crew Work Result:")
print(result)
