"""
tests/test_agents.py
---------------------
Basic tests that DON'T require a Groq API key — they only test the
deterministic parts (language detection, AST checking, prompt loading).

Run with:  pytest tests/
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzers import detect_language, run_ast_check
from agents import load_prompt


def test_detect_language_python_by_extension():
    assert detect_language("sample.py", "print('hi')") == "Python"


def test_detect_language_java_by_extension():
    assert detect_language("Main.java", "class Main {}") == "Java"


def test_detect_language_unknown_extension_uses_heuristic():
    code = "def foo():\n    pass"
    assert detect_language("snippet.txt", code) == "Python"


def test_detect_language_truly_unknown():
    assert detect_language("data.xyz", "???") == "Unknown"


def test_ast_valid_python():
    result = run_ast_check("x = 1 + 2")
    assert result["valid_syntax"] is True
    assert result["node_count"] > 0


def test_ast_invalid_python():
    result = run_ast_check("def foo(:")
    assert result["valid_syntax"] is False
    assert "error" in result


def test_all_prompts_load():
    agent_names = [
        "planning", "review", "bug_detection", "complexity",
        "security", "optimizer", "documentation", "explanation",
    ]
    for name in agent_names:
        prompt_text = load_prompt(name)
        assert isinstance(prompt_text, str)
        assert len(prompt_text.strip()) > 0
