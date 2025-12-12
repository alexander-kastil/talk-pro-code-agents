# Microsoft Foundry SDKs

Microsoft Foundry SDKs provide libraries and tools to build, deploy, and manage AI-powered agents using Microsoft Foundry services.

These SDKs support multiple programming languages and offer seamless integration with Microsoft Foundry capabilities.

Available in Python and .NET

## Python SDK Sample

Azure Identity 1.26.0b1 provides DefaultAzureCredential so the agent can authenticate with Managed Identity or local credentials without hard-coding secrets.

Azure AI Projects 2.0.0b2 supplies the Foundry client APIs that create agent versions and run conversations against your configured model deployment. Together they let the sample register a Foundry agent bound to your project endpoint and vector store, instead of wiring HTTP calls manually.

PromptAgentDefinition defines the instructions, model, and tools for a prompt-based agent version, meaning Foundry can serve and invoke it without extra orchestration code. Foundry also supports OpenAI Assistants-style agents and workflow agents, giving you options for tool-augmented prompts, multi-step process orchestration, or custom plug-in flows.

Other Foundry agent types include workflow agents (YAML/code orchestrations across steps and tools) and hosted agents. A hosted agent is your containerized agentic app (for example, a LangGraph or custom server) run on the Foundry Agent Service with managed scaling, conversations, auth, and observability—no custom hosting or protocol glue required.
