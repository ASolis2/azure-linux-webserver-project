from azure.identity import AzureCliCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient

# Authenticate
credential = AzureCliCredential()

# Your Azure Subscription ID
subscription_id = '318ee8c9-e6f9-4b5f-b0bf-eed50d3da920'

# Create Storage Management client
storage_client = StorageManagementClient(credential, subscription_id)

# Set variables
resource_group_name = "practice-resource-group"
storage_account_name = "practicestoracct123"
container_name = "practice-container"

# Get storage account keys
keys = storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
storage_keys = {v.key_name: v.value for v in keys.keys}
account_key = storage_keys['key1']

# Build the connection string
connection_string = (
    f"DefaultEndpointsProtocol=https;"
    f"AccountName={storage_account_name};"
    f"AccountKey={account_key};"
    f"EndpointSuffix=core.windows.net"
)

# Create Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create container if it doesn't exist
try:
    container_client = blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created.")
except Exception as e:
    print(f"Container might already exist: {e}")

# List of local files you want to upload
files_to_upload = [
    r"C:\Users\arays\OneDrive\Desktop\dog.jpg",   # <-- Replace with your first file full path
    r"C:\Users\arays\OneDrive\Desktop\cat.jpg"   # <-- Replace with your second file full path
]

# Upload each file
for file_path in files_to_upload:
    file_name = file_path.split("\\")[-1]  # Extracts the file name from the path
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"Uploaded '{file_name}' to container '{container_name}'.")
