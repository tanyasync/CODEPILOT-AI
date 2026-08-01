# CodePilot AI

A Multi-Agent Intelligent Code Review and Explanation Platform.

Built with **LangGraph**, **LangChain**, **Streamlit**, and the **Groq API**
(`openai/gpt-oss-120b` + `openai/gpt-oss-20b`).

## What it does

Upload or paste code in **any programming language**, and CodePilot AI runs it through
a pipeline of specialist agents:

`Intake (language detection + static analysis) → Planning → Code Review → Bug Detection
→ Complexity Analysis → Security Audit → Optimizer → Documentation → Explanation → Report`

## Project Structure

```
codepilot-ai/
├── app.py            # Streamlit dashboard (entry point)
├── agents.py         # 8 LLM-powered specialist agents
├── graph.py           # LangGraph workflow (DAG of agents)
├── llm.py             # Groq client + model router (120b vs 20b)
├── analyzers.py        # Non-LLM static checks: language detect, AST, Radon, Bandit
├── report.py           # Aggregates agent outputs into a Markdown report
├── prompts/             # System prompt for each agent
├── tests/                # Unit tests (no API key required)
└── outputs/generated_reports/  # Saved reports land here
```

## Setup

1. **Clone / open the project folder**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Groq API key**
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and paste your key from https://console.groq.com/keys:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```
   It will open at `http://localhost:8501`

## Running tests

```bash
pip install pytest
pytest tests/
```
(Tests only cover the deterministic parts — language detection, AST checks,
and prompt loading — so they run without needing a Groq API key.)

## Notes

- Radon and Bandit checks currently run only for Python files (module 6 in the synopsis);
  other languages skip straight to the LLM agents.
- All LLM calls go through `llm.py` → Groq only. No other model provider is used.
- Reports are saved as Markdown in `outputs/generated_reports/` and are also downloadable
  from the Streamlit UI.
