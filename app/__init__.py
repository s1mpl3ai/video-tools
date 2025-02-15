from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from app.databases.sqlite.connection import Database
from dotenv import load_dotenv
from flask_migrate import Migrate
db = SQLAlchemy()

def create_app():
    load_dotenv(override=True)
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 
    db_instance = Database(app)
    Migrate(app, db_instance.db)
    # db_instance.init_app(app)

    from .services.video_service import VideoService
    app.video_service = VideoService(db_instance.db)

    from .routes.videos import videos_bp
    app.register_blueprint(videos_bp, url_prefix='/api/v1/videos')

    return app

from werkzeug.exceptions import RequestEntityTooLarge
