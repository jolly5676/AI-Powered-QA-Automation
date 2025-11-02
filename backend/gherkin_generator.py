from backend.ai_client import AIClient
from backend.app_utils.prompt_library import PromptLibrary

class GherkinGenerator:
    """Generates Gherkin feature files and step definitions."""

    def __init__(self, code: str, requirement: str, filename: str):
        self.code = code
        self.requirement = requirement
        self.filename = filename
        self.ai = AIClient()

    def process(self):
        module_doc = "Extracted module documentation."
        functions_summary = "List of functions and logical flows."
        prompt = PromptLibrary.gherkin_prompt(
            module_doc, functions_summary, self.filename
        )
        return self.ai.generate_text(prompt)
