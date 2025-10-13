import os
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from langchain_openai import ChatOpenAI

# Install required packages
# pip install crewai langchain langchain-openai

os.environ["OPENAI_API_KEY"] = "NA"

# Llama3:8b model
ollama_model = 'ollama/llama3.2'
llm = ChatOpenAI(
    model = ollama_model,
    base_url = "http://localhost:11434/v1"
)


product_owner = Agent(
  role='Product Owner',
  goal='Define the product requirements for a simple todo list management application in NodeJS.',
  backstory=dedent("""
    You are an experienced Product Owner with a strong understanding of user needs and market trends.
    You are responsible for defining clear and concise product requirements that can be easily understood by the development team.
    You will focus on the core features of a todo list application.
  """),
  verbose=True,
  allow_delegation=False,
  llm=llm
)

software_architect = Agent(
  role='Software Architect',
  goal='Translate product requirements into technical specifications and high-level architecture.',
  backstory=dedent("""
    You are a skilled Software Architect with expertise in designing scalable and maintainable web applications.
    You are responsible for creating a robust architecture that meets the product requirements and follows best practices.
    You will define the classes, their relationships, configurations, and the overall structure of the application.
  """),
  verbose=True,
  allow_delegation=True,
  llm=llm
)

senior_developer_1 = Agent(
  role='Senior Software Developer 1',
  goal='Implement specific components of the application based on the architect\'s design.',
  backstory=dedent("""
    You are a Senior Software Developer with a strong background in NodeJS and backend development.
    You are responsible for writing clean, efficient, and well-documented code.
    You will focus on implementing specific modules as assigned by the architect.
  """),
  verbose=True,
  allow_delegation=True,
  llm=llm
)

senior_developer_2 = Agent(
  role='Senior Software Developer 2',
  goal='Implement specific components of the application based on the architect\'s design.',
  backstory=dedent("""
    You are a Senior Software Developer with a strong background in NodeJS and backend development.
    You are responsible for writing clean, efficient, and well-documented code.
    You will focus on implementing specific modules as assigned by the architect.
  """),
  verbose=True,
  allow_delegation=True,
  llm=llm
)

junior_developer = Agent(
  role='Junior Software Developer',
  goal='Assist senior developers in implementing the application and learn from the process.',
  backstory=dedent("""
    You are a Junior Software Developer eager to learn and contribute to the project.
    You will work under the guidance of senior developers and assist them in various coding tasks.
    You are responsible for writing code, fixing bugs, and documenting your work.
  """),
  verbose=True,
  allow_delegation=False,
  llm=llm
)

qa_engineer = Agent(
  role='Quality Assurance Engineer',
  goal='Define the testing scope and write unit tests to ensure the quality of the application.',
  backstory=dedent("""
    You are a detail-oriented QA Engineer with experience in testing web applications.
    You are responsible for identifying test cases, writing unit tests, and ensuring that the application meets the quality standards.
    You will use testing frameworks like Jest to implement your tests.
  """),
  verbose=True,
  allow_delegation=False,
  llm=llm
)

code_reviewer = Agent(
    role="Senior Code Reviewer",
    goal="""
        To thoroughly review code, provide specific, actionable feedback, 
        and identify any errors, bugs, or style violations without human intervention.
        Ensure the code is optimized, efficient, and follows best practices.
        """,
    backstory="""
        You are a meticulous Senior Code Reviewer with years of experience 
        in software development. You are known for your attention to detail, 
        your ability to spot subtle errors, and your deep understanding of 
        coding best practices. Your feedback is always constructive and aimed 
        at improving the overall quality of the code.
        """,
    verbose=True,
    allow_delegation=False,
    llm=llm,  # Assuming you have an llm defined
)

# Define the tasks
task_product_requirements = Task(
  description=dedent("""
    ## Define Product Requirements
    Define the product requirements for a simple todo list management application.
    The application should allow users to:
      - Create new todo items.
      - Mark todo items as complete.
      - View a list of all todo items.
      - View a list of incomplete todo items.
      - View a list of completed todo items.
      - Delete todo items.

    Consider the following aspects:
      - User interface (basic command-line interface for simplicity).
      - Data storage (in-memory for this example).
      - Error handling.
      - User experience.

    Your final answer must be a comprehensive document outlining the product requirements.
  """),
  agent=product_owner,
  expected_output="A detailed document outlining the product requirements for the todo list application, including features, user interface considerations, data storage approach, error handling, and user experience guidelines."
)

