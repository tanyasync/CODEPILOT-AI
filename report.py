import os
from datetime import datetime

SECTION_ORDER = [
    ("Planning Notes", "planning_notes"),
    ("Code Review", "review"),
    ("Bug Detection", "bugs"),
    ("Complexity Analysis", "complexity"),
    ("Security Audit", "security"),
    ("Optimization Suggestions", "optimization"),
    ("Documentation", "documentation"),
    ("Beginner-Friendly Explanation", "explanation"),
]


def build_report(state: dict) -> str:
    lines = []
    lines.append("# CodePilot AI — Code Review Report")
    lines.append("")
    lines.append(f"**File:** {state.get('filename', 'N/A')}")
    lines.append(f"**Detected Language:** {state.get('language', 'Unknown')}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for title, key in SECTION_ORDER:
        lines.append(f"## {title}")
        lines.append("")
        lines.append(state.get(key) or "_N/A_")
        lines.append("")

    return "\n".join(lines)


def save_report(content: str, filename: str, output_dir: str = "outputs/generated_reports") -> str:
    os.makedirs(output_dir, exist_ok=True)
    safe_name = filename.replace("/", "_").replace("\\", "_")
    path = os.path.join(output_dir, safe_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
