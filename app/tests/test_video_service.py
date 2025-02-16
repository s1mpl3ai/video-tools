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
    def test_trim_video_invalid_times(self):
        self.mock_repo.get.return_value = MagicMock(length=10)
        with self.assertRaises(ValueError):
            self.service.trim_video(1, 5, 2)
    
    def test_trim_video_exceeds_length(self):
        self.mock_repo.get.return_value = MagicMock(length=10)
        with self.assertRaises(ValueError):
            self.service.trim_video(1, 2, 15)
    
    def test_merge_videos_invalid_list(self):
        self.mock_repo.get.side_effect = lambda vid: None if vid == 999 else MagicMock(mime_type='video/mp4', file_path=f"video{vid}.mp4")
        with self.assertRaises(ValueError):
            self.service.merge_videos([1, 999])
    
    def test_get_video_link_not_found(self):
        self.mock_repo.get.return_value = None
        with self.assertRaises(Exception):
            self.service.get_video_link(1, 30)
    
    def test_download_invalid_token(self):
        self.mock_utils.verify_download_token.side_effect = Exception("Invalid token")
        with self.assertRaises(Exception):
            self.service.download("invalid_token")

if __name__ == "__main__":
    unittest.main()
