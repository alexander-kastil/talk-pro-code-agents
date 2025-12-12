# Microsoft Agent Framework

Allows developers to build, orchestrate, and manage AI-powered agents across Microsoft platforms and services.

Workflows allow deterministic sequences of actions, integrating multiple agents and tools using executors and edges.

Microsoft Agent Framework is integrated into Microsoft Foundry using the Hosted Agent type, enabling scalable deployment and management of agentic applications.

| Workflow Type | Description                                                                                                        | Use Cases                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| Sequential    | Passes the result from one agent to the next in a defined order.                                                   | Step-by-step workflows, pipelines, multi-stage processing.            |
| Concurrent    | Broadcasts a task to all agents, collects results independently.                                                   | Parallel analysis, independent subtasks, ensemble decision making.    |
| Group Chat    | Coordinates multiple agents in a collaborative conversation with a manager controlling speaker selection and flow. | Iterative refinement, collaborative problem-solving, content review.  |
| Handoff       | Dynamically passes control between agents based on context or rules.                                               | Dynamic workflows, escalation, fallback, or expert handoff scenarios. |
| Magentic      | Inspired by MagenticOne.                                                                                           | Complex, generalist multi-agent collaboration.                        |
