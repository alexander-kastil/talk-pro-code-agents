# Microsoft Foundry Workflows

Workflows are UI-based tools in Microsoft Foundry. You can use them to create declarative, predefined sequences of actions that include agents.

| Pattern           | Description                                                         | Typical use case                                                                                                            |
| ----------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Sequential        | Passes the result from one agent to the next in a defined order     | Step-by-step workflows, pipelines, or multiple-stage processing                                                             |
| Human in the loop | Asks the user a question and awaits user input to proceed           | Creating approval requests during workflow execution and waiting for human approval, or obtaining information from the user |
| Group chat        | Dynamically passes control between agents based on context or rules | Dynamic workflows, escalation, fallback, or expert handoff scenarios                                                        |
