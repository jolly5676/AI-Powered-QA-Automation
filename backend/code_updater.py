from backend.ai_client import AIClient
from backend.app_utils.prompt_library import PromptLibrary

class CodeUpdater:
    """Updates Python source code based on new requirements."""

    def __init__(self, requirements_text: str, old_code: str, filename: str):
        self.requirements_text = requirements_text
        self.old_code = old_code
        self.filename = filename
        self.ai = AIClient()

    def process(self):
        """Use centralized prompt to request GPT-driven code updates."""
        prompt = PromptLibrary.code_updater_prompt(
            self.requirements_text, self.old_code, self.filename
        )
        return self.ai.generate_text(prompt)
