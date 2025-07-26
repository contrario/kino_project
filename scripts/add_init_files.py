import os

def ensure_init_files(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        if "__pycache__" in dirpath:
            continue  # αγνόησε cache φακέλους
        if "__init__.py" not in filenames:
            init_path = os.path.join(dirpath, "__init__.py")
            with open(init_path, encoding="utf-8", "w") as f:
                pass
            print(f"✅ Προστέθηκε: {init_path}")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ensure_init_files(project_root)
    print("🎯 Έλεγχος και προσθήκη ολοκληρώθηκαν.")