# Portainer Manager Skill Backend

import requests
import os
import json
import sys
import traceback
import urllib3
from typing import Optional, Dict, Any, List

# Attempt to get Portainer API URL from environment, default to https://localhost:9443/api
PORTAINER_API_URL = os.environ.get("PORTAINER_API_URL", "https://localhost:9443/api")

# Suppress warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_portainer_api_token():
    token = os.environ.get("PORTAINER_API_TOKEN")
    if not token:
        raise ValueError("PORTAINER_API_TOKEN environment variable not set.")
    return token

def get_headers():
    token = get_portainer_api_token()
    return {"X-API-Key": token, "Content-Type": "application/json"}

def make_request(method: str, endpoint: str, payload: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
    """Generic HTTP request to Portainer API"""
    try:
        url = f"{PORTAINER_API_URL}{endpoint}"
        headers = get_headers()
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=30, verify=False)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=payload, timeout=30, verify=False)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, json=payload, timeout=30, verify=False)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        
        try:
            return response.json()
        except:
            return {"status": "success", "text": response.text}
    except Exception as e:
        return {"error": str(e)}

# =============================================================================
# ENVIRONMENT/ENDPOINT MANAGEMENT
# =============================================================================

def list_environments():
    """Retrieves all Portainer environments (endpoints)."""
    print(f"Attempting to list Portainer environments via {PORTAINER_API_URL}...", flush=True)
    return make_request("GET", "/endpoints")

def inspect_environment(endpoint_id: int):
    """Returns full details for a specific environment."""
    print(f"Inspecting environment ID: {endpoint_id}...", flush=True)
    return make_request("GET", f"/endpoints/{endpoint_id}")

def get_environment_snapshot(endpoint_id: int):
    """Gets a snapshot of an environment's state."""
    print(f"Getting snapshot for environment ID: {endpoint_id}...", flush=True)
    return make_request("GET", f"/endpoints/{endpoint_id}/snapshot")

# =============================================================================
# STACK MANAGEMENT
# =============================================================================

def list_stacks(environment_id: Optional[int] = None):
    """Lists all stacks. Optional: filter by environment ID."""
    print(f"Executing list_stacks{' for environment ID: ' + str(environment_id) if environment_id else ''}...", flush=True)
    result = make_request("GET", "/stacks")
    if isinstance(result, list) and environment_id:
        env_id_int = int(environment_id)
        result = [s for s in result if s.get("EndpointId") == env_id_int]
    return result

def get_stack_by_name(name: str):
    """Retrieves a stack by its name."""
    print(f"Getting stack by name: {name}...", flush=True)
    return make_request("GET", f"/stacks/name/{name}")

def inspect_stack(stack_id: int):
    """Returns full JSON details for a specific stack."""
    print(f"Inspecting stack ID: {stack_id}...", flush=True)
    result = make_request("GET", f"/stacks/{stack_id}")
    
    # Also fetch the stack file content if possible
    if isinstance(result, dict) and "error" not in result:
        try:
            file_result = make_request("GET", f"/stacks/{stack_id}/file")
            if isinstance(file_result, dict) and "StackFileContent" in file_result:
                result["StackFileContent"] = file_result["StackFileContent"]
        except:
            pass
    
    return result

def get_stack_file(stack_id: int):
    """Returns the docker-compose.yml content for a stack."""
    print(f"Getting stack file for stack ID: {stack_id}...", flush=True)
    return make_request("GET", f"/stacks/{stack_id}/file")

