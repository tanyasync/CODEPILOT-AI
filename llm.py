import os
from groq import Groq
from dotenv import load_dotenv
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=_env_path)

_api_key = os.getenv("GROQ_API_KEY")

if not _api_key:
    print(f"[CodePilot AI] WARNING: No GROQ_API_KEY found. Looked for .env at: {_env_path}")
    print("[CodePilot AI] Make sure a file literally named '.env' (not '.env.txt') "
          "sits in the same folder as this file, with a line: GROQ_API_KEY=your_key_here")
    
client = Groq(api_key=_api_key) if _api_key else None

MODEL_HEAVY = "openai/gpt-oss-120b"
MODEL_LIGHT = "openai/gpt-oss-20b"

HEAVY_AGENTS = {"bug_detection", "security", "complexity", "optimizer"}
LIGHT_AGENTS = {"planning", "review", "documentation", "explanation"}


def get_model_for_agent(agent_name: str) -> str:
    """Return which Groq model a given agent should use."""
    if agent_name in HEAVY_AGENTS:
        return MODEL_HEAVY
    return MODEL_LIGHT


def call_groq(
    agent_name: str,
    system_prompt: str,
    user_content: str,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> str:
    if client is None:
        raise RuntimeError(
            "GROQ_API_KEY not found. Copy .env.example to .env and add your Groq API key."
        )

    model = get_model_for_agent(agent_name)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        reasoning_effort="low",
    )

    content = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    if not content:
        # Surface WHY it was empty instead of silently returning "" to the UI.
        content = (
            f"_[{agent_name} agent returned an empty response from `{model}` "
            f"(finish_reason: {finish_reason}). This usually means max_tokens was "
            f"too low for the model's reasoning step, or the request was rate-limited. "
            f"Try again, or increase max_tokens in llm.py.]_"
        )
        print(f"[CodePilot AI] WARNING: empty content from {agent_name} "
              f"(model={model}, finish_reason={finish_reason})")

    return content
