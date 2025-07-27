
import streamlit as st
import subprocess

st.set_page_config(page_title="Git Swiss Knife", layout="centered")

st.title("🛠️ Git Swiss Knife Web UI")
st.markdown("Πραγματοποίησε εύκολα git εντολές από εδώ.")

repo_path = st.text_input("📁 Repo Directory (π.χ. /home/youruser/mysite):", ".")

def run_git_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=repo_path, check=True)
        st.success("✅ Επιτυχία!")
        st.code(result.stdout)
    except subprocess.CalledProcessError as e:
        st.error("❌ Σφάλμα:")
        st.code(e.stderr)

if st.button("📦 git add ."):
    run_git_command(["git", "add", "."])

commit_msg = st.text_input("✏️ Commit Message")
if st.button("✅ git commit"):
    if commit_msg.strip():
        run_git_command(["git", "commit", "-m", commit_msg])
    else:
        st.warning("Παρακαλώ γράψε ένα μήνυμα.")

if st.button("🚀 git push"):
    run_git_command(["git", "push"])

if st.button("📥 git pull"):
    run_git_command(["git", "pull"])

if st.button("🔍 git status"):
    run_git_command(["git", "status"])
