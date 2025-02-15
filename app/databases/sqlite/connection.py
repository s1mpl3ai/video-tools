from flask_sqlalchemy import SQLAlchemy
from app.utils.singleton import SingletonMeta
from flask_migrate import  upgrade


class Database(metaclass=SingletonMeta):
   
    def __init__(self, app=None):
        self.db = SQLAlchemy()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        
        self.db.init_app(app)
        with app.app_context():
            self.db.create_all()
           

    def __enter__(self):
        
        self.session = self.db.session()
        return self.session

    def __exit__(self, exc_type):
        
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()