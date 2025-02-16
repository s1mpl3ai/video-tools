from app.databases.sqlite.repository import VideoRepository
from app.utils.video_utils import VideoUtils
from app.databases.object_storage.object_db import LocalFileServer
import uuid
import os
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
    
    def trim_video(self, video_id, start, end):
       
        original_video = self.get(video_id)
        if not original_video:
            raise ValueError("Video not found")
        
        if start < 0:
            raise ValueError("Start time must be non-negative")
        if end <= start:
            raise ValueError("End time must be greater than start time")
        if end > original_video.length:
            raise ValueError("End time exceeds original video duration")
        
        original_path = original_video.file_path
        new_filename = f"trimmed_{uuid.uuid4().hex}_{os.path.basename(original_path)}"
        new_file_path = os.path.join(self.video_utils.upload_folder, new_filename)

        try:
            self.video_utils.trim_video_file(original_path, start, end, new_file_path)
        except Exception as e:
            raise Exception("Error trimming video: " + str(e))
        
        new_size = os.path.getsize(new_file_path)
        new_length = end - start

        new_video_info = {
            'file_name': new_filename,
            'file_path': new_file_path,
            'mime_type': original_video.mime_type,
            'length': new_length,
            'size': new_size,
            'label': original_video.label + " (trimmed)"
        }
        return self.video_repository.create(new_video_info)
    

    def merge_videos(self, video_ids):
        print(str(self.get_all()))

        videos = [self.get(vid) for vid in video_ids]
        if any(v is None for v in videos):
            raise ValueError("One or more videos not found")
        
        file_paths = [video.file_path for video in videos]

        new_filename = f"merged_{uuid.uuid4().hex}_{os.path.basename(file_paths[0])}"
        new_file_path = os.path.join(self.video_utils.upload_folder, new_filename)

        try:
            self.video_utils.merge_video_files(file_paths, new_file_path)
        except Exception as e:
            raise Exception("Error merging videos: " + str(e))
        
        total_length = sum(video.length for video in videos)
        new_size = os.path.getsize(new_file_path)

        new_video_info = {
            'file_name': new_filename,
            'file_path': new_file_path,
            'mime_type': videos[0].mime_type, 
            'length': total_length,
            'size': new_size,
            'label': "Merged Video"
        }
        return self.video_repository.create(new_video_info)
    
    def get_all_videos(self):
        try:
            videos = self.video_repository.get_all()
            return [
                {
                    "label": video.label,
                    "filename": video.file_name,
                    "mime_type": video.mime_type,
                    "length": round(video.length, 2),  
                    "size_mb": round(video.size / (1024 * 1024), 2), 
                    "uploaded_time": video.uploaded_at.strftime("%Y-%m-%d %H:%M:%S")  
                }
                for video in videos
            ]
        except Exception as e:
            raise Exception(f"Error fetching all videos: {str(e)}")
