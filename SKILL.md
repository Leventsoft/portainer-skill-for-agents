---
name: portainer
description: Comprehensive management for Portainer CE environments and stacks. Supports interaction with users via agents like Hermes and OpenClaw to handle Docker Compose, Swarm, and Kubernetes stacks, as well as advanced raw Docker proxy commands. This skill simplifies infrastructure management for agents.
---

# Portainer Manager Skill

Extend your agent's capabilities by managing Docker infrastructure through the Portainer CE HTTP API. This skill is compatible with Hermes, OpenClaw, and other modular agents.

## Setup

Add your Portainer API Key to the environment variable configuration:

```bash
export PORTAINER_API_TOKEN="your_token_here"  # Required: API key from Portainer
export PORTAINER_API_URL="https://your-portainer-instance.example.com/api" # Optional; defaults to https://localhost:9443/api
```

## Key Functions

### Environment/Endpoint Management
- **`list_environments()`**: Retrieve all connected Portainer environments (endpoints).
- **`inspect_environment(endpoint_id)`**: Get full details for a specific environment.
- **`get_environment_snapshot(endpoint_id)`**: Retrieve an environment's state snapshot.

### Stack Management (Docker Compose/Swarm/Kubernetes)
- **`list_stacks(environment_id)`**: List all stacks across environments or filter by environment.
- **`inspect_stack(stack_id)`**: Fetch full details (compose content, environment variables) of a stack.
- **`deploy_stack(name, compose_content, endpoint_id, method="string")`**: Deploy a new stack. Methods: `string`, `file`, `repository`.
- **`deploy_kubernetes_stack(...)`** and **`deploy_swarm_stack(...)`**: Specialized stack deployment.
- **`update_stack(stack_id, ...)`**: Update an existing stack's configuration/compose file.
- **`start_stack(stack_id)`** & **`stop_stack(stack_id)`**: Manage running/stopped status.
- **`remove_stack(stack_id)`**: Delete a stack safely.

### Advanced Features
- **`execute_docker_command(...)`**: Proxy raw Docker API commands seamlessly through Portainer.
- **`list_templates()`**, **`create_backup()`**, and **Kubernetes integration:** Extend beyond stacks into Portainer's system functionalities.
