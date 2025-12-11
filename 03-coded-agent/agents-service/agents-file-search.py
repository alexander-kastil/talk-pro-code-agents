import os
import time

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, PromptAgentDefinition


def main() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

    load_dotenv()
    endpoint = os.getenv("PROJECT_ENDPOINT")
    model = os.getenv("MODEL_DEPLOYMENT")
    vector_store_id = os.getenv("VECTOR_STORE_ID")

    print(f"Using endpoint: {endpoint}")
    print(f"Using model: {model}")
    print(f"Using vector store: {vector_store_id}")

    credential = DefaultAzureCredential()
    project_client = AIProjectClient(endpoint=endpoint, credential=credential)
    openai_client = project_client.get_openai_client()

    start = time.time()

    # Create a new agent version that shows up in the Microsoft Foundry portal by default.
    agent = project_client.agents.create_version(
        agent_name="file-search-agent",
        definition=PromptAgentDefinition(
            kind="prompt",
            model=model,
            instructions=(
                "You are a helpful agent knowledgeable about stock companies."
                "Use the file search tool to find relevant information."
            ),
            tools=[FileSearchTool(type="file_search", vector_store_ids=[vector_store_id])],
        ),
        description="File search agent migrated to the new Foundry agents experience.",
    )
    print(f"Created agent version: {agent.name}:{agent.version}")
    print("✓ Agent is visible in the Foundry portal under 'Agents'")
    print(f"  View at: {endpoint.replace('/api/projects/', '/projects/')}")

    # Conversations + responses replace the legacy threads/runs flow.
    conversation = openai_client.conversations.create(
        items=[{"type": "message", "role": "user", "content": "Tell me about Equinox Gold"}]
    )
    print(f"Created conversation: {conversation.id}")

    response = openai_client.responses.create(
        conversation=conversation.id,
        input="Tell me about Equinox Gold",
        extra_body={
            "agent": {
                "type": "agent_reference",
                "name": agent.name,
                "version": agent.version,
            }
        },
    )
    print(f"Response status: {getattr(response, 'status', 'completed')}")

    duration = time.time() - start
    print(f"Run took {duration:.2f}s")

    if getattr(response, "error", None):
        print(f"Run error: {response.error}")

    print("\n--- Conversation ---")
    for item in response.output or []:
        if getattr(item, "type", "") != "message":
            continue
        for content in item.content:
            text = getattr(content, "text", None)
            if text:
                print(f"assistant: {text}")
            elif hasattr(content, "input_text"):
                print(f"assistant: {content.input_text}")


if __name__ == "__main__":
    main()
