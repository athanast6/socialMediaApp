from io import BytesIO
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import os



AZURE_STORAGE_ACCOUNT = os.environ['AZURE_STORAGE_ACCOUNT']
AZURE_STORAGE_KEY_NAME = os.environ['AZURE_STORAGE_KEY_NAME']

#Remove before building.
#key = ""

def get_blob_service_client_account_key():
    # TODO: Replace <storage-account-name> with your actual storage account name
    account_url = "https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net"
    #account_url = "https://athanast6.blob.core.windows.net"
    #shared_access_key = os.getenv("AZURE_STORAGE_ACCESS_KEY")
    #credential = key
    credential = AZURE_STORAGE_KEY_NAME

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    return blob_service_client



def upload_blob_file(blob_service_client: BlobServiceClient, file, filename, container_name: str):
    
    container_client = blob_service_client.get_container_client(container=container_name)

    blob_client = container_client.get_blob_client(blob=filename)
    if blob_client.exists():
        # Delete the existing file
        blob_client.delete_blob()
    
    container_client.upload_blob(name=filename, data=file)
