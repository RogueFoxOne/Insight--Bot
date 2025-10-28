#!/usr/bin/env python3
"""
COMPLETE Insight-Bot Generator for Red Hat OpenShift
Generates ALL files for the Python/PRAW version of the bot.
Run: python3 generate_insight_bot.py
"""

import os
from pathlib import Path

# A dictionary to hold the content for each generated file
# This makes the script cleaner and easier to manage
FILE_CONTENT = {
    "insight_bot.py": """
import os
import argparse
import logging
from dotenv import load_dotenv
from insight_bot.core import InsightBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/insight_bot.log"),
        logging.StreamHandler()
    ]
)

def main():
    \"\"\"Main entry point for the bot.\"\"\"
    load_dotenv()
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    parser = argparse.ArgumentParser(description="Insight-Bot: A consciousness-serving Reddit companion.")
    parser.add_argument("--test", action="store_true", help="Run in test mode with a specific test subreddit.")
    parser.add_argument("--subreddit", type=str, help="Override the subreddit(s) to monitor.")
    args = parser.parse_args()

    logging.info("=====================================================")
    logging.info("INSIGHT BOT v1.0.0 - Starting...")
    logging.info("=====================================================")

    try:
        bot = InsightBot(is_test_mode=args.test, subreddit_override=args.subreddit)
        bot.run()
    except Exception as e:
        logging.critical(f"A critical error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
""",
    ".env.example": """
# Reddit API Credentials from https://www.reddit.com/prefs/apps
REDDIT_CLIENT_ID=YOUR_CLIENT_ID_HERE
REDDIT_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
REDDIT_USER_AGENT="InsightBot:v1.0.0 (by u/YOUR_USERNAME)"
REDDIT_USERNAME=YOUR_BOT_ACCOUNT_USERNAME
REDDIT_PASSWORD=YOUR_BOT_ACCOUNT_PASSWORD

# Anthropic Claude API from https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE

# MongoDB from https://cloud.mongodb.com/
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
DATABASE_NAME=insight_bot_db

# Bot Configuration
# Comma-separated list of subreddits, no spaces (e.g., GestaltView,YourTestSub)
SUBREDDITS=YourTestSubreddit
RESPONSE_DELAY=5 # Optional delay in seconds between replies

# Moderation
CRISIS_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE
""",
    "requirements.txt": """
praw==7.7.1
anthropic==0.25.0
pymongo==4.6.1
python-dotenv==1.0.1
nltk==3.8.1
textblob==0.17.1
spacy==3.7.2
# Don't forget to run: python -m spacy download en_core_web_sm
""",
    "requirements-dev.txt": """
pytest==7.4.3
black==23.12.1
flake8==7.0.0
mypy==1.8.0
""",
    "Dockerfile": """
# Stage 1: Build stage with dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN pip install --upgrade pip

# Install requirements
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# ---

# Stage 2: Final production stage
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY ./insight_bot ./insight_bot
COPY insight_bot.py .

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Set the entrypoint
CMD ["python", "insight_bot.py"]
""",
    "insight_bot/__init__.py": "# This file makes Python treat the `insight_bot` directory as a package.",
    "insight_bot/core.py": """
import os
import time
import logging
from .reddit_client import RedditClient
from .anthropic_client import AnthropicClient
from .mongodb_logger import MongoDBLogger
from .gestaltview_plk import GestaltViewPLK
from .crisis_detector import CrisisDetector

class InsightBot:
    def __init__(self, is_test_mode=False, subreddit_override=None):
        logging.info("Initializing InsightBot Core...")
        
        self.subreddits = self._get_subreddits(is_test_mode, subreddit_override)
        self.response_delay = int(os.getenv('RESPONSE_DELAY', 5))

        # Initialize clients
        self.reddit_client = RedditClient()
        self.anthropic_client = AnthropicClient()
        self.db_logger = MongoDBLogger()
        self.plk_analyzer = GestaltViewPLK()
        self.crisis_detector = CrisisDetector()
        
        logging.info(f"Monitoring subreddits: {', '.join(self.subreddits)}")
        logging.info("✓ Core modules loaded")

    def _get_subreddits(self, is_test, override):
        if is_test: return ['gestaltview_bot_dev']
        if override: return override.split(',')
        return os.getenv('SUBREDDITS', 'all').split(',')

    def run(self):
        logging.info("Starting bot monitoring...")
        subreddit_stream = self.reddit_client.stream_comments(self.subreddits)
        for comment in subreddit_stream:
            self._process_comment(comment)

    def _process_comment(self, comment):
        try:
            # Basic checks to avoid processing unnecessary comments
            if comment.author == self.reddit_client.username or comment.saved:
                return

            logging.info(f"New comment found in r/{comment.subreddit.display_name}: {comment.id}")
            
            # --- Main Logic Pipeline ---
            # 1. PLK Analysis
            plk_result = self.plk_analyzer.analyze(comment.body)
            
            # 2. Crisis Detection
            crisis_level = self.crisis_detector.detect(comment.body)

            # 3. Decision to respond
            if self._should_respond(plk_result, crisis_level):
                # 4. Generate AI response
                response_text = self.anthropic_client.generate_response(comment.body, plk_result, crisis_level)
                
                # 5. Post reply to Reddit
                self.reddit_client.reply_to_comment(comment, response_text)
                logging.info(f"Replied to comment {comment.id}")
                
                # 6. Log to database
                self.db_logger.log_interaction(comment, response_text, plk_result)

            # Mark as processed to avoid duplicates
            comment.save()
            time.sleep(self.response_delay)

        except Exception as e:
            logging.error(f"Error processing comment {comment.id}: {e}", exc_info=True)

    def _should_respond(self, plk_result, crisis_level):
        # TODO: Implement sophisticated logic based on PLK scores, crisis level, mentions, etc.
        # For now, let's respond if resonance is high.
        return plk_result.get('resonance_score', 0) > 75 or crisis_level == "High"
""",
    "insight_bot/reddit_client.py": """
import os
import praw
import logging

class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
        )
        self.username = self.reddit.user.me().name
        logging.info(f"✓ Reddit client initialized. Logged in as u/{self.username}")

    def stream_comments(self, subreddits):
        subreddit_string = "+".join(subreddits)
        return self.reddit.subreddit(subreddit_string).stream.comments(skip_existing=True)

    def reply_to_comment(self, comment, text):
        # TODO: Add footer text
        comment.reply(body=text)
""",
    "insight_bot/anthropic_client.py": """
import os
import anthropic
import logging

class AnthropicClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        logging.info("✓ Anthropic client initialized.")

    def generate_response(self, text, plk_result, crisis_level):
        # TODO: Build a sophisticated prompt using PLK data and crisis level
        prompt = f"Based on the following text, provide an empathetic, consciousness-serving response.\\n\\nText: '{text}'"
        
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            logging.error(f"Error contacting Anthropic API: {e}")
            return "I am currently unable to process this request. My apologies."
""",
    "insight_bot/mongodb_logger.py": """
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
""",
    "insight_bot/gestaltview_plk.py": """
import logging

class GestaltViewPLK:
    def __init__(self):
        logging.info("✓ PLK v5.0 Engine initialized.")
    
    def analyze(self, text):
        # TODO: Implement full PLK v5.0 analysis
        # This is a placeholder
        logging.info(f"Analyzing text with PLK: '{text[:50]}...'")
        return {
            "resonance_score": 80,
            "emotional_tone": "curious",
            "distress_level": 2
        }
""",
    "insight_bot/crisis_detector.py": """
import logging

class CrisisDetector:
    def __init__(self):
        # TODO: Load crisis keywords and patterns from a file
        self.patterns = ["help me", "i can't go on", "goodbye"]
        logging.info("✓ Crisis Detector initialized.")

    def detect(self, text):
        # TODO: Implement advanced context-aware crisis detection
        # This is a placeholder
        text_lower = text.lower()
        for pattern in self.patterns:
            if pattern in text_lower:
                logging.warning(f"High-risk crisis pattern detected: '{pattern}'")
                return "High"
        return "Low"
""",
    "tests/test_plk_engine.py": """
from insight_bot.gestaltview_plk import GestaltViewPLK

def test_plk_analysis():
    plk = GestaltViewPLK()
    result = plk.analyze("This is a test sentence.")
    assert "resonance_score" in result
    assert isinstance(result["resonance_score"], int)
""",
    ".gitignore": """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Project files
.idea/
.vscode/

# Logs
logs/
*.log

# Pytest
.pytest_cache/
"""
}

def create_file(path, content=""):
    """Helper function to create a file with content."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✓ Created {path}")

def main():
    """Main generator function."""
    project_name = 'insight-bot'
    base_path = Path(project_name)
    base_path.mkdir(exist_ok=True)
    
    print(f"🚀 Generating Insight-Bot project in ./{project_name}")
    
    # Create main directories
    dirs = [
        "insight_bot",
        "tests",
        "scripts",
        "docs",
        ".github/workflows"
    ]
    for d in dirs:
        (base_path / d).mkdir(parents=True, exist_ok=True)

    # Create all files from the FILE_CONTENT dictionary
    for rel_path, content in FILE_CONTENT.items():
        create_file(base_path / rel_path, content)
        
    print("\n✨ All done! Your Insight-Bot project is ready.")
    print(f"1. Navigate to the directory: cd {project_name}")
    print("2. Create a virtual environment: python3 -m venv venv && source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt && pip install -r requirements-dev.txt")
    print("4. Download NLP model: python -m spacy download en_core_web_sm")
    print("5. Configure your bot: cp .env.example .env && nano .env")
    print("6. Run the bot: python insight_bot.py")

if __name__ == "__main__":
    main()