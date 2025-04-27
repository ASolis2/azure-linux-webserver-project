from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

# Authenticate
credential = AzureCliCredential()

# Your Azure Subscription ID
subscription_id = '318ee8c9-e6f9-4b5f-b0bf-eed50d3da920'

# Create clients
resource_client = ResourceManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Set basic variables
resource_group_name = "practice-resource-group"
location = "eastus"

# Create Virtual Network
vnet_name = "practice-vnet"
subnet_name = "practice-subnet"

vnet_params = {
    "location": location,
    "address_space": {
        "address_prefixes": ["10.0.0.0/16"]
    }
}

vnet_result = network_client.virtual_networks.begin_create_or_update(
    resource_group_name,
    vnet_name,
    vnet_params
).result()

print(f"Virtual Network '{vnet_result.name}' created.")

# Create Subnet
subnet_params = {
    "address_prefix": "10.0.0.0/24"
}

subnet_result = network_client.subnets.begin_create_or_update(
    resource_group_name,
    vnet_name,
    subnet_name,
    subnet_params
).result()

print(f"Subnet '{subnet_result.name}' created.")

# Create Public IP Address
public_ip_name = "practice-public-ip"

public_ip_params = {
    "location": location,
    "public_ip_allocation_method": "Dynamic"
}

public_ip_result = network_client.public_ip_addresses.begin_create_or_update(
    resource_group_name,
    public_ip_name,
    public_ip_params
).result()

print(f"Public IP '{public_ip_result.name}' created.")

# Create Network Interface
nic_name = "practice-nic"

nic_params = {
    "location": location,
    "ip_configurations": [{
        "name": "practice-ip-config",
        "subnet": {
            "id": subnet_result.id
        },
        "public_ip_address": {
            "id": public_ip_result.id
        }
    }]
}

nic_result = network_client.network_interfaces.begin_create_or_update(
    resource_group_name,
    nic_name,
    nic_params
).result()

print(f"Network Interface '{nic_result.name}' created.")
