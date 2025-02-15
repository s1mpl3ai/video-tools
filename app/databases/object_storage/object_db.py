import os
from flask import abort, send_file
from app.config import Config

class LocalFileServer:
    
    def __init__(self, video_repository):    
        self.object_store = Config().UPLOAD_FOLDER

    def get_file(self, file_path, download_name=None):
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=download_name or os.path.basename(file_path)
        )
    
    def save_file(self, file, file_name):
        file_path = os.path.join(self.object_store, file_name)
        file.save(file_path)
        return file_path