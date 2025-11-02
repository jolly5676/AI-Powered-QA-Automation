import json
import os
from textwrap import dedent

PROMPT_STORE = "outputs/prompt_store.json"

class PromptLibrary:
    """Central dynamic prompt loader for GPT interactions."""

    @staticmethod
    def _load_dynamic_prompt(name: str):
        """Load updated prompt text from prompt_store.json if present."""
        if os.path.exists(PROMPT_STORE):
            try:
                with open(PROMPT_STORE, "r", encoding="utf-8") as f:
                    prompts = json.load(f)
                if name in prompts:
                    return prompts[name]
            except Exception:
                pass
        return None  # fallback to static version

    # ===========================================================
    # 📘 REQUIREMENTS PROMPT
    # ===========================================================
    @staticmethod
    def requirements_prompt(module_doc: str, functions_summary: str, constants: list, filename: str) -> str:
        dynamic = PromptLibrary._load_dynamic_prompt("requirements_prompt")
        if dynamic:
            return dynamic

        return dedent(f"""
        You are an expert Business Analyst specializing in system documentation.

        Generate a **Functional Requirements Specification** document from the given Python module.

        Module: {filename}
        Description: {module_doc}
        Functions Summary: {functions_summary}
        Constants: {constants}

        Format as:
        1. Overview
        2. Functional Requirements
        3. Non-Functional Requirements
        4. Traceability
        5. Future Enhancements
        """)

    # ===========================================================
    # 🧩 GHERKIN PROMPT
    # ===========================================================
    @staticmethod
    def gherkin_prompt(module_doc: str, functions_summary: str, filename: str) -> str:
        dynamic = PromptLibrary._load_dynamic_prompt("gherkin_prompt")
        if dynamic:
            return dynamic

        return dedent(f"""
        You are a BDD Automation Expert skilled in Gherkin syntax.

        Using the given Python module info, generate:
        1. A Gherkin `.feature` file
        2. Python Behave step definitions

        Module: {filename}
        Description: {module_doc}
        Functions Summary: {functions_summary}
        """)

    # ===========================================================
    # 🧠 CODE UPDATER PROMPT
    # ===========================================================
    @staticmethod
    def code_updater_prompt(requirements_text: str, old_code: str, filename: str) -> str:
        dynamic = PromptLibrary._load_dynamic_prompt("code_updater_prompt")
        if dynamic:
            return dynamic

        return dedent(f"""
        You are a Senior Python Engineer.

        Update `{filename}` based on these requirements:
        {requirements_text}

        Maintain existing functionality and follow PEP8 standards.
        """)

    # ===========================================================
    # 📖 STORY PROMPT
    # ===========================================================
    @staticmethod
    def story_prompt(module_doc: str, functions_summary: str, filename: str) -> str:
        dynamic = PromptLibrary._load_dynamic_prompt("story_prompt")
        if dynamic:
            return dynamic

        return dedent(f"""
        You are a Product Owner generating JIRA-style stories for `{filename}`.

        Create:
        - Title
        - Description
        - Acceptance Criteria
        - Business Value
        - Story Points
        """)

    # ===========================================================
    # ⚙️ TEST PROMPT
    # ===========================================================
    @staticmethod
    def test_prompt(functions_summary: str, filename: str) -> str:
        dynamic = PromptLibrary._load_dynamic_prompt("test_prompt")
        if dynamic:
            return dynamic

        return dedent(f"""
        You are a QA Automation Engineer.

        Generate pytest unit tests for:
        {functions_summary}

        Include edge cases and proper naming conventions.
        """)
