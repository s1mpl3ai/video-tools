from app.databases.sqlite.models import Video
from app.databases.sqlite.connection import Database


class VideoRepository:
    def __init__(self,db):
        self.db= db
        

    def create(self, video):
        try: 
            new_video = Video(file_name=video['file_name'], file_path=video['file_path'],
                            mime_type=video['mime_type'], length=video['length'],
                            size=video['size'], label=video['label'])
            self.db.session.add(new_video)
            self.db.session.commit()
            return new_video
        except Exception as e:
            self.db.session.rollback()
            raise e   

    def get(self, id):
        
        return self.db.session.query(Video).get(id)

    def get_all(self):
        session = self.get_session()
        return self.db.session.query(Video).all()

    