def deploy_stack(name: str, compose_content: str, endpoint_id: int, method: str = "string"):
    """
    Launches a new stack. 
    Methods: "string" (default), "file", "repository"
    """
    print(f"Deploying stack '{name}' to environment ID {endpoint_id} via method '{method}'...", flush=True)
    
    if method == "string":
        url = f"/stacks/create/standalone/string?endpointId={endpoint_id}"
        payload = {"name": name, "stackFileContent": compose_content, "env": []}
    elif method == "file":
        url = f"/stacks/create/standalone/file?endpointId={endpoint_id}"
        payload = {"name": name, "stackFileContent": compose_content, "env": []}
    elif method == "repository":
        url = f"/stacks/create/standalone/repository?endpointId={endpoint_id}"
        payload = {"name": name, "repositoryURL": compose_content, "env": []}
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return make_request("POST", url, payload=payload)

def deploy_kubernetes_stack(name: str, content: str, endpoint_id: int, method: str = "string"):
    """Deploys a Kubernetes stack. Methods: "string", "repository", "url"."""
    print(f"Deploying Kubernetes stack '{name}' to environment ID {endpoint_id} via method '{method}'...", flush=True)
    
    if method == "string":
        url = f"/stacks/create/kubernetes/string?endpointId={endpoint_id}"
        payload = {"name": name, "stackFileContent": content}
    elif method == "repository":
        url = f"/stacks/create/kubernetes/repository?endpointId={endpoint_id}"
        payload = {"name": name, "repositoryURL": content}
    elif method == "url":
        url = f"/stacks/create/kubernetes/url?endpointId={endpoint_id}"
        payload = {"name": name, "stackFileURL": content}
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return make_request("POST", url, payload=payload)

def deploy_swarm_stack(name: str, content: str, endpoint_id: int, method: str = "string"):
    """Deploys a Swarm stack. Methods: "string", "repository", "file"."""
    print(f"Deploying Swarm stack '{name}' to environment ID {endpoint_id} via method '{method}'...", flush=True)
    
    if method == "string":
        url = f"/stacks/create/swarm/string?endpointId={endpoint_id}"
        payload = {"name": name, "stackFileContent": content}
    elif method == "repository":
        url = f"/stacks/create/swarm/repository?endpointId={endpoint_id}"
        payload = {"name": name, "repositoryURL": content}
    elif method == "file":
        url = f"/stacks/create/swarm/file?endpointId={endpoint_id}"
        payload = {"name": name, "stackFileContent": content}
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return make_request("POST", url, payload=payload)

def update_stack(stack_id: int, compose_content: str, endpoint_id: int, prune: bool = False):
    """Updates an existing stack."""
    print(f"Updating stack ID {stack_id}...", flush=True)
    url = f"/stacks/{stack_id}?endpointId={endpoint_id}"
    payload = {
        "stackFileContent": compose_content,
        "env": [],
        "prune": prune
    }
    return make_request("PUT", url, payload=payload)

def start_stack(stack_id: int):
    """Starts a stopped stack."""
    print(f"Starting stack ID: {stack_id}...", flush=True)
    return make_request("POST", f"/stacks/{stack_id}/start")

def stop_stack(stack_id: int):
    """Stops a running stack."""
    print(f"Stopping stack ID: {stack_id}...", flush=True)
    return make_request("POST", f"/stacks/{stack_id}/stop")

def remove_stack(stack_id: int):
    """Deletes a stack by ID."""
    print(f"Removing stack ID: {stack_id}...", flush=True)
    return make_request("DELETE", f"/stacks/{stack_id}")

def redeploy_git_stack(stack_id: int):
    """Redeploys a stack from its Git repository."""
    print(f"Redeploying git stack ID: {stack_id}...", flush=True)
    return make_request("POST", f"/stacks/{stack_id}/git/redeploy")

# =============================================================================
# DOCKER PROXY (Raw Docker API)
# =============================================================================

def execute_docker_command(environment_id: int, path: str, method: str = "GET", payload: Optional[Dict] = None):
    """
    Proxies raw Docker API requests through Portainer.
    Example paths: /containers/json, /images/json, /networks, /volumes, /info
    """
    print(f"Executing Docker command on env {environment_id}: {method} {path}...", flush=True)
    # Portainer proxies Docker API at /endpoints/{id}/docker/{path}
    endpoint = f"/endpoints/{environment_id}/docker{path}"
    return make_request(method, endpoint, payload=payload)

