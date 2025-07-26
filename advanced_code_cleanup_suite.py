import os
import shutil

def scan_and_fix_future_imports(root_path):
    print("[✔] Scanning for misplaced '__future__' imports...")
    for subdir, _, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(subdir, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    future_lines = [i for i, line in enumerate(lines) if 'from __future__' in line]
                    if future_lines and future_lines[0] > 5:  # only fix if not at top
                        print(f"  [!] Fixing {path}")
                        shutil.copy2(path, path + ".bak")

                        # move __future__ imports to top
                        future_imports = [lines[i] for i in future_lines]
                        lines = [l for i, l in enumerate(lines) if i not in future_lines]
                        lines = future_imports + lines

                        with open(path, "w", encoding="utf-8") as f:
                            f.writelines(lines)

                except Exception as e:
                    print(f"  [x] Error reading {path}: {e}")

def fix_webbrowser_encoding_bug(root_path):
    print("[✔] Scanning for webbrowser encoding bug...")
    for subdir, _, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(subdir, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    changed = False
                    new_lines = []
                    for line in lines:
                        if "webbrowser.open" in line and "encoding=" in line:
                            print(f"  [!] Fix in {path}")
                            changed = True
                            new_lines.append("# AUTO-FIXED: Removed invalid encoding parameter\n")
                            new_lines.append("webbrowser.open(url)\n")
                        else:
                            new_lines.append(line)

                    if changed:
                        shutil.copy2(path, path + ".bak")
                        with open(path, "w", encoding="utf-8") as f:
                            f.writelines(new_lines)

                except Exception as e:
                    print(f"  [x] Error fixing {path}: {e}")


if __name__ == "__main__":
    VENV_PATH = "./.venv"  # προσαρμόστε αν έχει άλλο όνομα ο φάκελος
    scan_and_fix_future_imports(VENV_PATH)
    fix_webbrowser_encoding_bug(VENV_PATH)
    print("\n✅ Advanced Code Cleanup Suite completed.\nRestart your IDE and rerun your app.")
