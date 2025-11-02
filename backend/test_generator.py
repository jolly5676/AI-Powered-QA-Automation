from backend.ai_client import AIClient
from backend.app_utils.prompt_library import PromptLibrary

class TestGenerator:
    """Generates pytest test cases from function summaries."""

    def __init__(self, functions_summary: str, filename: str):
        self.functions_summary = functions_summary
        self.filename = filename
        self.ai = AIClient()

    def process(self):
        """Use centralized prompt to generate test scripts."""
        prompt = PromptLibrary.test_prompt(
            self.functions_summary, self.filename
        )
        return self.ai.generate_text(prompt)
