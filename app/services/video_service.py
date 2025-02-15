from app.databases.sqlite.repository import VideoRepository
from app.utils.video_utils import VideoUtils

class VideoService:
    def __init__(self,db):
        self.video_repository = VideoRepository(db)
        self.video_utils = VideoUtils()

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