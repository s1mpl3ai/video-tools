from app.databases.sqlite.repository import VideoRepository
from app.utils.video_utils import VideoUtils
from app.databases.object_storage.object_db import LocalFileServer

class VideoService:
    def __init__(self,db):
        self.video_repository = VideoRepository(db)
        self.video_utils = VideoUtils()
        self.object_db = LocalFileServer(self.video_repository)

    def create(self, video ,label):
        try : 
            video_info = self.video_utils.save_video(video)
            video_info['label'] = label
            return self.video_repository.create(video_info)
        except Exception as e:
            raise e

    def get(self, id):
        return self.video_repository.get(id)

    def get_all(self):
        return self.video_repository.get_all()
    
    def get_video_link(self, id , exiperation_time):
        try:
            video = self.get(id)
            return self.video_utils.get_video_link(video.file_path,expiry_time_minutes=exiperation_time)
        except Exception as e:
            raise e
            
    def download(self,token): 
        try: 
            file_path = self.video_utils.verify_download_token(token)
            print("rrecieved_file_path",file_path)
            return self.object_db.get_file(file_path)
        except Exception as e:
            raise e
    