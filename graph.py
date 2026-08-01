from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents import (
    planning_agent,
    review_agent,
    bug_detection_agent,
    complexity_agent,
    security_agent,
    optimizer_agent,
    documentation_agent,
    explanation_agent,
)
from analyzers import analyze_code


class CodeState(TypedDict, total=False):
    filename: str
    code: str
    language: str
    static_analysis: dict
    planning_notes: str
    review: str
    bugs: str
    complexity: str
    security: str
    optimization: str
    documentation: str
    explanation: str


def node_intake(state: CodeState) -> CodeState:
    analysis = analyze_code(state["filename"], state["code"])
    state["language"] = analysis.get("language", "Unknown")
    state["static_analysis"] = analysis
    return state


def node_planning(state: CodeState) -> CodeState:
    state["planning_notes"] = planning_agent(state["code"], state["filename"])
    return state


def node_review(state: CodeState) -> CodeState:
    state["review"] = review_agent(state["code"], state["language"], state.get("planning_notes", ""))
    return state


def node_bugs(state: CodeState) -> CodeState:
    state["bugs"] = bug_detection_agent(state["code"], state["language"], state.get("planning_notes", ""))
    return state


def node_complexity(state: CodeState) -> CodeState:
    state["complexity"] = complexity_agent(state["code"], state["language"])
    return state


def node_security(state: CodeState) -> CodeState:
    state["security"] = security_agent(state["code"], state["language"], state.get("planning_notes", ""))
    return state


def node_optimizer(state: CodeState) -> CodeState:
    state["optimization"] = optimizer_agent(state["code"], state["language"])
    return state


def node_documentation(state: CodeState) -> CodeState:
    state["documentation"] = documentation_agent(state["code"], state["language"])
    return state


def node_explanation(state: CodeState) -> CodeState:
    state["explanation"] = explanation_agent(state["code"], state["language"])
    return state


def build_graph():
    graph = StateGraph(CodeState)

    graph.add_node("intake", node_intake)
    graph.add_node("planning", node_planning)
    graph.add_node("review", node_review)
    graph.add_node("bugs", node_bugs)
    graph.add_node("complexity", node_complexity)
    graph.add_node("security", node_security)
    graph.add_node("optimizer", node_optimizer)
    graph.add_node("documentation", node_documentation)
    graph.add_node("explanation", node_explanation)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "planning")
    graph.add_edge("planning", "review")
    graph.add_edge("review", "bugs")
    graph.add_edge("bugs", "complexity")
    graph.add_edge("complexity", "security")
    graph.add_edge("security", "optimizer")
    graph.add_edge("optimizer", "documentation")
    graph.add_edge("documentation", "explanation")
    graph.add_edge("explanation", END)

    return graph.compile()