task_architecture_design = Task(
  description=dedent("""
    ## Design Application Architecture
    Based on the product requirements, design the high-level architecture of the todo list application.
    
    Define the following:
      - Classes and their responsibilities.
      - Relationships between classes.
      - Configuration details (if any).
      - Data models.
      - API endpoints (if any, although we are using a command-line interface).
      - Overall structure of the application.
      - Technology stack (NodeJS, Express if needed, etc.).
      - Libraries to be used.

    Your final answer must be a detailed document describing the architecture of the application, ready to be implemented by the developers.
  """),
  agent=software_architect,
  expected_output="A detailed document outlining the technical architecture of the application, including classes, methods, configuration, data models, and overall structure."
)

task_divide_work = Task(
    description=dedent("""
      ## Divide the work between developers
      Divide the implementation work between the three developers based on the architecture designed.

      Assign specific classes or modules to each developer.
      Ensure that the workload is balanced and that dependencies between tasks are considered.
      Provide clear instructions for each developer on what they need to implement.
    """),
    agent=software_architect,
    expected_output="A clear work breakdown structure assigning specific tasks to each developer with dependencies and instructions."
)

task_implement_core_module = Task(
  description=dedent("""
    ## Implement Core Module: TodoItem and TodoList
    Implement the core module of the application, including the TodoItem and TodoList classes.

    **TodoItem Class:**
      - Properties: id, title, completed.
      - Methods: constructor, markAsComplete(), markAsIncomplete(), toString().

    **TodoList Class:**
      - Properties: items (list of TodoItems).
      - Methods:
        - constructor
        - addItem(title) -> adds a new TodoItem.
        - findItem(id) -> returns a TodoItem by id.
        - markItemAsComplete(id).
        - markItemAsIncomplete(id).
        - deleteItem(id).
        - getAllItems() -> returns all items.
        - getIncompleteItems() -> returns incomplete items.
        - getCompletedItems() -> returns completed items.
        - toString() -> returns a string representation of all items.
    
    Implement error handling for invalid inputs and non-existent items.

    Write the code in `todo_module.js`.

    Your final answer must be the full code for `todo_module.js`, ready to be reviewed and tested.
  """),
  agent=senior_developer_1,
  expected_output="Complete, functional, and well-documented code for the TodoItem and TodoList classes in a file named `todo_module.js`."
)

task_implement_app_logic = Task(
  description=dedent("""
    ## Implement Application Logic: App class
    Implement the main application logic in the App class.

    **App Class:**
      - Properties: todoList (an instance of TodoList).
      - Methods:
        - constructor
        - run() -> starts the main application loop.
        - showMenu() -> displays the main menu.
        - handleMenuChoice(choice) -> handles user input from the menu.
        - Implement methods to handle each menu option:
          - Add a new todo item.
          - Mark a todo item as complete.
          - Mark a todo item as incomplete.
          - View all todo items.
          - View incomplete todo items.
          - View completed todo items.
          - Delete a todo item.
          - Exit the application.

    Write the code in `app.js`.
    Ensure to use the `todo_module.js` created by the other developer.

    Your final answer must be the full code for `app.js`, ready to be reviewed and integrated.
  """),
  agent=senior_developer_2,
  expected_output="Complete, functional, and well-documented code for the App class in a file named `app.js`."
)

task_implement_data_storage = Task(
  description=dedent("""
    ## Implement Data Storage:
    Implement a simple in-memory data storage mechanism using an array to store todo items.
    Enhance the TodoList class to interact with this data storage.

    **TodoList Class (Enhancements):**
      - Use an array `items` to store TodoItem instances.
      - Modify the methods to work with the array:
        - addItem(title)
        - findItem(id)
        - markItemAsComplete(id)
        - markItemAsIncomplete(id)
        - deleteItem(id)
        - getAllItems()
        - getIncompleteItems()
        - getCompletedItems()

    Write the code in `todo_module.js` (you will be modifying the existing file).

    Your final answer must be the updated code for `todo_module.js` with in-memory data storage, ready to be reviewed and integrated.
  """),
  agent=junior_developer,
  expected_output="Complete and functional code modifications in `todo_module.js` implementing basic in-memory data storage."
)

