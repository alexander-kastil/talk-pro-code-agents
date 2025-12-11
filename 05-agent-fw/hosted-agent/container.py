import asyncio
import os

from agent_framework.azure import AzureAIAgentClient
from agent_framework.observability import setup_observability
from azure.ai.agentserver.agentframework import from_agent_framework
from dotenv import load_dotenv
from workflow_core import create_agent, get_credential

load_dotenv(override=True)


async def main() -> None:
    """
    The writer and reviewer multi-agent workflow.
    This module serves as the entry point for the containerized workflow application.

    Environment variables required:
    - AZURE_AI_PROJECT_ENDPOINT: Your Microsoft Foundry project endpoint
    - AZURE_AI_MODEL_DEPLOYMENT_NAME: Your Microsoft Foundry model deployment name
    """

    # Initialize observability only when explicitly enabled.
    # Set ENABLE_TRACING=true to export to a local collector (default VS Code port 4319).
    if os.getenv("ENABLE_TRACING", "").strip().lower() in ("1", "true", "yes", "on"):
        port = int(os.getenv("OTEL_COLLECTOR_PORT", "4319"))
        setup_observability(vs_code_extension_port=port, enable_sensitive_data=False)

    async with get_credential() as credential:
        async with AzureAIAgentClient(async_credential=credential) as chat_client:
            agent = await create_agent(chat_client)
            await from_agent_framework(agent).run_async()


if __name__ == "__main__":
    asyncio.run(main())
