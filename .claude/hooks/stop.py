#!/usr/bin/env python3
"""Test stop hook — uses TTS to announce task completion with a summary."""

import json
import subprocess
import sys


def speak(text: str):
    """Cross-platform text to speech."""
    if sys.platform == "darwin":
        subprocess.run(["say", text])
    elif sys.platform == "linux":
        subprocess.run(["espeak", text])
    elif sys.platform == "win32":
        subprocess.run(
            ["powershell", "-Command", f'Add-Type -AssemblyName System.Speech; '
             f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")']
        )


def get_stop_message() -> str:
    """Read the stop hook input from stdin and extract a summary."""
    try:
        hook_input = json.loads(sys.stdin.read())
        # Try common fields for the assistant's last output
        for key in ("message", "content", "text", "summary", "output"):
            val = hook_input.get(key, "")
            if isinstance(val, str) and val.strip():
                return val.strip()
        # Fallback: dump the whole input so Claude can summarize it
        return json.dumps(hook_input)[:2000]
    except (json.JSONDecodeError, EOFError):
        return ""


def summarize(message: str) -> str:
    """Use Claude to generate a short spoken summary of what was done."""
    try:
        result = subprocess.run(
            [
                "claude",
                "--print",
                "-m",
                f"In 10 words or less, summarize what was accomplished in this task. "
                f"Start with 'Done.' then the summary. No quotes, no markdown. "
                f"Example: 'Done. The login page is now implemented.'\n\n"
                f"Task output:\n{message[:2000]}",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    return "Done. Task completed."


if __name__ == "__main__":
    message = get_stop_message()
    summary = summarize(message) if message else "Done. Task completed."
    speak(summary)