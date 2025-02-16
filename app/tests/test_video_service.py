import unittest
from unittest.mock import MagicMock
from app.services.video_service import VideoService

class TestVideoService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_utils = MagicMock()
        self.mock_object_db = MagicMock()
        self.service = VideoService(self.mock_repo)
        self.service.video_repository = self.mock_repo
        self.service.video_utils = self.mock_utils
        self.service.object_db = self.mock_object_db

    def test_create_video(self):
        mock_file = MagicMock()
        self.service.create(mock_file, "Test Video")
        self.mock_utils.save_video.assert_called()
        self.mock_repo.create.assert_called()

    def test_get_video(self):
        self.mock_repo.get.return_value = MagicMock()
        video = self.service.get(1)
        self.assertIsNotNone(video)

if __name__ == "__main__":
    unittest.main()
