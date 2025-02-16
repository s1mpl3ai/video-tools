import unittest
from app.databases.sqlite.models import Video

class TestVideoModel(unittest.TestCase):

    def test_video_attributes(self):
        video = Video(
            id=1,
            label="Test Video",
            file_name="test.mp4",
            file_path="/dummy/path/test.mp4",
            mime_type="video/mp4",
            length=60.5,
            size=102400
        )
        self.assertEqual(video.label, "Test Video")
        self.assertEqual(video.file_name, "test.mp4")

if __name__ == "__main__":
    unittest.main()
