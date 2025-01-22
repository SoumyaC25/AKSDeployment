from ipaddress import ip_network

def calculate_required_ips(nodepools):
    """
    Calculates the total number of IPs required for the AKS cluster based on the nodepools.
    """
    total_ips = sum(pool['nodes'] * pool['pods'] for pool in nodepools)
    return total_ips

def validate_vnet_space(vnet_cidr, required_ips):
    """
    Validates if the VNet has enough IP space to accommodate the required IPs.
    """
    vnet = ip_network(vnet_cidr)
    available_ips = vnet.num_addresses - 2  # Subtract network and broadcast addresses
    if required_ips > available_ips:
        raise ValueError(f"Not enough IP addresses in the VNet. Required: {required_ips}, Available: {available_ips}.")
