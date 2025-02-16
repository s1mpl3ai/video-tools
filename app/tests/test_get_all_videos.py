import unittest
from unittest.mock import patch
from app import create_app
from app.services.video_service import VideoService
from flask import json

class TestGetAllVideos(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and mock dependencies."""
        self.app = create_app()
        self.client = self.app.test_client()
    
    @patch("app.services.video_service.VideoService.get_all_videos")
    def test_get_all_videos_success(self, mock_get_all_videos):
       
        mock_get_all_videos.return_value = [
            {
                "label": "Sample Video",
                "filename": "example.mp4",
                "mime_type": "video/mp4",
                "length": 10.5,
                "size_mb": round(5485760 / (1024 * 1024), 2), 
                "uploaded_time": "2025-02-17 14:30:00"
            }
        ]
        response = self.client.get("/api/v1/videos/all")
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("videos", data)
        self.assertEqual(len(data["videos"]), 1)
        self.assertNotIn("file_path", data["videos"][0])  
        self.assertAlmostEqual(data["videos"][0]["size_mb"], 5.23, places=2)  
    
    @patch("app.services.video_service.VideoService.get_all_videos")
    def test_get_all_videos_empty(self, mock_get_all_videos):
        mock_get_all_videos.return_value = []
        response = self.client.get("/api/v1/videos/all")
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["videos"], [])
    
    @patch("app.services.video_service.VideoService.get_all_videos")
    def test_get_all_videos_failure(self, mock_get_all_videos):
        mock_get_all_videos.side_effect = Exception("Database error")
        response = self.client.get("/api/v1/videos/all")
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Database error")
    
    def tearDown(self):
        
        pass  

if __name__ == "__main__":
    unittest.main()
