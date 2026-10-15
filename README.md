# Agentic AI Blog Generator

A multi-agent blog generation system built using Python, LangGraph, and Groq. The workflow uses specialized AI agents to research a topic, write a blog post, and polish the final content, with human review checkpoints between stages.

## Features

- **Research Agent:** Generates structured research outlines based on a topic and target audience.
- **Writer Agent:** Creates a blog draft using the research notes.
- **Human-in-the-Loop Review:** Allows users to approve or request changes to the research and draft.
- **Editor Agent:** Refines the approved draft into a final blog post.
- **Stateful Workflow:** Uses LangGraph to manage shared state, workflow transitions, and interruptions for human feedback.

## Workflow

1. Enter a blog topic and target audience.
2. The Research Agent generates an outline.
3. Review and approve the research or request changes.
4. The Writer Agent generates the draft.
5. Review and approve the draft or provide feedback.
6. The Editor Agent produces the final blog post.

## Tech Stack

- Python
- LangGraph
- LangChain
- Groq LLM API
- Pydantic
- Jupyter Notebook
- python-dotenv

## Project Structure

```text
blog_generator/
├── agents.py
├── graph.py
├── state.py
├── blog_generator.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mohit-Badi24/agentic-ai-blog-generator.git
cd agentic-ai-blog-generator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project directory and add your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

Never commit or share your actual API key.

### 5. Run the project

Open `blog_generator.ipynb` in Jupyter Notebook or VS Code and run its cells in order.

## Learning Outcomes

- Designing multi-agent workflows
- Managing shared state with LangGraph
- Implementing human-in-the-loop interactions
- Routing workflow execution based on user feedback
- Integrating an LLM through LangChain and Groq

## Author

Mohit Badi

GitHub: [Mohit-Badi24](https://github.com/Mohit-Badi24)