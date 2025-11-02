import json
import os

class PromptManager:
    def __init__(self, prompt_file="backend/app_utils/prompts.json"):
        self.prompt_file = prompt_file
        self.prompts = {}

    def load_prompts(self):
        """Load prompts from JSON file, or create defaults if missing."""
        if os.path.exists(self.prompt_file):
            try:
                with open(self.prompt_file, "r", encoding="utf-8") as f:
                    self.prompts = json.load(f)
                print(f"✅ Prompts loaded from {self.prompt_file}")
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON in {self.prompt_file}. Regenerating...")
                self.generate_default_prompts()
        else:
            print(f"⚠️ Prompt file not found. Creating new: {self.prompt_file}")
            self.generate_default_prompts()

        return self.prompts  # <-- This prevents 'NoneType' errors

    def generate_default_prompts(self):
        """Create a default prompt structure."""
        self.prompts = {
            "requirements_prompt": "Generate a requirements document from given Python code.",
            "gherkin_prompt": "Generate Gherkin feature file based on given code and requirements.",
            "story_prompt": "Create user stories from module functionality.",
            "code_update_prompt": "Update Python code based on new requirements."
        }
        self.save_prompts()

    def save_prompts(self):
        """Save prompts to file."""
        with open(self.prompt_file, "w", encoding="utf-8") as f:
            json.dump(self.prompts, f, indent=4)
        print(f"💾 Prompts saved to {self.prompt_file}")

    def get_prompt(self, key):
        """Retrieve a prompt using its key."""
        return self.prompts.get(key, f"⚠️ Prompt '{key}' not found.")
