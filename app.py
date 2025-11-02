import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
import time

# -------------------------------
# 📦 BACKEND IMPORTS
# -------------------------------
from backend.requirements_generator import RequirementsGenerator
from backend.story_generator import StoryGenerator
from backend.gherkin_generator import GherkinGenerator
from backend.code_updater import CodeUpdater
from backend.file_loader import FileLoader
from backend.orchestrator_multi import OrchestratorMulti
from backend.app_utils.prompt_manager import PromptManager

# -------------------------------
# ⚙️ INITIAL SETUP
# -------------------------------
load_dotenv()

st.set_page_config(
    page_title="AI-Powered QA Automation",
    layout="wide",
    page_icon="🤖"
)

st.title("🤖 AI-Powered QA Automation Suite")
st.caption("Smartly generate requirements, features, stories, and updated code with OpenAI-powered analysis.")

# -------------------------------
# 📂 DIRECTORY SETUP
# -------------------------------
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("generated_outputs")
PROMPT_FILE = Path("backend/app_utils/prompts.json")

for folder in [INPUT_DIR, OUTPUT_DIR, OUTPUT_DIR / "requirements", OUTPUT_DIR / "gherkin", OUTPUT_DIR / "updated_code"]:
    folder.mkdir(parents=True, exist_ok=True)

# -------------------------------
# 🧠 LOAD PROMPTS
# -------------------------------
pm = PromptManager()
prompts = pm.load_prompts() 

# -------------------------------
# 🧭 DEFINE TABS
# -------------------------------
tabs = st.tabs([
    "📄 Requirements",
    "📘 Story",
    "🧩 Gherkin / Feature",
    "🔁 Code Updater",
    "🚀 Run Automation",
    "🧠 Prompt Manager"
])

# ============================================================
# 📄 TAB 1: REQUIREMENTS GENERATOR
# ============================================================
with tabs[0]:
    st.header("📄 Generate Requirements Document")

    uploaded_file = st.file_uploader("Upload a Python (.py) file", type=["py"])
    if uploaded_file:
        py_code = uploaded_file.read().decode("utf-8")
        st.success("✅ File uploaded successfully!")

        if st.button("🧾 Generate Requirements"):
            generator = RequirementsGenerator(py_code, uploaded_file.name)
            requirements_text = generator.process()
            st.text_area("📘 Generated Requirements", requirements_text, height=400)

            save_path = OUTPUT_DIR / "requirements" / f"{uploaded_file.name.replace('.py', '_requirements.md')}"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(requirements_text)
            st.success(f"💾 Saved to {save_path}")

# ============================================================
# 📘 TAB 2: STORY GENERATOR
# ============================================================
with tabs[1]:
    st.header("📘 Generate User Stories")

    uploaded_file = st.file_uploader("Upload a Python (.py) file", type=["py"], key="story_upload")

    if uploaded_file:
        py_code = uploaded_file.read().decode("utf-8")

        st.success("✅ File uploaded successfully!")

        if st.button("📖 Generate Story"):
            story_gen = StoryGenerator(py_code, uploaded_file.name)  # ✅ Pass filename also
            story_output = story_gen.process()
            st.text_area("🧾 Generated User Story", story_output, height=400)

            # Save output
            save_path = OUTPUT_DIR / f"{uploaded_file.name.replace('.py', '_story.md')}"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(story_output)

            st.success(f"💾 Saved to {save_path}")


# ============================================================
# 🧩 TAB 3: GHERKIN / FEATURE GENERATOR
# ============================================================
with tabs[2]:
    st.header("🧩 Generate Gherkin / Feature File")

    code_file = st.file_uploader("Upload Python (.py) file", type=["py"], key="gherkin_code")
    requirement_file = st.file_uploader("Upload Requirements (.md) file", type=["md"], key="gherkin_req")

    if code_file and requirement_file:
        code_text = code_file.read().decode("utf-8")
        req_text = requirement_file.read().decode("utf-8")
        st.success("✅ Both files uploaded successfully!")

        if st.button("🧩 Generate Feature File"):
            gherkin_gen = GherkinGenerator(code_text, req_text, code_file.name)
            gherkin_output = gherkin_gen.process()
            st.text_area("📄 Generated Gherkin Feature", gherkin_output, height=400)

            save_path = OUTPUT_DIR / "gherkin" / f"{code_file.name.replace('.py', '.feature')}"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(gherkin_output)
            st.success(f"💾 Saved to {save_path}")

