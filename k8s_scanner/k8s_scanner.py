from kubernetes import client, config
import os

def load_kube_config():
    """Load Kubernetes configuration from file or in-cluster."""
    kubeconfig_path = os.getenv('KUBECONFIG', '/root/.kube/config')
    try:
        config.load_kube_config(config_file=kubeconfig_path)
        print(f"Loaded kubeconfig from {kubeconfig_path}")
    except config.config_exception.ConfigException as e:
        print(f"Failed to load kubeconfig file: {e}")
        exit(1)

# Try to load in-cluster config, fallback to kubeconfig file if needed
try:
    config.load_incluster_config()
    print("Loaded in-cluster Kubernetes configuration")
except config.config_exception.ConfigException as e:
    print(f"Failed to load in-cluster configuration: {e}")
    load_kube_config()

# Create an API client to interact with the Kubernetes cluster
v1 = client.CoreV1Api()

def scan_all_namespaces():
    """Scan all namespaces and list container names with their image versions."""
    namespaces = v1.list_namespace().items
    for namespace in namespaces:
        namespace_name = namespace.metadata.name
        print(f"\n--- Scanning namespace: {namespace_name} ---")
        pods = v1.list_namespaced_pod(namespace_name).items
        for pod in pods:
            containers = pod.spec.containers
            for container in containers:
                print(f"Container Name: {container.name}, Image: {container.image}")

if __name__ == "__main__":
    scan_all_namespaces()
