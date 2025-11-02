# backend/story_generator.py

import os
from openai import OpenAI
from backend.code_parser import PythonCodeParser
from backend.app_utils.prompt_manager import PromptManager
from dotenv import load_dotenv

load_dotenv()

class StoryGenerator:
    """Generate user stories from code using GPT."""
    
    def __init__(self, code_text: str, filename: str):
        self.code_text = code_text
        self.filename = filename
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("❌ OpenAI API key is missing. Please set it in your .env file.")

        self.client = OpenAI(api_key=self.api_key)
        self.parser = PythonCodeParser(code_text, filename)

        # Load prompt
        self.prompt_manager = PromptManager("backend/app_utils/prompts.json")
        self.story_prompt = self.prompt_manager.get_prompt("story_prompt")

    def process(self):
        parsed = self.parser.process()
        module_doc = parsed.get("module_doc", "No module description available.")
        functions = parsed.get("functions", [])

        formatted_functions = "\n".join([f"- {f['name']}: {f['doc'] or 'No docstring'}" for f in functions])

        prompt = self.story_prompt.format(
            module_doc=module_doc,
            functions_summary=formatted_functions,
            filename=self.filename
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional business analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()
