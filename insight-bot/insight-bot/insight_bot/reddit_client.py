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