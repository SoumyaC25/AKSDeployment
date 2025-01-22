import os
import re
from typing import List
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.containerservice import ContainerServiceClient

class VNetManager:
    def __init__(self, subscription_id: str):
        self.credential = DefaultAzureCredential()
        self.network_client = NetworkManagementClient(self.credential, subscription_id)

    def get_vnet_details(self, resource_group: str, vnet_name: str):
        return self.network_client.virtual_networks.get(resource_group, vnet_name)

    def calculate_available_ips(self, vnet):
        total_ips = 0
        for subnet in vnet.subnets:
            address_prefix = subnet.address_prefix
            subnet_size = 2 ** (32 - int(address_prefix.split("/")[1]))
            total_ips += subnet_size
        return total_ips
