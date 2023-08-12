from flask import Flask
from g_drive_service import GoogleDriveService
import os
from googleapiclient.http import MediaFileUpload

app=Flask(__name__)


def get_folder_id(service, folder_name):
    results = service.files().list(q=f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'",
                                   fields="files(id)").execute()
    items = results.get('files', [])
    if items:
        return items[0]['id']
    else:
        return None
    
def create_folder(service, folder_name, parent_folder_id=None):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    print(folder_metadata)
    if parent_folder_id:
        print(parent_folder_id)
        folder_metadata['parents'] = [parent_folder_id]

    folder = service.files().create(body=folder_metadata,
                                    fields='id').execute()
    return folder.get('id')


def upload_file(service, folder_id, file_name):
    media_body = MediaFileUpload(file_name, mimetype='video/mp4', resumable=True)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    file = service.files().create(body=file_metadata,
                                  media_body=media_body,
                                  fields='id').execute()
    

@app.get('/gdrive-files')
def getFileListFromGDrive():
    selected_fields="files(id,name,webViewLink)"
    g_drive_service=GoogleDriveService().build()
    list_file=g_drive_service.files().list(fields=selected_fields).execute()
    folder_name = "Videos"
    folder_id = get_folder_id(g_drive_service, folder_name)
    folder_name2 = "NewFolder"  # Replace with the desired folder name
    file_name = "clip.mp4"  # Replace with the desired file name
    parent_folder_id = "1N4i1DnEQeR_vCDLrpW9ZlFWW7FFUPO4s"
    g_drive_service = GoogleDriveService().build()

    # Create a folder
    folder_id = create_folder(g_drive_service, folder_name2,parent_folder_id)

    if folder_id:
        # Upload a file to the folder
        upload_file(g_drive_service, folder_id, file_name)

        return {"message": f"Folder '{folder_name}' created and file '{file_name}' uploaded."}
    else:
        return {"error": f"Folder '{folder_name}' could not be created."}
    

    if folder_id:
        query = f"'{folder_id}' in parents"
        results = g_drive_service.files().list(q=query).execute()
        files = results.get('files', [])

        if files:
            return {"files": files}
        else:
            return {"error": "No files found in the specified folder."}
    else:
        return {"error": f"Folder '{folder_name}' not found in Google Drive."}


if __name__=='__main__':
    app.run(debug=True)