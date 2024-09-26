# Autogen_agentic_workflow_with_Gemini

This repository demonstrates the use of agents to generate, review, and revise a test plan through the integration of Vertex AI using Google's Gemini models. 

# Introduction to autogen
AutoGen, enables next-gen LLM applications with a generic multi-agent conversation framework. It offers customizable and conversable agents that integrate LLMs, tools, 
and humans. By automating chat among multiple capable agents, AutoGen can collectively perform tasks autonomously or with human feedback, including tasks that require the use 
of tools via code.

### Key Features of AutoGen in This Use Case:
- **Multi-agent conversations**: AutoGen agents can communicate with each other to solve tasks. This allows for more complex and sophisticated applications than would be possible with a single LLM.
- **Customization**: AutoGen agents can be customized to meet the specific needs of an application. This includes the ability to choose the LLMs to use, the types of human input to allow, and the tools to employ.
- **Human participation**: AutoGen seamlessly allows human participation. This means that humans can provide input and feedback to the agents as needed.

### Key Agents:
- **AssistantAgent**: Acts as an AI assistant using LLMs (e.g., GPT-4). It writes Python code to solve tasks, provides corrections based on execution results, and can be configured with a custom system message or LLM configuration via llm_config.

- **UserProxyAgent**: Represents a human user, gathering human input or executing code automatically when code blocks are detected. It can also generate LLM-based replies if llm_config is enabled, and code execution can be disabled via code_execution_config.

Both agents support auto-reply for more autonomous communication while allowing human intervention. The agents' behavior can be extended by registering custom reply functions using the register_reply() method.

In the following example, we create an AssistantAgent ("assistant") and a UserProxyAgent ("user_proxy") to collaborate on solving tasks.

# Features for this repository
The process involves multiple agents (Researcher, Reviewer, and Reviser) collaborating to create a comprehensive test plan, incorporating feedback from both an automated reviewer and the user.
- **ResearcherAgent**: Generates a detailed test plan based on a user-provided query.
- **ReviewerAgent**: Reviews the generated test plan, ensuring it covers all scenarios and provides feedback.
- **ReviserAgent**: Modifies the test plan based on reviewer feedback and user inputs.
- **UserProxyAgent**: Acts as a user proxy to provide user feedback and incorporate it into the conversation.

# Pre-requisites
- A Google Cloud Platform (GCP) project.
- Service Account credentials for Vertex AI with the necessary permissions.
- Vertex AI and Gemini models setup.

### Install Dependencies
```
$ pip install google-cloud-aiplatform
$ pip install autogen
$ pip install google-auth
```

### Service account Integration
```
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    filename="path/to/your/service_account_file.json"
)
```
### Vertex AI Initialization
```
vertexai.init(
    project="your_project_ID",  # Replace with your GCP project ID
    location="us-central1",     # Replace with your preferred region
    credentials=credentials
)
```

### Gemini Model Setup
```
config_list = [
    {
        "model": "gemini-model",  # Replace with the correct Gemini model
        "api_type": "google",
        "project_id": "your_project_id",
        "location": "us-central1",
        "credentials": credentials,
        "safety_settings": safety_settings,
    }
]
```
  
