# AI Agents

LLMs that can take actions and use tools.

## Overview

Agents use LLMs to decide which actions to take based on observations.

```
User Query → LLM decides action → Execute tool → Observe result → 
            → LLM decides next action → ... → Final answer
```

## LangChain Agents

### Basic Agent Setup
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.llms import OpenAI
from langchain import hub

# Define tools
def search(query):
    return f"Search results for: {query}"

def calculator(expression):
    return str(eval(expression))

tools = [
    Tool(
        name="Search",
        func=search,
        description="Useful for finding information online"
    ),
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math calculations"
    )
]

# Create agent
llm = OpenAI(temperature=0)
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# Run
result = agent_executor.invoke({"input": "What is 15% of 250?"})
```

### Built-in Tools
```python
from langchain.agents import load_tools

tools = load_tools(
    ["serpapi", "llm-math", "wikipedia"],
    llm=llm
)
```

### Custom Tools
```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="City name")
    unit: str = Field(default="celsius", description="Temperature unit")

class WeatherTool(BaseTool):
    name = "weather"
    description = "Get current weather for a location"
    args_schema = WeatherInput
    
    def _run(self, location: str, unit: str = "celsius"):
        # Call weather API
        return f"Weather in {location}: 20°{unit[0].upper()}"
    
    async def _arun(self, location: str, unit: str = "celsius"):
        return self._run(location, unit)
```

## OpenAI Function Calling Agents

```python
from langchain.agents import create_openai_functions_agent
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

## ReAct Pattern

Reasoning and Acting in an interleaved manner.

```
Thought: I need to find the population of France
Action: Search
Action Input: "population of France 2024"
Observation: France has approximately 68 million people
Thought: Now I have the answer
Final Answer: France has approximately 68 million people
```

```python
from langchain.agents import create_react_agent

# ReAct prompt
react_prompt = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}"""

agent = create_react_agent(llm, tools, react_prompt)
```

## CrewAI

Multi-agent collaboration framework.

```python
from crewai import Agent, Task, Crew

# Define agents
researcher = Agent(
    role='Research Analyst',
    goal='Find and analyze relevant information',
    backstory='Expert at finding and synthesizing information',
    tools=[search_tool],
    llm=llm
)

writer = Agent(
    role='Content Writer',
    goal='Write clear and engaging content',
    backstory='Skilled technical writer',
    llm=llm
)

# Define tasks
research_task = Task(
    description='Research the topic: {topic}',
    expected_output='Detailed research findings',
    agent=researcher
)

writing_task = Task(
    description='Write an article based on the research',
    expected_output='Well-written article',
    agent=writer,
    context=[research_task]  # Depends on research
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

# Execute
result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
```

## LangGraph

Stateful multi-agent orchestration.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next: str

# Define nodes (agents)
def researcher_node(state):
    # Research logic
    return {"messages": ["Research findings..."]}

def writer_node(state):
    # Writing logic
    return {"messages": ["Written content..."]}

def router(state):
    # Decide next step
    if "research done" in state["messages"][-1]:
        return "writer"
    return "end"

# Build graph
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("researcher")
workflow.add_conditional_edges(
    "researcher",
    router,
    {"writer": "writer", "end": END}
)
workflow.add_edge("writer", END)

app = workflow.compile()

# Run
result = app.invoke({"messages": ["Research AI trends"]})
```

## Agent Patterns

### Sequential
```
Agent A → Agent B → Agent C → Output
```

### Hierarchical
```
Manager Agent
    ├── Worker A
    ├── Worker B
    └── Worker C
```

### Collaborative
```
Agent A ←→ Agent B
    ↕         ↕
Agent C ←→ Agent D
```

## Memory and State

### Conversation Memory
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)
```

### Long-term Memory
```python
from langchain.memory import VectorStoreRetrieverMemory

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
memory = VectorStoreRetrieverMemory(retriever=retriever)
```

## Error Handling

```python
from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=10,  # Prevent infinite loops
    max_execution_time=60,  # Timeout in seconds
    handle_parsing_errors=True,  # Handle LLM output parsing errors
    return_intermediate_steps=True  # Debug
)

try:
    result = agent_executor.invoke({"input": query})
except Exception as e:
    print(f"Agent error: {e}")
```

## Complete Agent Example

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain import hub

# Tools
def search_database(query: str) -> str:
    """Search internal database for information."""
    return f"Database results for: {query}"

def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return f"Email sent to {to}"

tools = [
    Tool(
        name="search_database",
        func=search_database,
        description="Search the company database for information"
    ),
    Tool(
        name="send_email",
        func=send_email,
        description="Send an email. Input should be 'to|subject|body'"
    )
]

# Agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, tools, prompt)

# Memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Executor
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    max_iterations=5
)

# Use
result = executor.invoke({
    "input": "Find John's email in the database and send him a meeting reminder"
})
print(result["output"])
```

## Quick Reference

```python
# LangChain Agent
tools = [Tool(name, func, description)]
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent, tools, verbose=True)
result = executor.invoke({"input": query})

# CrewAI
agent = Agent(role, goal, backstory, tools, llm)
task = Task(description, expected_output, agent)
crew = Crew(agents, tasks)
result = crew.kickoff(inputs)

# Key patterns
- ReAct: Reason → Act → Observe → Repeat
- Plan and Execute: Plan first, then execute steps
- Hierarchical: Manager delegates to workers
```

## Related Topics
- [LLMs](llms.md)
- [LangChain](langchain.md)
- [RAG](rag.md)
