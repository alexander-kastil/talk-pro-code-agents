import asyncio
import os
import logging

from agent_framework import AgentRunUpdateEvent
from agent_framework.azure import AzureAIAgentClient
from agent_framework.observability import setup_observability
from dotenv import load_dotenv
from workflow_core import create_agent, get_credential

load_dotenv(override=True)


async def main() -> None:
    # Initialize observability only when explicitly enabled.
    # Set ENABLE_TRACING=true to export to a local collector (default VS Code port 4319).
    if os.getenv("ENABLE_TRACING", "").strip().lower() in ("1", "true", "yes", "on"):
        port = int(os.getenv("OTEL_COLLECTOR_PORT", "4319"))
        setup_observability(vs_code_extension_port=port, enable_sensitive_data=False)

    # Suppress terminal-node runner warnings from agent framework in one-way flows.
    logging.getLogger("agent_framework._workflows._runner").setLevel(logging.ERROR)

    def _print_banner(title: str) -> None:
        line = "=" * 80
        print(f"\n{line}\n{title}\n{line}")

    async with get_credential() as credential:
        async with AzureAIAgentClient(async_credential=credential) as chat_client:
            # Use workflow form for rich streaming; warnings are suppressed via logging.
            agent = await create_agent(chat_client, as_agent=False)

            # Run the agent and stream events with clear executor banners
            last_executor_id: str | None = None
            async for event in agent.run_stream(
                "Create a story about the love between a Sighthound and his owner."
            ):
                if isinstance(event, AgentRunUpdateEvent):
                    eid = event.executor_id
                    if eid != last_executor_id:
                        _print_banner(f"Executor: {eid}")
                        last_executor_id = eid
                    # Stream the token/data chunk
                    print(event.data, end="", flush=True)
            # Ensure a final newline after streaming completes
            print()


if __name__ == "__main__":
    asyncio.run(main())
