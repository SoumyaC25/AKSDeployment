import os
import re
from typing import List
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.containerservice import ContainerServiceClient

class UserInputValidator:
    @staticmethod
    def validate_aks_name(name: str):
        if not re.match(r"^[a-zA-Z0-9-]+$", name):
            raise ValueError("AKS Name must be alphanumeric with dashes.")

    @staticmethod
    def validate_subscription_id(subscription_id: str):
        if not re.match(r"^[a-f0-9-]{36}$", subscription_id):
            raise ValueError("Invalid Subscription ID format.")

    @staticmethod
    def validate_resource_group(name: str):
        if not name:
            raise ValueError("Resource group name cannot be empty.")

    @staticmethod
    def validate_node_pool(node_pool_name: str, nodes: int, network_type: str, pod_count: int):
        if not re.match(r"^[a-zA-Z0-9-]+$", node_pool_name):
            raise ValueError("Node pool name must be alphanumeric with dashes.")
        if nodes < 3:
            raise ValueError("Node pool must have at least 3 nodes.")
        if network_type not in ["kubenet", "azureCNI", "Overlay"]:
            raise ValueError("Invalid network type.")
        if pod_count <= 10:
            raise ValueError("Pod count must be greater than 10.")

    @staticmethod
    def validate_rbac_type(rbac_type: str, user_groups: List[str]):
        if rbac_type == "kuberbac" and not user_groups:
            raise ValueError("User groups are required for kuberbac RBAC type.")
