# Geo-Political News Analysis with CrewAI and Ollama

This project demonstrates how to build a team of AI agents using **CrewAI** and the **deepseek-r1:32b** model deployed locally via **Ollama**. The team consists of three agents:
1. **Web Scraper Agent**: Fetches the latest geopolitical news headlines.
2. **Geo-Politics Expert Agent**: Summarizes the fetched news into concise reports.
3. **Trends and Shifts Expert Agent**: Analyzes the summarized news to identify geopolitical trends and shifts.

The project is designed to showcase how AI agents can collaborate to process and analyze real-world data effectively.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

The goal of this project is to create a pipeline for analyzing geopolitical news in real-time. The workflow involves:
1. **Fetching News**: A web scraper collects the latest geopolitical headlines from a news website.
2. **Summarizing News**: An AI agent summarizes the headlines into a concise report.
3. **Analyzing Trends**: Another AI agent analyzes the summarized report to identify geopolitical trends and shifts.

The agents are orchestrated using **CrewAI**, and the summarization and analysis tasks are powered by the **deepseek-r1:32b** model deployed locally via **Ollama**.

---

## Architecture

Below is a Mermaid diagram illustrating the architecture of the project:

``` mermaid
flowchart TD
    A[User Input] --> B(Web Scraper Agent)
    B --> C[Fetch News Headlines]
    C --> D(Geo-Politics Expert Agent)
    D --> E[Summarize News]
    E --> F(Trends and Shifts Expert Agent)
    F --> G[Analyze Trends and Shifts]
    G --> H[Output Results]
```


# Installation
Prerequisites
Python 3.8+ : Ensure you have Python installed on your system.
Ollama : Install and run Ollama locally. Deploy the deepseek-r1:32b model:
``` bash
ollama run deepseek-r1:32b
```
Dependencies : Install the required Python libraries:
``` bash
pip install crewai requests beautifulsoup4 ollama
```
# Usage
Clone the repository:
``` bash
git clone https://github.com/yourusername/geo-political-analysis.git
cd geo-political-analysis
```

Run the script:
``` bash
python main.py
```
The output will include:
Fetched news headlines.
Summarized geopolitical news.
Analyzed trends and shifts.

# Testing
The project includes unit tests to validate the functionality of each agent. To run the tests:
``` bash
python -m unittest discover
```
The tests cover:

- Web scraping functionality.
- Summarization task using the LLM.
- Trend analysis task using the LLM.

# Project Structure
The project is organized as follows:

```
geo-political-analysis/
├── main.py                  # Main script to execute the workflow
├── agents.py                # Definitions of the AI agents
├── tasks.py                 # Definitions of the tasks for each agent
├── ollama_client.py         # Wrapper for interacting with the Ollama API
├── tests/                   # Unit tests
│   ├── test_agents.py       # Tests for agent functionality
│   └── __init__.py          # Marks the directory as a Python package
├── README.md                # Project documentation
└── requirements.txt         # List of dependencies
```


## Explanation of Each File

1. **`main.py`**:
   - The entry point of the application.
   - Initializes the agents, tasks, and crew.
   - Executes the workflow and prints the results.

2. **`agents.py`**:
   - Defines the three agents:
     - `WebScraperAgent`: Fetches news headlines.
     - `GeoPoliticsExpertAgent`: Summarizes news.
     - `TrendsAndShiftsExpertAgent`: Analyzes trends.

3. **`tasks.py`**:
   - Defines the tasks for each agent:
     - `NewsFetchingTask`: Fetches news.
     - `NewsSummarizationTask`: Summarizes news.
     - `TrendAnalysisTask`: Analyzes trends.

4. **`ollama_client.py`**:
   - Wraps the `ollama` Python client for interacting with the locally deployed LLM.

5. **`tests/test_agents.py`**:
   - Contains unit tests for the agents:
     - Tests the web scraper.
     - Tests the summarization task.
     - Tests the trend analysis task.

6. **`requirements.txt`**:
   - Lists all required Python libraries:
     ```
     crewai
     requests
     beautifulsoup4
     ollama
     ```

7. **`README.md`**:
   - Provides an overview of the project, installation instructions, usage, and architecture.


### Next Steps

1. **Deploy Locally**: Follow the instructions in the `README.md` to set up and run the project.
2. **Customize**: Modify the prompts or add new agents/tasks to suit your needs.
3. **Contribute**: Share your improvements or extensions with the community!