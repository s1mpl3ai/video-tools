import os 
import cv2 
import time
from werkzeug.utils import secure_filename
from app.config import Config
import tempfile
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer as Serializer, SignatureExpired, BadSignature
from app.config import Config
import subprocess
import logging 
logger = logging.getLogger(__name__)

class VideoUtils: 
    def __init__(self):
        self.upload_folder = Config.UPLOAD_FOLDER
        self.allowed_extensions = {'mp4', 'avi', 'mov', 'flv', 'wmv', 'mkv'}
        self.max_video_length = Config.VIDEO_LENGTH_LIMIT_SECONDS
        self.max_video_size = Config.VIDEO_SIZE_LIMIT_MB
        self.config = Config()

    def is_allowed_extension(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def get_file_size(self, file):
        file.seek(0, os.SEEK_END)  
        file_size = file.tell()  
        file.seek(0) 
        return file_size

    def get_video_length(self, file):
        with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as temp:
            file.seek(0)
            temp.write(file.read())
            temp_path = temp.name

        try: 
            video = cv2.VideoCapture(temp_path)
            if not video.isOpened():
                raise ValueError('Could not open the video file')
            frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = video.get(cv2.CAP_PROP_FPS)
            if fps == 0 : 
                raise ValueError('Could not get the frames per second')
            video_length = frames / fps
            video.release()
        finally:
            os.remove(temp_path)
        return video_length
    
    def get_mime_type(self, file):
        try: 
            return file.mime_type
        except: 
            return "Unknown"
    
    def save_video(self, file):
        filename = secure_filename(file.filename)
        if not self.is_allowed_extension(filename):
            raise ValueError('Invalid file extension')
        
        file_size = self.get_file_size(file)
        if file_size > self.max_video_size:
            raise ValueError('File size exceeds the limit')
        
        file_duration = self.get_video_length(file)
        if file_duration > self.max_video_length:
            raise ValueError('File duration exceeds the limit')

        mime_type = self.get_mime_type(file)

        file_path = os.path.join(self.upload_folder, filename)
        file.seek(0)
        file.save(file_path)

        return {
            'file_name': filename,
            'file_path': file_path,
            'mime_type': mime_type,
            'length': file_duration,
            'size': file_size
        }

    def get_video_link(self, file_path , expiry_time_minutes = 60):

        logger.info("Generating video link for file: %s with expiry time: %d minutes", file_path, expiry_time_minutes)
        expiry_time = expiry_time_minutes * 60
        expiry_timestamp = expiry_time + int(time.time())

        s = Serializer(self.config.SECRET_API_KEY)
        token = s.dumps({'file_path': file_path,'expiry':expiry_timestamp})
        
        download_url = url_for('videos_bp.download_file', token=token, _external=True)
        logger.info("Download URL generated: %s", download_url)

        return download_url
    
    def verify_download_token(self,token): 
        s = Serializer(self.config.SECRET_API_KEY)
        try:
            data = s.loads(token)
            logger.info("Token loaded successfully: %s", data)
        except BadSignature:
            logger.error("Token missing expiry information: %s", data)
            raise ValueError('Invalid token')
        
        expiry_timestamp = data.get('expiry')
        if expiry_timestamp < int(time.time()):
            logger.error("Token has expired. Expiry timestamp: %d, current time: %d", expiry_timestamp, int(time.time()))
            raise ValueError('Token has expired')
        print(data.get('file_path'))
        return data.get('file_path')
    
    def trim_video_file(self, original_path, start, end, output_path):
        # Additional checks have already been performed at a higher level.
        logger.info("Trimming file %s from %s to %s seconds", original_path, start, end)
        command = [
            "ffmpeg",
            "-i", original_path,
            "-ss", str(start),
            "-to", str(end),
            "-c", "copy",
            output_path
        ]
        subprocess.run(command, check=True)
        logger.info("Trimmed video saved to %s", output_path)

    
    def merge_video_files(self, file_paths, output_path):
       
        logger.info("Merging video files: %s", file_paths)
        # Check that each file exists.
        for path in file_paths:
            if not os.path.exists(path):
                logger.error("File does not exist: %s", path)
                raise ValueError(f"File not found: {path}")

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as list_file:
            for path in file_paths:
                list_file.write(f"file '{path}'\n")
            list_filename = list_file.name

        try:
            command = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", list_filename,
                "-fflags", "+genpts",       # Regenerate timestamps
                "-r", "30",                 # Force 30 FPS output (optional)
                "-c", "copy",               # No re-encoding
                "-metadata:s:v", "rotate=0",  # Strip rotation metadata
                "-video_track_timescale", "30k",  # Standardize timebase
                "-movflags", "+faststart",
                "-y",
                output_path
            ]
            # logger.info("Running FFmpeg command: %s", " ".join(command))
            subprocess.run(command, check=True)
            logger.info("Merged video saved to %s", output_path)
        
        except subprocess.CalledProcessError as e:
            logger.error("Error merging videos: %s", e)
            raise 
        finally:
            os.remove(list_filename)
        logger.info("Merge completed sucessfully %s", output_path)