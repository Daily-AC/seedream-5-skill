# Agent Deployment Guide

For Claude Code, Codex, OpenClaw, and similar agents:

1. Clone this repo.
2. Install Python dependencies.
3. Set `ARK_API_KEY`.
4. Set the Qiniu environment variables.
5. Invoke the `seedream-5-image` skill or run `python3 scripts/generate_seedream.py` directly.

## Typical commands

```bash
python3 scripts/generate_seedream.py "Jazz Festival poster"
python3 scripts/generate_seedream.py "poster redesign" --image /tmp/local.png
python3 scripts/generate_seedream.py "multi reference" --image https://a.png --image /tmp/b.png --sequential --max-images 3
```

## Notes

- Local image files are uploaded through the company Qiniu image host first.
- Seedream ultimately receives only remote image URLs.
- The repo can be hosted on internal GitLab and opened as public if desired.