task_define_test_scope = Task(
  description=dedent("""
    ## Define Test Scope and Write Unit Tests
    Define the testing scope for the todo list application and write unit tests.

    **Testing Scope:**
      - Identify the classes and methods that need to be tested.
      - Define the test cases for each method, including positive and negative scenarios.
      - Focus on unit testing the TodoItem, TodoList and App classes.

    **Unit Tests:**
      - Write unit tests using a testing framework like Jest.
      - Ensure that each test case is independent and focused on a specific unit of code.
      - Cover all critical methods and edge cases.
      - Write at least 10 unit tests.

    Write the tests in `test.js`.

    Your final answer must be a comprehensive test suite in `test.js` ready to be executed.
  """),
  agent=qa_engineer,
  expected_output="A document outlining the testing scope and a complete set of unit tests in `test.js`."
)

task_review_core_module = Task(
    description=dedent(
        """
        ## Review Code: `todo_module.js`
        Review the code in `todo_module.js` implemented by the Senior Developer 1.

        Check for the following:
          - **Code correctness and adherence to requirements.**
          - **Code style and readability (e.g., consistent indentation, naming conventions).**
          - **Error handling (e.g., handling of invalid inputs, edge cases).**
          - **Comments and documentation (clarity and completeness).**
          - **Code efficiency and potential optimizations.**
          - **Adherence to SOLID principles.**
          - **Security vulnerabilities.**

        Provide specific, actionable feedback to the developer. 
        Report any bugs, errors, or areas of improvement you find.
        Your feedback should be comprehensive and detailed. 
        Do not ask for any human input.
        """
    ),
    agent=code_reviewer,
    expected_output="A comprehensive code review document with detailed feedback and suggestions for improvement for `todo_module.js`."
)

task_review_app_logic = Task(
  description=dedent("""
    ## Review Code: `app.js`
    Review the code in `app.js` implemented by the Senior Developer 2.

    Check for the following:
      - Code correctness and functionality.
      - Code style and readability.
      - Error handling.
      - Comments and documentation.
      - Potential improvements.

    Provide specific, actionable feedback to the developer. If you find errors ask for clarification, you can use the human input tool.

    Your final answer must be a detailed code review report with specific feedback and suggestions for improvement.
  """),
  agent=code_reviewer,
  context=[task_implement_app_logic],
  expected_output="A comprehensive code review document with detailed feedback and suggestions for improvement for `app.js`."
)

task_review_tests = Task(
  description=dedent("""
    ## Review Tests: `test.js`
    Review the unit tests in `test.js` implemented by the QA Engineer.

    Check for the following:
      - Test coverage and completeness.
      - Test correctness and effectiveness.
      - Test style and readability.
      - Potential improvements and missing test cases.

    Provide specific, actionable feedback to the QA Engineer.

    Your final answer must be a detailed review report of the test suite with specific feedback and suggestions for improvement.
  """),
  agent=code_reviewer,
  context=[task_define_test_scope],
  expected_output="A comprehensive review document of the test suite with detailed feedback and suggestions for improvement for `test.js`."
)

todo_crew = Crew(
  agents=[
    product_owner,
    software_architect,
    senior_developer_1,
    senior_developer_2,
    junior_developer,
    qa_engineer,
    code_reviewer
  ],
  tasks=[
    task_product_requirements,
    task_architecture_design,
    task_divide_work,
    task_implement_core_module,
    task_implement_app_logic,
    task_implement_data_storage,
    task_define_test_scope,
    task_review_core_module,
    task_review_app_logic,
    task_review_tests
  ],
  process=Process.sequential,  
  verbose=True
)

# Kickoff the project
result = todo_crew.kickoff()

print("######################")
print("Project Result:")
print(result)
