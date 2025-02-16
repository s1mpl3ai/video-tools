import unittest
from unittest.mock import patch, MagicMock, mock_open
import io
import os
from app.utils.video_utils import VideoUtils

class TestVideoUtils(unittest.TestCase):
    def setUp(self):
        self.utils = VideoUtils()
        self.mock_file = io.BytesIO(b"Fake video data")  

    def test_get_file_size(self):
        self.mock_file.seek(0, io.SEEK_END)
        expected_size = self.mock_file.tell()
        self.mock_file.seek(0)
        
        size = self.utils.get_file_size(self.mock_file)
        self.assertEqual(size, expected_size)
    
    def test_is_allowed_extension(self):
        self.assertTrue(self.utils.is_allowed_extension("video.mp4"))
        self.assertFalse(self.utils.is_allowed_extension("video.txt"))
    
    @patch("app.utils.video_utils.cv2.VideoCapture")
    def test_get_video_length(self, mock_video_capture):
        mock_capture = MagicMock()
        mock_capture.isOpened.return_value = True
        mock_capture.get.side_effect = [100, 25]  
        mock_video_capture.return_value = mock_capture
        
        mock_file = io.BytesIO(b"Fake video data")
        length = self.utils.get_video_length(mock_file)
        self.assertAlmostEqual(length, 4.0)  
    
    def test_get_mime_type(self):
        self.assertEqual(self.utils.get_mime_type("video.mp4"), "mp4")
        self.assertEqual(self.utils.get_mime_type("video"), "Unknown")
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("app.utils.video_utils.os.path.join", return_value="/mock/path/video.mp4")
    @patch("app.utils.video_utils.VideoUtils.get_video_length", return_value=30)
    @patch("app.utils.video_utils.VideoUtils.get_file_size", return_value=1024 * 1024)
    def test_save_video(self, mock_get_file_size, mock_get_video_length, mock_path_join, mock_file_open):
        mock_file = MagicMock()
        mock_file.filename = "video.mp4"
        mock_file.save = MagicMock()
        
        result = self.utils.save_video(mock_file)
        self.assertIsInstance(result, dict)
        self.assertIn("file_name", result)
        self.assertIn("file_path", result)

    @patch("app.utils.video_utils.subprocess.run")
    @patch("app.utils.video_utils.os.path.exists", return_value=True)
    def test_trim_video_file(self, mock_exists, mock_subprocess):
        self.utils.trim_video_file("input.mp4", 5, 10, "output.mp4")
        mock_subprocess.assert_called_once()

    @patch("app.utils.video_utils.subprocess.run")
    @patch("app.utils.video_utils.os.path.exists", return_value=True)
    @patch("tempfile.NamedTemporaryFile", create=True)
    @patch("app.utils.video_utils.os.remove")  
    def test_merge_video_files_success(self, mock_remove, mock_tempfile, mock_exists, mock_subprocess):
        
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value.name = "/mock/path/temp_list.txt"
        mock_tempfile.return_value = mock_temp

        self.utils.merge_video_files(["video1.mp4", "video2.mp4"], "merged.mp4")

        mock_subprocess.assert_called_once()

        mock_temp.__enter__.return_value.write.assert_called()

        mock_remove.assert_called_with("/mock/path/temp_list.txt")
        
    @patch("app.utils.video_utils.os.path.exists", return_value=False)
    def test_merge_video_files_missing(self, mock_exists):
        with self.assertRaises(ValueError):
            self.utils.merge_video_files(["missing.mp4", "video2.mp4"], "merged.mp4")

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
