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