# =============================================================================
# SYSTEM & STATUS
# =============================================================================

def get_system_info():
    """Returns Portainer system information."""
    print("Getting Portainer system info...", flush=True)
    return make_request("GET", "/system/info")

def get_system_version():
    """Returns Portainer version."""
    print("Getting Portainer version...", flush=True)
    return make_request("GET", "/system/version")

def get_system_status():
    """Returns Portainer status."""
    print("Getting Portainer system status...", flush=True)
    return make_request("GET", "/system/status")

def get_portainer_status():
    """Returns Portainer instance status."""
    print("Getting Portainer status...", flush=True)
    return make_request("GET", "/status")

# =============================================================================
# REGISTRY MANAGEMENT
# =============================================================================

def list_registries():
    """Lists all configured Docker registries."""
    print("Listing registries...", flush=True)
    return make_request("GET", "/registries")

def inspect_registry(registry_id: int):
    """Returns details for a specific registry."""
    print(f"Inspecting registry ID: {registry_id}...", flush=True)
    return make_request("GET", f"/registries/{registry_id}")

# =============================================================================
# TEMPLATE MANAGEMENT
# =============================================================================

def list_templates():
    """Lists all App Templates."""
    print("Listing App Templates...", flush=True)
    return make_request("GET", "/templates")

def list_custom_templates():
    """Lists all Custom Templates."""
    print("Listing Custom Templates...", flush=True)
    return make_request("GET", "/custom_templates")

# =============================================================================
# BACKUP & RESTORE
# =============================================================================

def create_backup():
    """Creates a Portainer backup."""
    print("Creating Portainer backup...", flush=True)
    return make_request("POST", "/backup")

def restore_backup(backup_file_path: str):
    """Restores from a backup file."""
    print(f"Restoring from backup: {backup_file_path}...", flush=True)
    # This requires multipart/form-data upload
    try:
        token = get_portainer_api_token()
        headers = {"X-API-Key": token}
        url = f"{PORTAINER_API_URL}/restore"
        with open(backup_file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, headers=headers, files=files, timeout=60, verify=False)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# =============================================================================
# ADVANCED: Generic Raw Request
# =============================================================================

