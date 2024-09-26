import vertexai
from google.oauth2 import service_account
import autogen

# Load service account credentials for Vertex AI
credentials = service_account.Credentials.from_service_account_file(
    filename=r"service_account_file.json"  # Your service account file here 
)

# Initialize Vertex AI with your project details
vertexai.init(
    project="your_project_ID",  # Replace with your GCP project ID
    location="us-central1",     # Replace with your preferred region
    credentials=credentials
)

# Define the LLM configuration for Gemini models
llm_config = {
    "config_list": [
        {
            "model": "gemini_model",  # Use the appropriate model version
            "api_type": "google",
            "project_id": "your_project_ID",
            "location": "us-central1",
            "credentials": credentials,
        }
    ]
}

# Define the ResearcherAgent (generates test plan)
research_agent = autogen.AssistantAgent(
    name="ResearcherAgent",
    llm_config=llm_config,
    system_message="""\
        You are a researcher tasked with generating detailed test plans based on queries.
        Your test plans should be comprehensive and well-structured.
        """
)

# Define the ReviewerAgent (reviews the test plan)
reviewer_agent = autogen.AssistantAgent(
    name="ReviewerAgent",
    llm_config=llm_config,
    system_message="""\
        You are a reviewer tasked with reviewing test plans.
        Use the following guidelines to provide feedback:
        - Ensure all edge cases are covered.
        - Steps should be logically ordered and actionable.
        - Make sure the test plan covers all relevant scenarios.
        Provide feedback or mark as TERMINATE if satisfied.
        """
)

# Define the ReviserAgent (modifies the test plan based on feedback)
reviser_agent = autogen.AssistantAgent(
    name="ReviserAgent",
    llm_config=llm_config,
    system_message="""\
        You are a reviser tasked with modifying the test plan according to the reviewer's feedback.
        Ensure that any user feedback is also incorporated in the revision process.
        """
)

# Define the UserProxyAgent (proxy for user feedback)
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="ALWAYS",  # ask human for input at each step
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,  # Set to True if using Docker
    },
)

# Sample tasks
test_plan_query = "Generate a test plan for the user login functionality."
review_feedback = "The test plan is missing a check for incorrect login credentials."
user_feedback = "Ensure that password recovery is also covered in the test plan."

# Initiate conversation between Researcher, Reviewer, Reviser, and incorporate User feedback
chat_results = autogen.initiate_chats(
    [
        # Step 1: Researcher generates the test plan
        {
            "sender": user_proxy,
            "recipient": research_agent,
            "message": test_plan_query,
            "clear_history": True,
            "silent": False,
            "summary_method": "last_msg",
        },
        # Step 2: Reviewer reviews the test plan based on guidelines
        {
            "sender": reviewer_agent,
            "recipient": research_agent,
            "message": "Review the generated test plan and provide feedback based on the guidelines.",
            "carryover": review_feedback,  # Reviewer gives feedback
            "max_turns": 3,  # Limit interactions to 3 turns between Reviewer and Researcher
        },
        # Step 3: Reviser modifies the test plan based on reviewer's feedback
        {
            "sender": user_proxy,
            "recipient": reviser_agent,
            "message": f"Revise the test plan based on the reviewer's feedback: {review_feedback} and incorporate the user's feedback: {user_feedback}.",
            "carryover": user_feedback,  # User feedback incorporated in revision
        },
        # Step 4: Reviewer reviews the revised test plan
        {
            "sender": reviser_agent,
            "recipient": reviewer_agent,
            "message": "Review the revised test plan and ensure all feedback has been addressed.",
            "max_turns": 3,  # Limit interactions to 3 turns between Reviewer and Reviser
            "summary_method": "reflection_with_llm",
        }
    ]
)

# Output the chat results for each agent interaction
for result in chat_results:
    recipient_name = result.recipient.name
    message = result.message
    print(f"{recipient_name}: {message}")
