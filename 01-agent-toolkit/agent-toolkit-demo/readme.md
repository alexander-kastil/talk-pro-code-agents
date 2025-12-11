# Travel Agent

Travel Agent is a declarative agent using the Microsoft Agent Toolkit to assist users in planning trips by providing recommendations on destinations, accommodations, and activities based on user preferences.

## Implementation

- Using the Microsoft Agent Toolkit to create a declarative agent.

- Explain important files and folders in the project structure:

  - manifest.json: Contains metadata about the agent, including its name, description, and capabilities.
  - declarativeAgent.json: Defines the behavior and configurations of the travel agent.
  - m365agents.yml: Provides deployment configurations for the agent.

- Point out instruction.txt file that contains the specific instructions given to the agent to guide its responses and actions.

- Add conversation starters to help users initiate interactions with the travel agent:

  ```
  "conversation_starters": [
    {
        "title": "Vienna Trip",
        "text": "Recommend places to visit in Vienna"
    },
    {
        "title": "Lunch Options",
        "text": "Recommend places for lunch near the Colosseum in Rome"
    },
    {
        "title": "Currency Exchange",
        "text": "I am coming from China. How much is 1000 CNY in EUR?"
    }
  ]
  ```

- Run and deploy it using the Microsoft 365 Agents Toolkit:

  - Use the `Provision` command to set up necessary resources.
  - Use the `Preview Your App (F5)` command to test the agent in Copilot.

- Next we will use the Microsoft 365 Agents Toolkit MCP to extend the Travel Agent by adding web content and API plugins to enhance its capabilities.
