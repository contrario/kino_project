# oracle_launcher.py
import os
import subprocess

def find_kino_oracle(root="."):
    for dirpath, _, filenames in os.walk(root):
        if "kino_oracle.py" in filenames:
            return os.path.join(dirpath, "kino_oracle.py")
    return None

def run_streamlit_app():
    oracle_path = find_kino_oracle()
    if oracle_path:
        print(f"✅ Found kino_oracle.py at: {oracle_path}")
        print("🚀 Launching with Streamlit...\n")
        subprocess.run(["streamlit", "run", oracle_path])
    else:
        print("❌ Error: 'kino_oracle.py' not found in the project directory.")
        print("💡 Tip: Make sure the file exists and is named correctly.")

if __name__ == "__main__":
    run_streamlit_app()
