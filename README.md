# AKSDeployment

The Python script provides the structure to deploy an AKS cluster with validation for user inputs and calculation of required IPs.

File Structure Proposal:
main.py: Entry point of the application (provided script).
azure_services/:
aks_deployer.py: Contains the AKSClusterDeployer class.
utils/:
validators.py: Functions to validate inputs.
ip_calculator.py: IP calculation logic.
configs/:
default_config.json: Store default values (e.g., node counts).
