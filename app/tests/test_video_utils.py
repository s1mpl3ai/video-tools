import unittest
from app.utils.video_utils import VideoUtils
from unittest.mock import mock_open, patch
import io

class TestVideoUtils(unittest.TestCase):
    def setUp(self):
        self.utils = VideoUtils()
        self.mock_file = io.BytesIO(b"Fake video data")  # Mock a file object

    def test_get_file_size(self):
        """Test getting the size of a file."""
        self.mock_file.seek(0, io.SEEK_END)  # Move to the end to simulate a file
        expected_size = self.mock_file.tell()  # Get file size
        self.mock_file.seek(0)  # Reset for testing

        size = self.utils.get_file_size(self.mock_file)  # Pass file object
        self.assertEqual(size, expected_size)  # Ensure size matches

if __name__ == "__main__":
    unittest.main()
