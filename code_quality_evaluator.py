import os
import json
import ast
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

def evaluate_code_quality(file_path):
    quality = {
        "filename": str(file_path),
        "line_count": 0,
        "function_count": 0,
        "class_count": 0,
        "has_docstrings": False,
        "has_type_annotations": False,
        "syntax_ok": True,
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
            quality["line_count"] = len(source.splitlines())

            tree = ast.parse(source)
            quality["function_count"] = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            quality["class_count"] = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            quality["has_docstrings"] = any(isinstance(node, (ast.FunctionDef, ast.ClassDef)) and ast.get_docstring(node) for node in ast.walk(tree))
            quality["has_type_annotations"] = any(hasattr(node, 'returns') and node.returns is not None for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
    except Exception as e:
        quality["syntax_ok"] = False
        quality["error"] = str(e)

    return quality

def scan_project(directory):
    results = []
    for path in Path(directory).rglob("*.py"):
        if path.name == "code_quality_evaluator.py":
            continue
        results.append(evaluate_code_quality(path))
    return results

if __name__ == "__main__":
    results = scan_project(PROJECT_ROOT)
    output_path = LOG_DIR / "code_quality_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"✅ Quality report saved to {output_path}")
