import os

from agent_framework import WorkflowBuilder
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential, ManagedIdentityCredential


def get_credential():
    """Will use Managed Identity when running in Azure, otherwise falls back to DefaultAzureCredential."""
    return (
        ManagedIdentityCredential()
        if os.getenv("MSI_ENDPOINT")
        else DefaultAzureCredential()
    )


async def create_agent(chat_client: AzureAIAgentClient, as_agent: bool = True):
    writer = chat_client.create_agent(
        name="Writer",
        instructions="You are an excellent content writer. Create an up to 10 sentence story about the love between a dog and his owner in German.",
    )

    translator = chat_client.create_agent(
        name="Translator",
        instructions=(
            "You are an excellent content translator. Translate the story from German to English."
        ),
    )

    # Build the workflow by adding agents directly as edges.
    workflow = (
        WorkflowBuilder().set_start_executor(writer).add_edge(writer, translator).build()
    )

    return workflow.as_agent() if as_agent else workflow
