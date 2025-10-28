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