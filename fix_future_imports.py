import os

def fix_future_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    future_lines = [i for i, l in enumerate(lines) if 'from __future__ import' in l]

    if not future_lines:
        print(f"❌ No __future__ import found in {file_path}")
        return

    idx = future_lines[0]
    if idx != 0:
        # Μεταφέρουμε την γραμμή στην κορυφή
        future_line = lines.pop(idx)
        lines.insert(0, future_line)
        # Προσθέτουμε νέα γραμμή κάτω από αυτήν αν δεν υπάρχει ήδη
        if not lines[1].strip():
            lines.insert(1, '\n')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✅ Fixed: {file_path}")
    else:
        print(f"ℹ️ Already correct: {file_path}")

# Επιδιόρθωση συγκεκριμένου αρχείου του streamlit:
streamlit_logger = os.path.join(os.getcwd(), ".venv", "Lib", "site-packages", "streamlit", "logger.py")
fix_future_imports(streamlit_logger)
