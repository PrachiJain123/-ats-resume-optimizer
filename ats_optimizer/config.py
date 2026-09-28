"""Configuration settings and environment variable helpers for ATS Resume Optimizer.
"""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_MODEL = "gemini-3.1-pro"
TARGET_ATS_SCORE = 90.0  # Target threshold for ATS keyword match percentage


def load_env_file(env_path: Path | str | None = None) -> dict[str, str]:
    """Reads a local .env file and sets values in os.environ if not already set."""
    if env_path is None:
        env_path = Path.cwd() / ".env"
    else:
        env_path = Path(env_path)

    loaded = {}
    if not env_path.is_file():
        return loaded

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = val
                    loaded[key] = val
    except Exception:
        pass
    return loaded


def get_gemini_api_key(override_key: str | None = None) -> str | None:
    """Retrieves the Gemini API key from explicit override, environment, or .env file."""
    if override_key and override_key.strip():
        return override_key.strip()

    load_env_file()
    for var in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTIGRAVITY_API_KEY"):
        val = os.environ.get(var)
        if val and val.strip():
            return val.strip()

    return None


def save_gemini_api_key(api_key: str, env_path: Path | str | None = None) -> None:
    """Saves the API key to a local .env file."""
    if env_path is None:
        env_path = Path.cwd() / ".env"
    else:
        env_path = Path(env_path)

    key_clean = api_key.strip()
    os.environ["GEMINI_API_KEY"] = key_clean

    lines = []
    found = False
    if env_path.is_file():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                if line.strip().startswith("GEMINI_API_KEY="):
                    lines[i] = f"GEMINI_API_KEY={key_clean}\n"
                    found = True
                    break
        except Exception:
            lines = []

    if not found:
        lines.append(f"GEMINI_API_KEY={key_clean}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
