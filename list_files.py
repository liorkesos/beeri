# file: list_files.py

from googleapiclient.discovery import build
from google.oauth2 import service_account

def list_files_in_folder(folder_id, credentials_json):
    """
    List all files in a specified Google Drive folder.

    Args:
        folder_id (str): The ID of the Google Drive folder.
        credentials_json (str): Path to the service account credentials JSON file.

    Returns:
        List[Dict]: A list of file metadata dictionaries.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        credentials_json, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)

    query = f"'{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(q=query).execute()
    files = results.get('files', [])
    return files

# Usage example
if __name__ == "__main__":
    folder_id = 'your-folder-id'
    credentials_json = 'path/to/credentials.json'
    file_list = list_files_in_folder(folder_id, credentials_json)
    for file in file_list:
        print(f"Name: {file['name']}, ID: {file['id']}")