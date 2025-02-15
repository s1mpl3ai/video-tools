import os 

class Config : 
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_API_KEY = os.environ.get('SECRET_API_KEY', 'random_key_1234')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'file_object_storage/')
    VIDEO_LENGTH_LIMIT_SECONDS = int(os.environ.get('VIDEO_LENGTH_LIMIT_SECONDS'))
    VIDEO_SIZE_LIMIT_MB = int(os.environ.get('VIDEO_SIZE_LIMIT_MB','25')) * 1024 * 1024