# ============================================================
# 🔁 TAB 4: CODE UPDATER
# ============================================================
with tabs[3]:
    st.header("🔁 Update Python Code Based on Requirements")

    uploaded_code = st.file_uploader("Upload existing Python (.py) file", type=["py"], key="code_updater_py")
    uploaded_req = st.file_uploader("Upload updated Requirements (.md) file", type=["md"], key="code_updater_req")

    if uploaded_code and uploaded_req:
        py_code = uploaded_code.read().decode("utf-8")
        req_text = uploaded_req.read().decode("utf-8")

        st.success("✅ Files ready for update!")

        if st.button("🔧 Update Code"):
            updater = CodeUpdater(py_code, req_text, uploaded_code.name)
            updated_code = updater.process()
            st.text_area("🧠 Updated Python Code", updated_code, height=400)

            save_path = OUTPUT_DIR / "updated_code" / uploaded_code.name
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(updated_code)
            st.success(f"💾 Updated file saved to {save_path}")

# ============================================================
# 🚀 TAB 5: RUN AUTOMATION (MULTI-FILE)
# ============================================================
with tabs[4]:
    st.header("🚀 Automated Multi-File Processing Dashboard")

    st.write(f"📂 Scanning directory: `{INPUT_DIR}`")
    py_files = FileLoader.list_py_files(str(INPUT_DIR))

    if not py_files:
        st.warning("⚠️ No Python files found in the input folder.")
    else:
        st.success(f"✅ Found {len(py_files)} Python files for processing.")
        for file in py_files:
            st.markdown(f"- `{file}`")

        st.markdown("---")
        if st.button("🚀 Run Full Automation", use_container_width=True, type="primary"):
            st.info("⚙️ Starting background processing for all files...")
            progress = st.progress(0)
            status_placeholder = st.empty()
            results = []
            total_files = len(py_files)

            for i, file_path in enumerate(py_files):
                filename = Path(file_path).name
                status_placeholder.markdown(f"🧩 **Processing:** `{filename}`")
                time.sleep(0.3)
                try:
                    orchestrator = OrchestratorMulti([file_path])
                    result = orchestrator.process_all()
                    results.append((filename, "🟢 Success", result))
                except Exception as e:
                    results.append((filename, f"🔴 Failed ({e})", None))
                progress.progress((i + 1) / total_files)

            status_placeholder.empty()
            st.success("✅ Automation completed for all files!")

            st.markdown("---")
            st.subheader("📊 Processing Summary")
            for filename, status, result in results:
                with st.expander(f"{status} — {filename}"):
                    if result:
                        st.code(result, language="markdown")
                    else:
                        st.warning("No result data available for this file.")
            st.info(f"📁 Outputs saved in `{OUTPUT_DIR}` directory.")

# ============================================================
# 🧠 TAB 6: PROMPT MANAGER
# ============================================================
with tabs[5]:
    st.header("🧠 Manage GPT Prompt Templates")

    try:
        prompts = pm.load_prompts()
    except Exception as e:
        st.error(f"❌ Error loading prompts: {e}")
        prompts = {}

    st.info("💡 Modify prompt templates below and click **Save Prompts** to update them.")

    updated_prompts = {}
    for key, value in prompts.items():
        updated_prompts[key] = st.text_area(
            label=f"🧩 {key.replace('_', ' ').title()}",
            value=value,
            height=250,
            placeholder=f"Enter or edit {key.replace('_', ' ')} prompt..."
        )

    if st.button("💾 Save Prompts", use_container_width=True, type="primary"):
        try:
            pm.save_prompts(updated_prompts)
            st.success("✅ Prompts saved successfully!")
        except Exception as e:
            st.error(f"⚠️ Failed to save prompts: {e}")
