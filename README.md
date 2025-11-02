# Researcher Agent

This project implements a multi-agent system for automated research and content creation. A supervisor agent orchestrates a researcher and a copywriter agent to fulfill user requests, from initial research to final content publication on platforms like LinkedIn.

## How it Works

The system uses a hierarchical agent structure:

1.  **Supervisor Agent**: The user interacts with the supervisor. It interprets the user's request, creates a research plan, and delegates tasks to the specialized sub-agents.

2.  **Researcher Agent**: This agent receives research tasks from the supervisor. It uses the Tavily API to browse the web, gather information, and compile detailed research reports.

3.  **Copywriter Agent**: Once the research is complete, the supervisor passes the reports to the copywriter. This agent synthesizes the information into well-written content and can post it directly to social media using its available tools.

## Features

-   **Multi-Agent Architecture**: Built with LangChain and LangGraph for robust and stateful agent collaboration.
-   **Automated Web Research**: Leverages the Tavily API for comprehensive web searches and content extraction.
-   **Content Generation**: Creates various content formats, including blog posts and social media updates.
-   **Direct Social Media Posting**: Capable of authorizing with the LinkedIn API and posting content directly to a user's profile.
-   **Interactive CLI**: A user-friendly command-line interface allows for real-time interaction with the agent system.
-   **Extensible Agent Roles**: Clearly defined prompts and tools for each agent make it easy to extend their capabilities.

## Getting Started

### Prerequisites

-   Python 3.9+
-   Google Cloud SDK (for authentication)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd researcher-agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Create a `.env` file** in the root of the project directory.

2.  **Add the following environment variables** to the `.env` file:

    ```env
    # Google API Key for Gemini
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"

    # Tavily API Key for web research
    TAVILY_API_KEY="YOUR_TAVILY_API_KEY"

    # Groq API Key (optional, if you use Groq models)
    GROQ_API_KEY="YOUR_GROQ_API_KEY"

    # LinkedIn API Credentials for posting
    LINKEDIN_CLIENT_ID="YOUR_LINKEDIN_CLIENT_ID"
    LINKEDIN_CLIENT_SECRET="YOUR_LINKEDIN_CLIENT_SECRET"

    # LangSmith API Key for tracing (optional)
    LANGSMITH_API_KEY="YOUR_LANGSMITH_API_KEY"
    ```

3.  **Authenticate with LinkedIn:**
    Run the `linkdin_call.py` script once to authorize the application and generate a `linkedin_token.txt` file.
    ```bash
    python linkdin_call.py
    ```

## Usage

To start the interactive CLI, run:

```bash
python main.py
```

You can then enter your research and content creation requests at the prompt.

**Example:**

```
User: write a linkedin post on the top AI tools that small businesses and entrepreneurs need to be using to scale their businesses. include real-world examples and case studies where businesses are using these tools to scale their business with real numbers. include a call to action at the end for readers to follow me for more actionable playbooks on how to generate real value for their business.
```

## Project Structure

```
/
├─── .gitignore
├─── copywriter.py         # Defines the copywriter agent and its tools
├─── gemini.md             # Project context and log
├─── linkdin_call.py       # Handles LinkedIn OAuth authentication
├─── main.py               # Main entry point for the interactive CLI
├─── post_to_linkedin.py   # Script for posting content to LinkedIn
├─── researcher.py         # Defines the researcher agent and its tools
├─── supervisor.py         # Defines the supervisor agent and the main graph
├─── requirements.txt      # Python dependencies
├─── prompts/              # Contains the system prompts for each agent
└─── example_content/      # Contains example content for different platforms
```
