import unittest
from flask import Flask
from app.databases.sqlite.connection import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        self.db = Database()  

    def test_init_app(self):
        with self.app.app_context():
            self.db.init_app(self.app)

    def test_enter_exit(self):
        with self.app.app_context():
            with self.db as session:
                self.assertIsNotNone(session)  

if __name__ == "__main__":
    unittest.main()
