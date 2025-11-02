# Project: Researcher Agent

## Objective

This project is a multi-agent system designed for automated research and content creation. It utilizes a supervisor agent to orchestrate the collaboration between a specialized researcher agent and a copywriter agent. The primary goal is to take a user's request, conduct thorough research from multiple angles, and then generate high-quality, engaging content in various formats, including posting directly to social media platforms.

## Project Log

### LinkedIn API Integration

- **Objective**: Enabled the agent to post content directly to a user's LinkedIn profile.
- **Authentication Script (`linkdin_call.py`)**: 
    - Created a script to handle the complex LinkedIn OAuth 2.0 authentication flow.
    - Iteratively debugged multiple authentication errors (`redirect_uri_mismatch`, `invalid_client`, `invalid_request`, scope permission errors).
    - Greatly improved the script by embedding a temporary web server to automatically catch the authorization code from the redirect, providing a much smoother user experience.
- **Posting Script (`post_to_linkedin.py`)**:
    - Created a standalone script to test posting functionality.
    - Debugged a `403 ACCESS_DENIED` error by updating the script to use the modern `/v2/userinfo` endpoint, ensuring compatibility with the OpenID Connect scopes.
- **Agent Integration**:
    - Added a new `post_to_linkedin` tool to the `copywriter.py` agent.
    - Updated the copywriter's prompt to make it aware of its new capability to publish content directly to LinkedIn.
- **Security**:
    - Handled `Client Secret` securely by refusing to save it to files and advising on regeneration after it was exposed.
    - Used temporary hardcoding for debugging purposes only, with clear warnings about the security risks.

## How it Works

The workflow is managed by a supervisor agent that directs the sub-agents:

1.  **Supervisor Agent**: This is the main point of contact for the user. It analyzes the user's request, breaks it down into a series of atomic research tasks, and creates a plan.

2.  **Researcher Agent**: The supervisor assigns specific research tasks to this agent. The researcher uses the Tavily API to search the web, extract relevant information from web pages, and compile the findings into structured research reports.

3.  **Copywriter Agent**: Once all research tasks are completed, the supervisor hands off the collected research reports to the copywriter. This agent then synthesizes the information to create well-written content and can post it directly to social media platforms using its available tools.

## Current Status & Accomplishments

- **LinkedIn Integration**: The agent can now fully authorize with the LinkedIn API and post content to a user's profile.
- **Core Agentic Framework**: The multi-agent architecture using LangChain and LangGraph is fully implemented.
- **Defined Roles**: The supervisor, researcher, and copywriter agents are clearly defined with distinct prompts, tools, and responsibilities.
- **Graph-Based Workflow**: The agents are connected in a stateful graph, enabling seamless task handoffs and a persistent state.
- **Interactive CLI**: A command-line interface (`main.py`) allows users to interact with the system in real-time.

## Key Technologies

- **Core Language**: Python
- **Agent Framework**: LangChain, LangGraph
- **LLMs**: Google's Gemini models (via `langchain-google-genai`), Groq models (via `langchain-groq`)
- **Research Tools**: Tavily API for web search and content extraction
- **CLI**: Rich for formatted and interactive terminal output
- **Configuration**: `dotenv` for environment variable management

## Future Objectives

- **Direct Social Media Posting**: Enable the agent to post content directly to X (formerly Twitter).
- **Secure Credential Management**: Remove hardcoded secrets and implement a more robust method for handling credentials.
- **Expand Content Formats**: Add capabilities to generate other types of content, such as presentations or email newsletters.
- **Enhance Research Tools**: Integrate more diverse data sources beyond web search, such as academic papers or specific APIs.
