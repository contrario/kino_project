
import os

def patch_streamlit_webbrowser_import():
    import_path = os.path.join(
        ".venv", "Lib", "site-packages", "streamlit", "cli_util.py"
    )
    if not os.path.exists(import_path):
        print("❌ Δεν βρέθηκε το cli_util.py στο virtual environment.")
        return

    with open(import_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any("import webbrowser" in line for line in lines):
        print("✅ Το 'import webbrowser' υπάρχει ήδη.")
        return

    # Backup
    with open(import_path + ".bak", "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Βρες την πρώτη import και βάλε το webbrowser πριν
    for i, line in enumerate(lines):
        if line.strip().startswith("import") or line.strip().startswith("from"):
            lines.insert(i, "import webbrowser\n")
            break

    with open(import_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("🛠️ Προστέθηκε το 'import webbrowser' στο cli_util.py επιτυχώς.")

if __name__ == "__main__":
    patch_streamlit_webbrowser_import()
