import unittest
from unittest.mock import MagicMock
from app.databases.sqlite.repository import VideoRepository
from app.databases.sqlite.models import Video

class TestVideoRepository(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()
        self.repo = VideoRepository(self.mock_db)

    def test_create_video(self):
        video_data = {
            'file_name': 'test.mp4',
            'file_path': '/dummy/path/test.mp4',
            'mime_type': 'video/mp4',
            'length': 120.5,
            'size': 102400,
            'label': 'Test Video'
        }
        self.repo.create(video_data)
        self.mock_db.session.add.assert_called()
        self.mock_db.session.commit.assert_called()

    def test_get_video(self):
        video = Video(id=1, file_name="test.mp4", file_path="/dummy/path/test.mp4")
        self.mock_db.session.query().get.return_value = video
        result = self.repo.get(1)
        self.assertEqual(result.file_name, "test.mp4")

if __name__ == "__main__":
    unittest.main()
