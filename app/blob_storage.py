from logging import debug
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, __version__
from datetime import datetime, timedelta
from azure.storage.blob import BlobClient, generate_blob_sas, BlobSasPermissions
from dotenv import load_dotenv

load_dotenv()

DOWNLOAD_PATH = os.path.join(os.getcwd(), 'download')

#Initializing the variable components
def blob_download_handler(blob_name):
    container_name = os.getenv('CONTAINER_NAME')

    # local_path=os.path.join(os.getcwd(),blob_name)
    # download_path=os.path.join(os.getcwd(),"download.blend")

    try:
        connect_str = os.getenv('BLOB_CONNECTION_STRING')

        if not os.path.exists(DOWNLOAD_PATH):
            os.makedirs(DOWNLOAD_PATH)
        

        # Create the BlobServiceClient object
        # blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        #Create a blob client using the local file name as the name for the blob
        # blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # with open(local_path, "rb") as data:     
        #     blob_client.upload_blob(data)

        blob_client = BlobClient.from_connection_string(connect_str, container_name, blob_name)
        # print(sas_url)
        FILE_DOWNLOAD_PATH = os.path.join(DOWNLOAD_PATH, blob_name)
        with open(FILE_DOWNLOAD_PATH, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        return FILE_DOWNLOAD_PATH
    except Exception as ex:
        print('Exception:')
        print(ex)
        return None
