import os
import anthropic
import logging

class AnthropicClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        logging.info("✓ Anthropic client initialized.")

    def generate_response(self, text, plk_result, crisis_level):
        # TODO: Build a sophisticated prompt using PLK data and crisis level
        prompt = f"Based on the following text, provide an empathetic, consciousness-serving response.\n\nText: '{text}'"
        
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