"""
patch_streamlit.py

📌 Industrial-grade patching tool for fixing Streamlit's encoding bug in cli_util.py
Author: KINO Prediction Ecosystem
"""

import os
from pathlib import Path

def find_cli_util_file():
    base_dir = Path(__file__).resolve().parent
    venv_root = base_dir / ".venv" / "Lib" / "site-packages" / "streamlit"
    target_file = venv_root / "cli_util.py"
    if not target_file.exists():
        print("❌ streamlit/cli_util.py not found. Please check your virtual environment path.")
        return None
    return target_file

def patch_file(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")
        if 'open(os.devnull, encoding="utf-8", "w")' in content:
            new_content = content.replace(
                'open(os.devnull, encoding="utf-8", "w")',
                'open(os.devnull, "w", encoding="utf-8")'
            )
            file_path.write_text(new_content, encoding="utf-8")
            print(f"✅ Patched successfully: {file_path}")
        else:
            print("ℹ️ Patch already applied or pattern not found.")
    except Exception as e:
        print(f"❌ Error patching file: {e}")

if __name__ == "__main__":
    cli_util = find_cli_util_file()
    if cli_util:
        patch_file(cli_util)
