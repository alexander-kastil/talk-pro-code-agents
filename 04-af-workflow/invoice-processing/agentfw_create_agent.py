import asyncio
import os
from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from azure.ai.projects.aio import AIProjectClient
from azure.ai.agents.aio import AgentsClient

# Load environment variables
load_dotenv()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
AGENT_NAME = os.getenv("AZURE_AI_AGENT_NAME", "Foundry Demo Agent")


async def main():
    """Interactive demo: Create an agent that shows up in Foundry and chat with it."""

    print("\n" + "=" * 70)
    print("DEMO: Create Azure AI Foundry Agent (Interactive)")
    print("=" * 70)

    if not PROJECT_ENDPOINT or not MODEL_DEPLOYMENT:
        raise RuntimeError("AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME must be set.")

    async with AzureCliCredential() as credential:
        async with AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential) as project_client:
            print("\nCreating new agent in Azure AI Foundry...")

            async with AgentsClient(endpoint=PROJECT_ENDPOINT, credential=credential) as agents_client:
                created_agent = await agents_client.create_agent(
                    model=MODEL_DEPLOYMENT,
                    name=AGENT_NAME,
                    instructions=(
                        "You are a helpful AI assistant. Be concise and friendly. "
                        "This agent is created from the Agent Framework demo so it shows up in Microsoft Foundry."
                    ),
                    description="Agent Framework interactive sample created via script."
                )

            print("Agent created successfully!")
            print(f"   Agent ID: {created_agent.id}")

            async with ChatAgent(
                chat_client=AzureAIAgentClient(
                    project_client=project_client,
                    agent_id=created_agent.id,
                    async_credential=credential
                )
            ) as agent:

                print("\n" + "=" * 70)
                print("Interactive Chat (Type 'quit' to exit)")
                print("=" * 70 + "\n")

                while True:
                    try:
                        user_input = input("You: ")
                    except EOFError:
                        print("\nReceived EOF - exiting.")
                        break
                    except KeyboardInterrupt:
                        print("\nInterrupted - exiting.")
                        break

                    if user_input.lower() in ["quit", "exit", "q"]:
                        print("\nGoodbye!")
                        break

                    if not user_input.strip():
                        continue

                    print("Agent: ", end="", flush=True)
                    async for chunk in agent.run_stream(user_input):
                        if chunk.text:
                            print(chunk.text, end="", flush=True)
                    print("\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSee you again soon.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
