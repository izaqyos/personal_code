from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "NA"


# Llama3:8b model
ollama_model = 'ollama/llama3.2'
llm = ChatOpenAI(
    model = ollama_model,
    base_url = "http://localhost:11434/v1"
)

researcher = Agent(
    role='Researcher',
    goal=f'Research and summarize news related to a given topic. Use the {ollama_model} model for your research.',
    backstory="""You are an expert researcher, skilled in using search engines and databases to find relevant information.
    You are excellent at finding high quality and up-to-date information. You always double check your sources.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writer = Agent(
    role='Writer',
    goal=f'Write engaging and informative blog posts based on research provided by the Researcher. Use the {ollama_model} model for your writing.',
    backstory="""You are a talented writer with a knack for creating clear, concise, and engaging content.
    You can take complex information and distill it into easily digestible articles.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

editor = Agent(
    role='Editor',
    goal=f'Review and edit blog posts for clarity, grammar, and style. Use the {ollama_model} model for your editing.',
    backstory="""You are a sharp-eyed editor who ensures that every piece of writing is polished to perfection.
    You have a strong command of grammar and style, and you can make any text flow smoothly.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define tasks
research_task = Task(
    description='Find the latest news on the topic of AI, specifically advancements in LLMs capabilities for reasoning and complex problem solving .',
    agent=researcher,
    expected_output="A summary of the latest news and developments in AI ethics, with key points and sources."
)

writing_task = Task(
    description='Write a 500-word blog post about the findings from the research on AI and specifically on LLMs.',
    agent=writer,
    expected_output="A well-written, informative, and engaging 500-word blog post on the topic of AI advancements in LLMs capabilities for reasoning and complex problem solving"
)

review_task = Task(
    description='Review and edit the blog post for clarity, grammar, style, and accuracy. Ensure the post is under 500 words.',
    agent=editor,
    expected_output="A finalized and polished version of the blog post, ready for publication."
)

# Create a crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, review_task],
    process=Process.sequential,  # Run tasks sequentially
    verbose=True
)

# Run the crew
result = crew.kickoff()

print("######################")
print("Crew Work Result:")
print(result)
