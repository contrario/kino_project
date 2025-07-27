
import os
import subprocess
import sys
from datetime import datetime

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print("[OUTPUT]:", result.stdout.strip())
    if result.stderr:
        print("[ERROR]:", result.stderr.strip())

def auto_add_commit_push():
    msg = input("🔧 Commit Message: ") or f"Auto-update {datetime.now()}"
    run_cmd("git add .")
    run_cmd(f'git commit -m "{msg}"')
    run_cmd("git push")

def create_branch():
    branch = input("🪴 New branch name: ")
    if branch:
        run_cmd(f"git checkout -b {branch}")
        run_cmd("git push --set-upstream origin " + branch)

def revert_last_commit():
    print("⚠️ Reverting last commit (soft reset)")
    run_cmd("git reset --soft HEAD~1")

def git_status_log():
    print("📌 Git Status:")
    run_cmd("git status")
    print("
🕰️ Git Log:")
    run_cmd("git log --oneline --graph --decorate --all")

def deploy_github_pages():
    folder = input("📁 Folder to deploy (e.g. 'build' or 'dist'): ") or "build"
    branch = input("🌿 Branch for Pages (default: gh-pages): ") or "gh-pages"
    run_cmd(f"git subtree push --prefix {folder} origin {branch}")

def main():
    while True:
        print("""
╔══════════════════════════════════════╗
║      GIT SWISS KNIFE - MENU          ║
╠══════════════════════════════════════╣
║ 1. Auto Add + Commit + Push          ║
║ 2. Create New Branch                 ║
║ 3. Revert Last Commit (Soft)         ║
║ 4. Show Git Status + Log             ║
║ 5. Deploy GitHub Pages               ║
║ 0. Exit                              ║
╚══════════════════════════════════════╝
""")
        choice = input("👉 Choose an option: ")
        if choice == "1":
            auto_add_commit_push()
        elif choice == "2":
            create_branch()
        elif choice == "3":
            revert_last_commit()
        elif choice == "4":
            git_status_log()
        elif choice == "5":
            deploy_github_pages()
        elif choice == "0":
            print("👋 Exiting Git Swiss Knife.")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
