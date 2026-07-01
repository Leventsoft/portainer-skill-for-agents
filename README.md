# Portainer Skill for Agents (Hermes-Compatible)

This skill empowers agents like Hermes and OpenClaw to manage Docker infrastructure through a Portainer CE instance. Unlock advanced capabilities to inspect and manage stacks, execute raw Docker commands, and integrate with Kubernetes and Swarm environments directly via the Portainer API.

---

## 📢 Key Features

- **Environment Management**:
  - ✅ List all environments (endpoints) connected to Portainer.
  - 🔍 Inspect specific environments (e.g., resource usage, Docker engine details).
  - 📸 Retrieve snapshots of Docker environment states.

- **Stack Operations** (Docker Compose/Swarm/Kubernetes):
  - 🗂️ Deploy new stacks directly from Docker Compose content files.
  - 🛠️ Update existing stacks with new configurations (compose files).
  - ⏯️ Start or stop running stacks.
  - 🔥 Safely remove stacks while preserving your environment.
  - 🔍 Inspect detailed configurations, including **docker-compose.yml** and environment variables.

- **Advanced Docker Command Execution**:
  - 🛠️ Execute raw Docker API commands (e.g., `containers/json`, `networks` queries).
  - 🔗 Proxy commands seamlessly via the Portainer API for secure execution.

- **Portainer System Utilities**:
  - 🧰 List all custom templates available in Portainer.
  - 🚨 Backup or restore your Portainer instance.
  - 🔧 Access raw endpoints via `raw_request()` for extended flexibility (system-wide control).

🔥 **Advanced Kubernetes Support!** Deploy Kubernetes stacks by leveraging Portainer's unique capabilities.

---

## 📋 Requirements

- **Python 3.8+** installed in the agent’s runtime.
- Libraries: `requests`, `urllib3` (installable via `pip`).
- An active Portainer CE instance (token required for authentication).

---

## ⚙️ Setup

1. Export the necessary environment variables:
   ```bash
   export PORTAINER_API_TOKEN="your_token_here"
   export PORTAINER_API_URL="https://portainer.yourdomain.com/api"  # Optional (defaults to localhost)
   ```

2. Enable the skill in your agent configuration (Hermes example):
   ```bash
   hermes skills enable portainer
   ```

---

## 🛠️ Example Usage

Here’s how you can use this skill in interaction with your agent:

**Example 1: List all environments**
```
> "List all environments in my Portainer instance."
```
**Response:**
"Here are the connected environments:
1. `local` (Docker)
2. `production-cluster` (Kubernetes)
3. `staging-cluster` (Docker Swarm)"

---

**Example 2: Deploy a new stack**
```
> "Deploy an nginx stack named 'web-proxy' to the environment 1."
```
Agent request:
```bash
/opt/data/venv/bin/python3 /opt/data/skills/portainer/scripts/portainer_manager.py deploy_stack "web-proxy" "<Compose content>" --environment 1 --method string
```

---

**Example 3: Execute a raw Docker command via Portainer**
```
> "List all running containers in environment 2"
```
Agent executes:
```bash
/opt/data/skills/portainer/scripts/portainer_manager.py execute_docker_command 2 /containers/json GET
```
**Response from Portainer API:**
- `nginx`, ID: `abc1234`, Status: "Running"
- `mysql`, ID: `xyz5678`, Status: "Running"

---

**Example 4: Inspect a stack**
```
> "Show me the configuration of the stack named 'ai'."
```
Agent executes:
```bash
/opt/data/skills/portainer/scripts/portainer_manager.py inspect_stack <stack_id>
```
---

**Example 5: Deploy a Kubernetes stack**
```
> "Deploy a Kubernetes stack named 'data-pipeline' to Production."
```
Agent executes:
```bash
/opt/data/skills/portainer/scripts/portainer_manager.py deploy_kubernetes_stack 'data-pipeline' '<Manifest>' --environment 2
```

---

## 🛡️ Security Notes

- This skill requires an API token with appropriate privileges.
- Ensure your agent is operating in a secure environment to prevent unauthorized access to your infrastructure resources.

---

## 🚀 Compatibility

Works seamlessly with modular chatbot/agent architectures like **Hermes**, **OpenClaw**, and custom integrations.

---

Add it to your stack and simplify Docker management within seconds! 📦