from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = BASE_DIR / "prompts"

def load_prompt(filename: str) -> str:
    with open(PROMPT_DIR / filename, "r") as f:
        return f.read()