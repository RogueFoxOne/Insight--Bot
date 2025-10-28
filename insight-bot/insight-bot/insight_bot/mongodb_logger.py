import os
from pymongo import MongoClient
import logging
from datetime import datetime

class MongoDBLogger:
    def __init__(self):
        try:
            self.client = MongoClient(os.getenv("MONGODB_URI"))
            self.db = self.client[os.getenv("DATABASE_NAME", "insight_bot_db")]
            self.collection = self.db.interactions
            logging.info("✓ MongoDB client initialized.")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            self.client = None

    def log_interaction(self, comment, response, plk_result):
        if not self.client:
            return
        
        doc = {
            "comment_id": comment.id,
            "author": comment.author.name,
            "subreddit": comment.subreddit.display_name,
            "comment_body": comment.body,
            "response_body": response,
            "plk_result": plk_result,
            "timestamp": datetime.utcnow()
        }
        self.collection.insert_one(doc)