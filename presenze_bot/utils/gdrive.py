"""
Integrazione Google Drive tramite gspread.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from config.settings import GOOGLE_CREDENTIALS_JSON
from utils.logger import logger

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def get_gspread_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_JSON, SCOPES)
    return gspread.authorize(creds)

def get_or_create_user_folder(gc, cf: str):
    """
    Restituisce l'ID della cartella su Drive col nome cf.
    Se non esiste la crea.
    """
    drive = gc.auth.service
    results = drive.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{cf}'", fields="files(id, name)").execute()
    folders = results.get('files', [])
    if folders:
        return folders[0]['id']
    file_metadata = {'name': cf, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.files().create(body=file_metadata, fields='id').execute()
    logger.info(f"Creata cartella Drive per {cf}: {folder['id']}")
    return folder['id']

def upload_excel_to_drive(gc, folder_id: str, local_path: str, remote_name: str):
    drive = gc.auth.service
    file_metadata = {
        'name': remote_name,
        'parents': [folder_id],
        'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(local_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    uploaded = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
    logger.info(f"Caricato file {remote_name} su Drive in {folder_id}: {uploaded['id']}")
    return uploaded['id']