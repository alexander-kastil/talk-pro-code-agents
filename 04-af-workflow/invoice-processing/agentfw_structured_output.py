import asyncio
import os
from pydantic import BaseModel
from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agents.aio import AgentsClient
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential

# Load environment variables
load_dotenv()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")


# Define structured output model
class PersonInfo(BaseModel):
    """Extract person information from text."""
    name: str | None = None
    age: int | None = None
    occupation: str | None = None
    city: str | None = None


async def main():
    """Interactive demo: Structured output extraction against Foundry agent service."""

    print("\n" + "=" * 70)
    print("DEMO: Structured Output with Pydantic (Foundry)")
    print("=" * 70)

    if not PROJECT_ENDPOINT or not MODEL_DEPLOYMENT:
        raise RuntimeError("AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME must be set.")

    async with AzureCliCredential() as credential:
        async with AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential) as project_client:
            async with AgentsClient(endpoint=PROJECT_ENDPOINT, credential=credential) as agents_client:
                agent_record = await agents_client.create_agent(
                    model=MODEL_DEPLOYMENT,
                    name="ExtractorBot",
                    instructions="Extract person information from the user's text."
                )

            print("\nAgent created in Microsoft Foundry with PersonInfo schema")
            print("Schema: name, age, occupation, city")

            async with ChatAgent(
                chat_client=AzureAIAgentClient(
                    project_client=project_client,
                    agent_id=agent_record.id,
                    async_credential=credential
                )
            ) as agent:

                print("\n" + "=" * 70)
                print("Interactive Chat (Type 'quit' to exit)")
                print("=" * 70)
                print("\nTIP: Describe a person and see structured extraction\n")

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

                    print("\nExtracting structured data...")
                    response = await agent.run(user_input, response_format=PersonInfo)

                    if response.value:
                        person = response.value
                        print("\nExtracted Information:")
                        print(f"   Name: {person.name}")
                        print(f"   Age: {person.age}")
                        print(f"   Occupation: {person.occupation}")
                        print(f"   City: {person.city}")
                    else:
                        print("Could not extract information")

                    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSee you again soon.")
