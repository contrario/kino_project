# code_quality_evaluator.py

import os
import json
from pathlib import Path
from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor

# === Paths ===
ROOT_PATH = Path(__file__).resolve().parent.parent.parent
SCAN_PATH = ROOT_PATH  # ✅ Διορθώθηκε εδώ για να σαρώσει όλο το project
OUTPUT_PATH = ROOT_PATH / "kino_project" / "logs" / "code_quality_report.json"

EXCLUDE_DIRS = {'venv', '__pycache__', '.git', 'logs'}

def get_python_files(path):
    py_files = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(".py"):
                py_files.append(Path(root) / file)
    return py_files

def analyze_code_quality(files):
    results = []
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                code = f.read()
                blocks = cc_visit(code)
                for block in blocks:
                    results.append({
                        "file": str(file_path.relative_to(ROOT_PATH)),
                        "name": block.name,
                        "complexity": block.complexity,
                        "lineno": block.lineno
                    })
            except Exception as e:
                results.append({
                    "file": str(file_path.relative_to(ROOT_PATH)),
                    "error": str(e)
                })
    return results

def save_report(data):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✔️ Report saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    py_files = get_python_files(SCAN_PATH)
    print(f"📁 Analyzing {len(py_files)} Python files...")
    report = analyze_code_quality(py_files)
    save_report(report)
    print("✅ Code Quality Evaluation Complete")