def raw_request(endpoint: str, method: str = "GET", payload: Optional[Dict] = None):
    """Generic raw API request for endpoints not yet wrapped."""
    print(f"Raw request: {method} {endpoint}...", flush=True)
    return make_request(method, endpoint, payload=payload)

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python portainer_manager.py <command> [args...]", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  list_environments", file=sys.stderr)
        print("  inspect_environment <endpoint_id>", file=sys.stderr)
        print("  get_environment_snapshot <endpoint_id>", file=sys.stderr)
        print("  list_stacks [environment_id]", file=sys.stderr)
        print("  get_stack_by_name <name>", file=sys.stderr)
        print("  inspect_stack <stack_id>", file=sys.stderr)
        print("  get_stack_file <stack_id>", file=sys.stderr)
        print("  deploy_stack <name> <compose_content> <endpoint_id> [method]", file=sys.stderr)
        print("  deploy_kubernetes_stack <name> <content> <endpoint_id> [method]", file=sys.stderr)
        print("  deploy_swarm_stack <name> <content> <endpoint_id> [method]", file=sys.stderr)
        print("  update_stack <stack_id> <compose_content> <endpoint_id> [prune]", file=sys.stderr)
        print("  start_stack <stack_id>", file=sys.stderr)
        print("  stop_stack <stack_id>", file=sys.stderr)
        print("  remove_stack <stack_id>", file=sys.stderr)
        print("  redeploy_git_stack <stack_id>", file=sys.stderr)
        print("  execute_docker_command <env_id> <path> [method] [json_payload]", file=sys.stderr)
        print("  get_system_info", file=sys.stderr)
        print("  get_system_version", file=sys.stderr)
        print("  get_system_status", file=sys.stderr)
        print("  get_portainer_status", file=sys.stderr)
        print("  list_registries", file=sys.stderr)
        print("  inspect_registry <registry_id>", file=sys.stderr)
        print("  list_templates", file=sys.stderr)
        print("  list_custom_templates", file=sys.stderr)
        print("  create_backup", file=sys.stderr)
        print("  restore_backup <backup_file_path>", file=sys.stderr)
        print("  raw_request <endpoint> [method] [json_payload]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    try:
        if cmd == "list_environments":
            result = list_environments()
        elif cmd == "inspect_environment":
            result = inspect_environment(int(sys.argv[2]))
        elif cmd == "get_environment_snapshot":
            result = get_environment_snapshot(int(sys.argv[2]))
        elif cmd == "list_stacks":
            env_id = int(sys.argv[2]) if len(sys.argv) > 2 else None
            result = list_stacks(env_id)
        elif cmd == "get_stack_by_name":
            result = get_stack_by_name(sys.argv[2])
        elif cmd == "inspect_stack":
            result = inspect_stack(int(sys.argv[2]))
        elif cmd == "get_stack_file":
            result = get_stack_file(int(sys.argv[2]))
        elif cmd == "deploy_stack":
            method = sys.argv[5] if len(sys.argv) > 5 else "string"
            result = deploy_stack(sys.argv[2], sys.argv[3], int(sys.argv[4]), method)
        elif cmd == "deploy_kubernetes_stack":
            method = sys.argv[5] if len(sys.argv) > 5 else "string"
            result = deploy_kubernetes_stack(sys.argv[2], sys.argv[3], int(sys.argv[4]), method)
        elif cmd == "deploy_swarm_stack":
            method = sys.argv[5] if len(sys.argv) > 5 else "string"
            result = deploy_swarm_stack(sys.argv[2], sys.argv[3], int(sys.argv[4]), method)
        elif cmd == "update_stack":
            prune = sys.argv[5].lower() == "true" if len(sys.argv) > 5 else False
            result = update_stack(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), prune)
        elif cmd == "start_stack":
            result = start_stack(int(sys.argv[2]))
        elif cmd == "stop_stack":
            result = stop_stack(int(sys.argv[2]))
        elif cmd == "remove_stack":
            result = remove_stack(int(sys.argv[2]))
        elif cmd == "redeploy_git_stack":
            result = redeploy_git_stack(int(sys.argv[2]))
        elif cmd == "execute_docker_command":
            env_id = int(sys.argv[2])
            path = sys.argv[3]
            method = sys.argv[4] if len(sys.argv) > 4 else "GET"
            payload = json.loads(sys.argv[5]) if len(sys.argv) > 5 else None
            result = execute_docker_command(env_id, path, method, payload)
        elif cmd == "get_system_info":
            result = get_system_info()
        elif cmd == "get_system_version":
            result = get_system_version()
        elif cmd == "get_system_status":
            result = get_system_status()
        elif cmd == "get_portainer_status":
            result = get_portainer_status()
        elif cmd == "list_registries":
            result = list_registries()
        elif cmd == "inspect_registry":
            result = inspect_registry(int(sys.argv[2]))
        elif cmd == "list_templates":
            result = list_templates()
        elif cmd == "list_custom_templates":
            result = list_custom_templates()
        elif cmd == "create_backup":
            result = create_backup()
        elif cmd == "restore_backup":
            result = restore_backup(sys.argv[2])
        elif cmd == "raw_request":
            endpoint = sys.argv[2]
            method = sys.argv[3] if len(sys.argv) > 3 else "GET"
            payload = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None
            result = raw_request(endpoint, method, payload)
        else:
            result = {"error": f"Unknown command: {cmd}"}
        
        print(json.dumps(result, indent=2), flush=True)
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)