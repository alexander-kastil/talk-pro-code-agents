import os
import time
from dotenv import load_dotenv
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    ListSortOrder,
    McpTool,
    RequiredMcpToolCall,
    SubmitToolApprovalAction,
    ToolApproval,
)


def main():
    # Load environment variables from .env file
    load_dotenv()
    endpoint = os.environ["PROJECT_ENDPOINT"]
    model = os.environ["MODEL_DEPLOYMENT"]

    # Get MCP server configuration from environment variables
    mcp_server_url = os.environ["MCP_SERVER_URL"]
    mcp_server_label = os.environ["MCP_SERVER_LABEL"]
    mcp_tool_name = os.environ["MCP_TOOL_NAME"]


    question = "Will agents from Azure AI Foundry show up in Microsoft Foundry by default"
    print(f"USER: {question}", flush=True)

    agents_client = AgentsClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    # [START create_agent_with_mcp_tool]
    # Initialize agent MCP tool
    mcp_tool = McpTool(
        server_label=mcp_server_label,
        server_url=mcp_server_url,
        allowed_tools=[],
    )

    # Allow the Microsoft Learn tool defined in configuration.
    mcp_tool.allow_tool(mcp_tool_name)

    # Create agent with MCP tool and process agent run
    with agents_client:
        # Create a new agent.
        # NOTE: To reuse existing agent, fetch it with get_agent(agent_id)
        agent = agents_client.create_agent(
            model=model,
            name="mcp-agent",
            instructions="You are a helpful agent that must consult the configured Microsoft Learn MCP tools before answering. Provide concise guidance based on official documentation.",
            description="Demonstrates Microsoft Learn MCP integration with approval workflows.",
            tools=mcp_tool.definitions,
        )
        # [END create_agent_with_mcp_tool]

        thread = agents_client.threads.create()

        message = agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content=question,
        )

        # [START handle_tool_approvals]
        # Create and process agent run in thread with MCP tools
        run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id, tool_resources=mcp_tool.resources)

        last_status = None
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
            if run.status != last_status:
                print(f"Run status: {run.status}")
                last_status = run.status

            if run.status == "requires_action" and isinstance(run.required_action, SubmitToolApprovalAction):
                tool_calls = run.required_action.submit_tool_approval.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    agents_client.runs.cancel(thread_id=thread.id, run_id=run.id)
                    break

                tool_approvals = []
                for tool_call in tool_calls:
                    if isinstance(tool_call, RequiredMcpToolCall):
                        tool_approvals.append(
                            ToolApproval(
                                tool_call_id=tool_call.id,
                                approve=True,
                                headers=mcp_tool.headers,
                            )
                        )
                if tool_approvals:
                    agents_client.runs.submit_tool_outputs(
                        thread_id=thread.id, run_id=run.id, tool_approvals=tool_approvals
                    )

            # [END handle_tool_approvals]

        print(f"Run finished with status: {run.status}")

        if run.status == "failed":
            # Check if you got "Rate limit is exceeded.", then you want to get more quota
            print(f"Run failed: {run.last_error}")

        # Fetch and log messages in chronological order
        messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        print("Conversation:")
        for msg in messages:
            if msg.text_messages:
                last_text = msg.text_messages[-1]
                print(f"{msg.role.upper()}: {last_text.text.value}")

        # Clean-up and delete the agent once the run is finished.
        # Controlled by DELETE_AGENT_ON_EXIT environment variable
        delete_on_exit = os.environ["DELETE_AGENT_ON_EXIT"].lower() == "true"
        if delete_on_exit:
            agents_client.delete_agent(agent.id)
            print("Deleted agent")
        else:
            print(f"Agent {agent.id} preserved for examination in Azure AI Foundry")


if __name__ == '__main__':
    main()
