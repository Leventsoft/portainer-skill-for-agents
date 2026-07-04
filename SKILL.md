---
name: portainer
description: Comprehensive management for Portainer CE environments and stacks. Supports listing environments, managing Docker Compose/Swarm/Kubernetes stacks, executing raw Docker commands via proxy, and full Portainer API coverage. Requires PORTAINER_API_TOKEN and PORTAINER_API_URL env vars set.
---

# Portainer Manager Skill

Manage Docker infrastructure via the Portainer CE HTTP API.

## Setup (already done — just use `portainer` command)

The env vars and dependencies are already configured. You **do NOT** need to set them up.

```
# Already configured:
#   PORTAINER_API_URL  →  http://172.18.0.2:9000/api  (overridable via .env)
#   PORTAINER_API_TOKEN → stored in .env
#   /opt/data/venv/bin/python3 with requests + urllib3
```

## Usage

**Use the `portainer` command** (not the long Python path):

```bash
portainer <command> [positional args...]
```

> ⚠️ **ALL arguments are POSITIONAL — do NOT use `--flags`**
> 
> Correct:  `portainer execute_docker_command 3 /networks`
> Wrong:    `portainer execute_docker_command --env-id 3 --path /networks`

## Quick Reference — Copy-Paste Ready

### First: Find your environment ID

```bash
portainer list_environments
```
→ The JSON output contains environments. Each has an `"Id"` field. Usually **3** (the local Docker socket).

### Environment/Endpoint Management

```bash
# List all environments
portainer list_environments

# Inspect a specific environment (replace 3 with your env ID)
portainer inspect_environment 3

# Get environment snapshot
portainer get_environment_snapshot 3
```

### Docker Proxy (Raw Docker API) — Most Used

```bash
# List all Docker networks
portainer execute_docker_command 3 /networks

# List all containers (running + stopped)
portainer execute_docker_command 3 /containers/json

# List all images
portainer execute_docker_command 3 /images/json

# List all volumes
portainer execute_docker_command 3 /volumes

# Docker system info
portainer execute_docker_command 3 /info

# List containers with filters (GET only)
portainer execute_docker_command 3 /containers/json?all=true
```

> 💡 **Path auto-fix**: The script automatically adds `/` if you forget it. `networks` → `/networks`.
>
> 💡 **Env shortcut**: Set `export PORTAINER_ENV_ID=3` then use `env` instead of the number:
> ```bash
> PORTAINER_ENV_ID=3 portainer execute_docker_command env /networks
> ```

### Stack Management

```bash
# List all stacks
portainer list_stacks

# List stacks for a specific environment
portainer list_stacks 3

# Get stack by name
portainer get_stack_by_name "my-stack"

# Inspect a stack (replace 9 with actual stack ID)
portainer inspect_stack 9

# Get stack compose file
portainer get_stack_file 9

# Start / Stop / Remove a stack
portainer start_stack 9
portainer stop_stack 9
portainer remove_stack 9

# Deploy a new stack (inline compose content)
portainer deploy_stack "my-app" "version: '3'\nservices:\n  web:\n    image: nginx" 3 string

# Update an existing stack
portainer update_stack 9 "version: '3'\nservices:\n  web:\n    image: nginx:alpine" 3 false
```

### System & Status

```bash
portainer get_system_info
portainer get_system_version
portainer get_system_status
portainer get_portainer_status
```

### Registry & Templates

```bash
portainer list_registries
portainer inspect_registry 1
portainer list_templates
portainer list_custom_templates
```

### Advanced

```bash
# Generic Portainer API call
portainer raw_request /endpoints GET
portainer raw_request /endpoints/3/docker/networks GET
```

## Environment ID Shortcut (Best Practice)

**Set this once so you never need to remember the numeric ID:**

```bash
# In your terminal session:
export PORTAINER_ENV_ID=3

# Then use 'env' as the env_id arg everywhere:
portainer execute_docker_command env /containers/json
portainer inspect_environment env
portainer list_stacks env
```

## Common Docker API Paths for `execute_docker_command`

| What | Path | Notes |
|------|------|-------|
| All networks | `/networks` | |
| All containers | `/containers/json` | Add `?all=true` for stopped too |
| All images | `/images/json` | |
| All volumes | `/volumes` | |
| Docker info | `/info` | |
| Container detail | `/containers/<id>/json` | Replace `<id>` with container hash |
| Container logs | `/containers/<id>/logs?stdout=true&stderr=true` | |
| Container stats | `/containers/<id>/stats?stream=false` | |

## Troubleshooting

**"Max retries exceeded" / "Failed to resolve" / Connection error:**
→ The `PORTAINER_API_URL` env var is wrong. Update it in `/opt/data/.env`.

**"I used `--flags` and it failed":**
→ This script uses POSITIONAL args only. See the flag-guard error message for the correct syntax.

**"What's the environment ID?":**
→ Run `portainer list_environments`, find the environment with `"Type": 1` (Docker standalone) and use its `"Id"`.

## What NOT to do ❌

```python
# DON'T try to import this as a Python module — it won't work:
from skills.portainer.scripts.portainer_manager import list_environments  # FAILS

# DON'T use --flags:
portainer execute_docker_command --env-id 3 --path /networks  # FAILS

# DON'T forget the leading / on Docker paths:
portainer execute_docker_command 3 networks  # Works! (auto-fixed)
```

## What TO do ✅

```bash
# ALWAYS use the portainer command with positional args:
portainer execute_docker_command 3 /networks
portainer list_environments
portainer list_stacks 3
```