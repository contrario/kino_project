
import os
import subprocess
from datetime import datetime

def run_cmd(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Σφάλμα:", e.stderr)

def git_add_commit_push():
    print("\n--- Git Auto Commit & Push ---")
    run_cmd("git status")
    run_cmd("git add .")
    commit_msg = input("Μήνυμα Commit (κενό = timestamp): ").strip()
    if not commit_msg:
        commit_msg = f"Auto commit @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run_cmd(f'git commit -m "{commit_msg}"')
    run_cmd("git push")

def git_menu():
    while True:
        print("\n[ Git Swiss Knife Menu ]")
        print("1. Auto Commit & Push")
        print("2. Δημιουργία νέου branch")
        print("3. Επιστροφή (revert) τελευταίου commit")
        print("4. Έξοδος")
        choice = input("Επιλογή: ").strip()
        if choice == "1":
            git_add_commit_push()
        elif choice == "2":
            name = input("Όνομα branch: ").strip()
            run_cmd(f"git checkout -b {name}")
        elif choice == "3":
            confirm = input("Είσαι σίγουρος; (yes/no): ").strip().lower()
            if confirm == "yes":
                run_cmd("git reset --soft HEAD~1")
        elif choice == "4":
            break
        else:
            print("Μη έγκυρη επιλογή.")

if __name__ == "__main__":
    git_menu()
