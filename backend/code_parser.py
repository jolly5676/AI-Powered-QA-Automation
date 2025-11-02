# backend/code_parser.py

import ast

class PythonCodeParser:
    """Extracts module docstring, functions, and their docstrings from a Python file."""

    def __init__(self, code_text: str, filename: str):
        self.code_text = code_text
        self.filename = filename

    def process(self):
        """Parse the code and return module summary as dictionary."""
        try:
            tree = ast.parse(self.code_text)
        except Exception as e:
            return {"module_doc": f"⚠️ Failed to parse code: {e}", "functions": []}

        module_doc = ast.get_docstring(tree) or "No module description available."

        functions = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "doc": ast.get_docstring(node) or "No description.",
                    "args": [arg.arg for arg in node.args.args],
                })

        return {"module_doc": module_doc, "functions": functions}
