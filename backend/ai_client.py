import os
from openai import OpenAI
from dotenv import load_dotenv

class AIClient:
    """Handles all OpenAI model calls for the automation framework."""

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OpenAI API key missing in .env file.")
        self.client = OpenAI(api_key=api_key)

    def generate_text(self, prompt: str, model="gpt-4.1-mini"):
        """Unified response generator for text-based prompts."""
        response = self.client.responses.create(
            model=model,
            input=prompt
        )
        return response.output[0].content[0].text.strip()
