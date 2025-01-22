# validators.py: Functions to validate inputs
def validate_aks_name(aks_name):
    if not aks_name.strip():
        raise ValueError("AKS Name cannot be empty.")

def validate_nodepools(nodepools):
    for pool in nodepools:
        if pool['nodes'] < 3:
            raise ValueError(f"Node count for node pool '{pool['name']}' must be at least 3.")
        if pool['pods'] <= 10:
            raise ValueError(f"Pod count for node pool '{pool['name']}' must be greater than 10.")

def validate_cluster_type(cluster_type, rbac_groups):
    if cluster_type == 'Shared' and not rbac_groups:
        raise ValueError("Admin users must be specified for a shared cluster.")

def validate_rbac_type(rbac_type, rbac_groups):
    if rbac_type == 'kuberbac' and not rbac_groups:
        raise ValueError("RBAC user groups must be specified for 'kuberbac' type.")
