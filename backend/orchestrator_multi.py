import os
from pathlib import Path
from backend.requirements_generator import RequirementsGenerator
from backend.gherkin_generator import GherkinGenerator
from backend.code_updater import CodeUpdater


class OrchestratorMulti:
    """Handles automation workflow for multiple Python files."""

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.output_dir = Path("generated_outputs")
        self.requirements_dir = self.output_dir / "requirements"
        self.gherkin_dir = self.output_dir / "gherkin"
        self.updated_dir = self.output_dir / "updated_code"

        # Ensure folders exist
        for folder in [self.output_dir, self.requirements_dir, self.gherkin_dir, self.updated_dir]:
            folder.mkdir(parents=True, exist_ok=True)

    def process_all(self):
        """Process all input Python files end-to-end."""
        results = []

        for file_path in self.file_paths:
            filename = Path(file_path).name

            try:
                # 1️⃣ Load Python code
                with open(file_path, "r", encoding="utf-8") as f:
                    code_text = f.read()

                # 2️⃣ Generate Requirements
                req_gen = RequirementsGenerator(code_text, filename)
                requirements_output = req_gen.process()

                req_path = self.requirements_dir / f"{filename.replace('.py', '_requirements.md')}"
                with open(req_path, "w", encoding="utf-8") as f:
                    f.write(requirements_output)

                # 3️⃣ Generate Gherkin (using code + requirements)
                gherkin_gen = GherkinGenerator(code_text, requirements_output, filename)
                gherkin_output = gherkin_gen.process()

                gherkin_path = self.gherkin_dir / f"{filename.replace('.py', '.feature')}"
                with open(gherkin_path, "w", encoding="utf-8") as f:
                    f.write(gherkin_output)

                # 4️⃣ Generate Updated Code (simulating new requirement addition)
                updater = CodeUpdater(code_text, requirements_output, filename)
                updated_code = updater.process()

                updated_path = self.updated_dir / filename
                with open(updated_path, "w", encoding="utf-8") as f:
                    f.write(updated_code)

                # 5️⃣ Summary for display
                summary = f"""
                ✅ **{filename} processed successfully**
                - 📘 Requirements → `{req_path}`
                - 🧩 Gherkin → `{gherkin_path}`
                - 🔁 Updated Code → `{updated_path}`
                """

                results.append(summary)

            except Exception as e:
                results.append(f"❌ Error processing {filename}: {e}")

        return "\n\n".join(results)
