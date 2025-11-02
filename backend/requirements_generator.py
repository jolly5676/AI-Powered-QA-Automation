from backend.ai_client import AIClient
from backend.app_utils.prompt_library import PromptLibrary

class RequirementsGenerator:
    """Generates functional requirements specification from Python code."""

    def __init__(self, py_code: str, filename: str):
        self.py_code = py_code
        self.filename = filename
        self.ai = AIClient()

    def process(self):
        """Use centralized prompt to generate requirements."""
        module_doc = "Extracted module documentation from code."
        functions_summary = "Summary of functions extracted from code."
        constants = []

        prompt = PromptLibrary.requirements_prompt(
            module_doc, functions_summary, constants, self.filename
        )

        return self.ai.generate_text(prompt)
