from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient

# Authenticate
credential = AzureCliCredential()

# Your Azure Subscription ID
subscription_id = '318ee8c9-e6f9-4b5f-b0bf-eed50d3da920'

# Create clients
compute_client = ComputeManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Set variables
resource_group_name = "practice-resource-group"
location = "eastus"
vm_name = "practice-linux-vm"
nic_name = "practice-nic"

# Get NIC ID
nic = network_client.network_interfaces.get(resource_group_name, nic_name)

# VM parameters
vm_parameters = {
    "location": location,
    "storage_profile": {
      "image_reference": {
    "publisher": "Debian",
    "offer": "debian-11",
    "sku": "11",
    "version": "latest"
}


    },
    "hardware_profile": {
        "vm_size": "Standard_B1s"  # Small, low-cost VM for practice
    },
    "os_profile": {
        "computer_name": vm_name,
        "admin_username": "azureuser",  # Login username
        "admin_password": "9Ef7a63c?",  # <-- Change this to your own strong password!
    },
    "network_profile": {
        "network_interfaces": [{
            "id": nic.id
        }]
    }
}

# Create the VM
print(f"Creating Linux VM '{vm_name}'... This might take 2-5 minutes...")
creation_result = compute_client.virtual_machines.begin_create_or_update(
    resource_group_name,
    vm_name,
    vm_parameters
).result()

print(f"VM '{vm_name}' created successfully!")
