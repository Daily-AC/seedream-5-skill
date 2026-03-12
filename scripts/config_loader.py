#!/usr/bin/env python3
"""Load config from config.json, falling back to environment variables."""

import json
import os
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATHS = [
    _SKILL_ROOT / "config.json",
    Path.home() / ".seedream-config.json",
]

_cache = None


def _load():
    global _cache
    if _cache is not None:
        return _cache

    for path in _CONFIG_PATHS:
        if path.is_file():
            with open(path) as f:
                _cache = json.load(f)
            return _cache

    _cache = {}
    return _cache


def get(key, default=None):
    """Get config value: config.json > env var > default."""
    cfg = _load()
    value = cfg.get(key)
    if value:
        return value
    value = os.getenv(key)
    if value:
        return value
    return default


def require(key):
    """Get config value or raise with a helpful message."""
    value = get(key)
    if not value:
        raise RuntimeError(
            f"Missing required config '{key}'. "
            f"Set it in config.json (place in skill root or ~/.seedream-config.json) "
            f"or as an environment variable."
        )
    return value
