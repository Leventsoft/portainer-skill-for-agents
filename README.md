# Portainer Skill for Agents (Hermes-Compatible)

This skill allows agents like Hermes and OpenClaw to integrate with a Portainer CE instance, streamlining Docker infrastructure management. Capabilities include deploying stacks, managing environments, querying Docker details through APIs, and much more.

## Key Features

- **Environment Management**:
  - List/inspect environments.
  - Retrieve snapshots of a Docker setup.
- **Docker Compose + Swarm/Kubernetes Stacks**:
  - Deploy, update, start/stop, delete stacks.
  - Detailed stack inspection (docker-compose.yml, environment variables, etc.).
- **Advanced Docker Command Execution**:
  - Leverage the Docker Proxy to execute raw API commands through Portainer, enabling operations not natively provided in the GUI.
- **Portainer System Utilities**:
  - List Docker templates, manage backups, or even access `raw_request()` endpoints for full system control.

## Requirements

- Python 3 installed in the agent's runtime.
- Libraries: `requests` and `urllib3` (installable via `pip`).
- Portainer CE up and running (API token required).

## Setup

```bash
export PORTAINER_API_TOKEN="ptr_..."  # API Token from Portainer → Settings > User
```

You can now enable the skill via your agent configuration. For Hermes:
```bash
hermes skills enable portainer
```

## Example Usage

Examples of user commands:

> "List all my environments."

> "Deploy an nginx stack in environment 1 using this Docker Compose content..."
