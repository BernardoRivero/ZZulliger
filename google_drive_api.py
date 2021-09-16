from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

directorio_credenciales = 'credentials_module.json'

# Log into Google Drive  
def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()    
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

# Upload a file to Google Drive
def upload_file(file_path, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder}]})
    archivo['title'] = file_path.split("/")[-1]
    archivo['title'] = file_path.split(os.path.sep)[-1]
    archivo.SetContentFile(file_path)
    archivo.Upload()

def download_files(name_file):
    drive = login() 

    files = drive.ListFile({'q': "'1EQ4h-Blfc3PqySXRvViSVrq2ZhCmq2rl' in parents and trashed=false"}).GetList()
    for file in files:
        if name_file in file['title'] and file['fileExtension']=='png':
            print('Downloading the image: %s' % (file['title']))
            file.GetContentFile(file['title'])
