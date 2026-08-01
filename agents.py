"""
agents.py
---------
All 8 LLM-powered specialist agents from the CodePilot AI synopsis:
Planning, Code Review, Bug Detection, Complexity, Security, Optimizer,
Documentation, Explanation.

(Language detection is the 9th agent in the synopsis, but it is handled
deterministically in analyzers.py rather than via an LLM call — cheaper,
faster, and works for any language.)

Each agent is a thin function: load its prompt -> call Groq -> return text.
graph.py wires these together into the LangGraph workflow.
"""

import os
from llm import call_groq

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


def load_prompt(name: str) -> str:
    path = os.path.join(PROMPTS_DIR, f"{name}.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _build_user_message(code: str, language: str = None, extra_context: str = "") -> str:
    parts = []
    if language:
        parts.append(f"Detected language: {language}")
    if extra_context:
        parts.append(f"Additional context:\n{extra_context}")
    parts.append(f"Code:\n```\n{code}\n```")
    return "\n\n".join(parts)


def planning_agent(code: str, filename: str) -> str:
    prompt = load_prompt("planning")
    user_msg = f"Filename: {filename}\n\n{_build_user_message(code)}"
    return call_groq("planning", prompt, user_msg)


def review_agent(code: str, language: str, planning_notes: str = "") -> str:
    prompt = load_prompt("review")
    user_msg = _build_user_message(code, language, extra_context=planning_notes)
    return call_groq("review", prompt, user_msg)


def bug_detection_agent(code: str, language: str, planning_notes: str = "") -> str:
    prompt = load_prompt("bug_detection")
    user_msg = _build_user_message(code, language, extra_context=planning_notes)
    return call_groq("bug_detection", prompt, user_msg)


def complexity_agent(code: str, language: str) -> str:
    prompt = load_prompt("complexity")
    user_msg = _build_user_message(code, language)
    return call_groq("complexity", prompt, user_msg)


def security_agent(code: str, language: str, planning_notes: str = "") -> str:
    prompt = load_prompt("security")
    user_msg = _build_user_message(code, language, extra_context=planning_notes)
    return call_groq("security", prompt, user_msg)


def optimizer_agent(code: str, language: str) -> str:
    prompt = load_prompt("optimizer")
    user_msg = _build_user_message(code, language)
    return call_groq("optimizer", prompt, user_msg)


def documentation_agent(code: str, language: str) -> str:
    prompt = load_prompt("documentation")
    user_msg = _build_user_message(code, language)
    return call_groq("documentation", prompt, user_msg)


def explanation_agent(code: str, language: str) -> str:
    prompt = load_prompt("explanation")
    user_msg = _build_user_message(code, language)
    return call_groq("explanation", prompt, user_msg)
