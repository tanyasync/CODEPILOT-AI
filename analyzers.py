"""
analyzers.py
------------
Non-LLM, deterministic checks. These run BEFORE the LLM agents so that:
1. Language detection works for ANY file extension (not a fixed list).
2. Python files get real static-analysis data (AST validity, cyclomatic
   complexity via Radon, security findings via Bandit) that can be handed
   to the LLM agents as extra grounding context.
"""

import ast
import json
import os
import subprocess
import tempfile

# Extend this map any time — it's just a hint, not a hard limit.
LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".m": "Objective-C",
    ".scala": "Scala",
    ".sh": "Shell",
}


def detect_language(filename: str, code: str) -> str:
    """Detect language from file extension first, falling back to simple
    keyword heuristics so unlabeled snippets (pasted code) still resolve
    to something useful instead of failing on unknown extensions."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in LANGUAGE_EXTENSIONS:
        return LANGUAGE_EXTENSIONS[ext]

    heuristics = [
        ("public static void main", "Java"),
        ("#include <iostream>", "C++"),
        ("#include <stdio.h>", "C"),
        ("func main()", "Go"),
        ("fn main()", "Rust"),
        ("def ", "Python"),
        ("function ", "JavaScript"),
        ("=>", "JavaScript"),
        ("<?php", "PHP"),
    ]
    for needle, lang in heuristics:
        if needle in code:
            return lang

    return "Unknown"


def run_ast_check(code: str) -> dict:
    """Only meaningful for Python — confirms the source at least parses."""
    try:
        tree = ast.parse(code)
        return {"valid_syntax": True, "node_count": len(list(ast.walk(tree)))}
    except SyntaxError as e:
        return {"valid_syntax": False, "error": str(e)}


def run_radon(filepath: str) -> dict:
    """Cyclomatic complexity via Radon (Python only)."""
    try:
        result = subprocess.run(
            ["radon", "cc", filepath, "-j"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return json.loads(result.stdout) if result.stdout else {}
    except FileNotFoundError:
        return {"error": "radon not installed"}
    except Exception as e:
        return {"error": str(e)}


def run_bandit(filepath: str) -> dict:
    """Security static analysis via Bandit (Python only)."""
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", "-q", filepath],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return json.loads(result.stdout) if result.stdout else {}
    except FileNotFoundError:
        return {"error": "bandit not installed"}
    except Exception as e:
        return {"error": str(e)}


def analyze_code(filename: str, code: str) -> dict:
    """Entry point used by graph.py. Runs whichever static tools apply."""
    language = detect_language(filename, code)
    result = {"language": language}

    if language == "Python":
        result["ast"] = run_ast_check(code)

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as f:
                f.write(code)
                tmp_path = f.name
            result["radon"] = run_radon(tmp_path)
            result["bandit"] = run_bandit(tmp_path)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    return result
