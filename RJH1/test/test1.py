from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

SCOPES= ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUTNT_FILE='service_account.json'
PARENT_FOLDER_ID="1TPMiu4rRgDlu0f_RkFRpJsoHGovRtQ_u"

def authenticate():
    creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUTNT_FILE,scopes=SCOPES)
    return creds

def upload_photo(file_path):
    creds=authenticate()
    service=build('drive','v3',credentials=creds)

    file_metadata={
        'name': "Hello",
        'parents':[PARENT_FOLDER_ID]
    }

    file=service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()
    file_id = file.get('id')
    file_link = f"https://drive.google.com/file/d/{file_id}"
    
    print(f"Uploaded file: {file_link}")
    os.remove(file_path)

upload_photo("downloaded_image.jpg")
