import os

class FileSaver:
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_all(self, filename, req_text, gherkin_text):
        base = os.path.splitext(filename)[0]
        req_path = os.path.join(self.output_dir, f"{base}_requirements.md")
        gherkin_path = os.path.join(self.output_dir, f"{base}.feature")

        with open(req_path, "w", encoding="utf-8") as r:
            r.write(req_text)
        with open(gherkin_path, "w", encoding="utf-8") as g:
            g.write(gherkin_text)
