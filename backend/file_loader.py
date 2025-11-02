import os

class FileLoader:
    """Handles file loading and reading for the automation system."""

    @staticmethod
    def load_file(file_path: str) -> str:
        """Reads a file (Python, Markdown, etc.) and returns its contents."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ File not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def list_py_files(directory: str):
        """Returns a list of all .py files in a given directory."""
        return [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if file.endswith(".py")
        ]

    @staticmethod
    def list_md_files(directory: str):
        """Returns a list of all .md files in a given directory."""
        return [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if file.endswith(".md")
        ]
