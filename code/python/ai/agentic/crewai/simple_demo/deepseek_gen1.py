from crewai import Agent, Task, Crew
import ollama

# Define the LLM function to interact with the local model
def query_llm(prompt):
    response = ollama.generate(model='deepseek-r1:32b', prompt=prompt)
    return response['response']

# Define the Product Owner Agent
product_owner = Agent(
    role='Product Owner',
    goal='Define the requirements for a simple todo list management application in Node.js',
    backstory='You are a product owner with a clear vision of what the application should do.',
    tools=[query_llm],
    verbose=True
)

# Define the Software Architect Agent
software_architect = Agent(
    role='Software Architect',
    goal='Convert product requirements into technical requirements and create high-level architecture, classes, and configuration.',
    backstory='You are an experienced software architect who can translate business needs into technical solutions.',
    tools=[query_llm],
    verbose=True
)

# Define the Software Developer Agents
developer1 = Agent(
    role='Software Developer 1',
    goal='Implement the classes and write the code based on the architect\'s breakdown.',
    backstory='You are a skilled developer with expertise in Node.js and backend development.',
    tools=[query_llm],
    verbose=True
)

developer2 = Agent(
    role='Software Developer 2',
    goal='Implement the classes and write the code based on the architect\'s breakdown.',
    backstory='You are a skilled developer with expertise in Node.js and backend development.',
    tools=[query_llm],
    verbose=True
)

developer3 = Agent(
    role='Software Developer 3',
    goal='Implement the classes and write the code based on the architect\'s breakdown.',
    backstory='You are a skilled developer with expertise in Node.js and backend development.',
    tools=[query_llm],
    verbose=True
)

# Define the QA Engineer Agent
qa_engineer = Agent(
    role='QA Engineer',
    goal='Define the test scope and implement unit tests for the application.',
    backstory='You are a meticulous QA engineer who ensures the quality of the code through rigorous testing.',
    tools=[query_llm],
    verbose=True
)

# Define the Code Reviewer Agent
code_reviewer = Agent(
    role='Code Reviewer',
    goal='Review the code and provide feedback to the developers.',
    backstory='You are an experienced code reviewer who ensures that the code meets the highest standards.',
    tools=[query_llm],
    verbose=True
)

# Define the Tasks
product_requirements_task = Task(
    description='Define the requirements for a simple todo list management application in Node.js.',
    agent=product_owner,
    expected_output='A detailed list of product requirements.'
)

technical_requirements_task = Task(
    description='Convert the product requirements into technical requirements and create the high-level architecture, classes, and configuration.',
    agent=software_architect,
    expected_output='A technical document outlining the architecture, classes, and configuration.'
)

development_task1 = Task(
    description='Implement the classes and write the code based on the architect\'s breakdown.',
    agent=developer1,
    expected_output='A set of implemented classes and code.'
)

development_task2 = Task(
    description='Implement the classes and write the code based on the architect\'s breakdown.',
    agent=developer2,
    expected_output='A set of implemented classes and code.'
)

development_task3 = Task(
    description='Implement the classes and write the code based on the architect\'s breakdown.',
    agent=developer3,
    expected_output='A set of implemented classes and code.'
)

qa_task = Task(
    description='Define the test scope and implement unit tests for the application.',
    agent=qa_engineer,
    expected_output='A set of unit tests and a test scope document.'
)

code_review_task = Task(
    description='Review the code and provide feedback to the developers.',
    agent=code_reviewer,
    expected_output='A code review report with feedback and suggestions for improvement.'
)

# Create the Crew
crew = Crew(
    agents=[product_owner, software_architect, developer1, developer2, developer3, qa_engineer, code_reviewer],
    tasks=[product_requirements_task, technical_requirements_task, development_task1, development_task2, development_task3, qa_task, code_review_task],
    verbose=2
)

# Execute the Crew
result = crew.kickoff()

# Output the result
print("Final Result:")
print(result)
