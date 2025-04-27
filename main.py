from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient

# Authenticate
credential = AzureCliCredential()

# Your Azure Subscription ID
subscription_id = '318ee8c9-e6f9-4b5f-b0bf-eed50d3da920'  # <-- your real subscription ID

# Create clients
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

# Define your Resource Group and Storage Account information
resource_group_name = "practice-resource-group"
storage_account_name = "practicestoracct123"  # Must be lowercase and unique
location = "eastus"

# First: Create (or make sure) the Resource Group exists
rg_result = resource_client.resource_groups.create_or_update(
    resource_group_name,
    {"location": location}
)

print(f"Resource Group '{rg_result.name}' created or already exists in {rg_result.location}.")

# Then: Create the Storage Account
poller = storage_client.storage_accounts.begin_create(
    resource_group_name,
    storage_account_name,
    {
        "location": location,
        "sku": {"name": "Standard_LRS"},
        "kind": "StorageV2",
        "enable_https_traffic_only": True
    }
)

account_result = poller.result()

print(f"Storage Account '{account_result.name}' created successfully in {account_result.primary_location}.")
