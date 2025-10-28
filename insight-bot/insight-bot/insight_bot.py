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
    """Main entry point for the bot."""
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