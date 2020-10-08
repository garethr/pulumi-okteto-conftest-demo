import pulumi
from pulumi import Config, ResourceOptions
from pulumi_kubernetes import Provider
from pulumi_kubernetes.apps.v1 import Deployment

config = Config()

namespace = config.get("namespace") or "default"

provider = Provider("kubernetes", namespace=namespace)

app_labels = {"app": "nginx"}

replicas = config.get("replicas") or 1

deployment = Deployment(
    "nginx",
    spec={
        "selector": {"match_labels": app_labels},
        "replicas": replicas,
        "template": {
            "metadata": {"labels": app_labels},
            "spec": {"containers": [{"name": "nginx", "image": "nginx"}]},
        },
    },
    opts=ResourceOptions(provider=provider),
)

pulumi.export("name", deployment.metadata["name"])
