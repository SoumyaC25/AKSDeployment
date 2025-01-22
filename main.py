import os
import re
from typing import List
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.containerservice import ContainerServiceClient

class AKSClusterManager:
    def __init__(self, subscription_id: str):
        self.credential = DefaultAzureCredential()
        self.aks_client = ContainerServiceClient(self.credential, subscription_id)

    def create_cluster(self, resource_group: str, cluster_name: str, params):
        return self.aks_client.managed_clusters.begin_create_or_update(
            resource_group, cluster_name, params
        )


# Main function for user input and processing
def main():
    print("Enter the following details to deploy an AKS cluster:")
    aks_name = input("AKS Name: ")
    subscription_id = input("Subscription ID: ")
    resource_group = input("Resource Group Name: ")
    vnet_name = input("VNet Name: ")

    node_pools = []
    for i in range(2):
        print(f"Node Pool {i + 1}:")
        name = input("  Name: ")
        nodes = int(input("  Number of nodes (min 3): "))
        network_type = input("  Network type (kubenet, azureCNI, Overlay): ")
        pod_count = int(input("  Number of pods (min > 10): "))
        node_pools.append((name, nodes, network_type, pod_count))

    rbac_type = input("RBAC Type (standard, kuberbac): ")
    user_groups = []
    if rbac_type == "kuberbac":
        user_groups = input("Comma-separated user groups: ").split(",")

    # Validation
    try:
        UserInputValidator.validate_aks_name(aks_name)
        UserInputValidator.validate_subscription_id(subscription_id)
        UserInputValidator.validate_resource_group(resource_group)
        for name, nodes, network_type, pod_count in node_pools:
            UserInputValidator.validate_node_pool(name, nodes, network_type, pod_count)
        UserInputValidator.validate_rbac_type(rbac_type, user_groups)
    except ValueError as e:
        print(f"Input validation error: {e}")
        return

    # VNet Management
    vnet_manager = VNetManager(subscription_id)
    vnet = vnet_manager.get_vnet_details(resource_group, vnet_name)
    available_ips = vnet_manager.calculate_available_ips(vnet)

    required_ips = sum(pool[1] * 30 for pool in node_pools)  # Example calculation
    if available_ips < required_ips:
        print("Insufficient IPs in the VNet to deploy the cluster.")
        return

    print("Validated and ready to deploy the cluster.")

if __name__ == "__main__":
    main()
