import os 
from dotenv import load_dotenv

load_dotenv(override=True)
class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_API_KEY = os.getenv('SECRET_API_KEY', 'random_key_1234')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'file_object_storage/')
    VIDEO_LENGTH_LIMIT_SECONDS = int(os.getenv('VIDEO_LENGTH_LIMIT_SECONDS', '30'))
    VIDEO_SIZE_LIMIT_MB = int(os.getenv('VIDEO_SIZE_LIMIT_MB', '25')) * 1024 * 1024
    VIDEO_LENGTH_MIN_SECONDS = int(os.getenv('VIDEO_LENGTH_MIN_SECONDS', '10'))
