from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from app.databases.sqlite.connection import Database
from dotenv import load_dotenv
from flask_migrate import Migrate
import os 

db = SQLAlchemy()

def create_app():
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    load_dotenv(env_path,override=True)
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024 
    db_instance = Database(app)
    Migrate(app, db_instance.db)

    from .services.video_service import VideoService
    app.video_service = VideoService(db_instance.db)

    from .routes.videos import videos_bp
    app.register_blueprint(videos_bp, url_prefix='/api/v1/videos')

    return app

