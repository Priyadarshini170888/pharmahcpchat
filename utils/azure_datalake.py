
from azure.storage.filedatalake import DataLakeServiceClient
import config
import io

def get_service_client():
    return DataLakeServiceClient(
        account_url=f"https://{config.AZURE_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
        credential=config.AZURE_STORAGE_ACCOUNT_KEY
    )

def upload_file_to_datalake(file_stream, file_name):
    service_client = get_service_client()
    file_system_client = service_client.get_file_system_client(file_system=config.AZURE_FILE_SYSTEM)
    directory_client = file_system_client.get_directory_client("")
    file_client = directory_client.create_file(file_name)
    data = file_stream.read()
    file_client.append_data(data, 0, len(data))
    file_client.flush_data(len(data))

def download_file_from_datalake(file_name):
    service_client = get_service_client()
    file_system_client = service_client.get_file_system_client(file_system=config.AZURE_FILE_SYSTEM)
    file_client = file_system_client.get_file_client(file_name)
    download = file_client.download_file()
    return io.BytesIO(download.readall())
