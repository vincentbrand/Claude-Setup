#!/usr/bin/env python3
"""
Claude Code Pre-Hook: NeuralDivergence
Evaluates incoming prompts and writes session context for post/stop hooks.
"""

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

NEURAL_DIR = Path(".claude") / "NeuroDivergence"

# Keywords/patterns that signal requirements
TEST_SIGNALS = [
    "function", "class", "method", "endpoint", "api", "component",
    "service", "handler", "controller", "model", "util", "helper",
    "refactor", "feature", "implement", "create", "build", "add",
]

GIT_SIGNALS = [
    "feature", "refactor", "fix", "bug", "breaking", "migrate",
    "update", "remove", "delete", "rename", "restructure", "overhaul",
    "rewrite", "redesign", "new page", "new component", "new endpoint",
]

DOC_SIGNALS = [
    "api", "endpoint", "config", "setup", "install", "deploy",
    "architecture", "schema", "migration", "breaking", "interface",
    "contract", "public", "export", "package", "library",
]


def evaluate_prompt(prompt: str) -> dict:
    """Analyze the prompt to determine what requirements apply."""
    lower = prompt.lower()

    require_tests = any(signal in lower for signal in TEST_SIGNALS)
    require_git = any(signal in lower for signal in GIT_SIGNALS)
    require_doc = any(signal in lower for signal in DOC_SIGNALS)

    return {
        "requireTests": require_tests,
        "requireGit": require_git,
        "requireDoc": require_doc,
    }


def main():
    # Read the prompt from stdin (Claude Code pipes it in)
    raw_input = sys.stdin.read().strip()

    if not raw_input:
        sys.exit(0)

    # Ensure directory exists
    NEURAL_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    session_id = str(uuid.uuid4())

    # Parse the incoming JSON from Claude Code
    try:
        prompt_data = json.loads(raw_input)
    except json.JSONDecodeError:
        prompt_data = {"prompt": raw_input}

    # The actual user prompt text for evaluation
    user_prompt = prompt_data.get("prompt", raw_input)
    requirements = evaluate_prompt(user_prompt)

    # Build the session context — spread prompt_data fields as proper JSON
    context = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "uuid": session_id,
        **prompt_data,
        "requireTests": requirements["requireTests"],
        "requireGit": requirements["requireGit"],
        "requireDoc": requirements["requireDoc"],
    }

    # Build path: NeuralDivergence / YYYY-MM-DD / session_id /
    cc_session_id = prompt_data.get("session_id", session_id)
    session_dir = NEURAL_DIR / now.strftime("%Y-%m-%d") / cc_session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    # Write file with timestamp as filename
    filename = now.strftime("%H%M%S") + ".json"
    filepath = session_dir / filename

    filepath.write_text(json.dumps(context, indent=2))

    # Also write a "latest.json" at the root for easy access by post/stop hooks
    latest = NEURAL_DIR / "latest.json"
    latest.write_text(json.dumps(context, indent=2))


if __name__ == "__main__":
    main()