# Seedream 5.0 Image Skill

> **Agent?** 如果你是 AI agent（Claude Code / Codex / OpenClaw 等），请直接阅读 [`docs/agent-deployment.md`](docs/agent-deployment.md) 进行部署，不要看下面的人类文档。

Standalone Seedream 5.0 image-generation skill.

It supports:
- text-to-image
- image-to-image with one or more reference images
- local image paths via automatic Qiniu upload
- sequential generation with `--max-images`

## Setup

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Copy `config.example.json` to `config.json` and fill in your values:

```bash
cp config.example.json config.json
```

Or place the config at `~/.seedream-config.json`.

## Quick examples

```bash
python3 scripts/generate_seedream.py "Jazz Festival poster"
python3 scripts/generate_seedream.py "poster redesign" --image https://example.com/a.png
python3 scripts/generate_seedream.py "poster redesign" --image /tmp/local.png
python3 scripts/generate_seedream.py "multi reference" --image https://a.png --image /tmp/b.png --sequential --max-images 3
```

If Seedream returns multiple images, outputs are saved as numbered files.

## For agents

See `docs/agent-deployment.md` for the install/use instructions intended for Claude Code, Codex, OpenClaw, and similar agents.
