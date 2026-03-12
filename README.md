# Seedream 5.0 Image Skill

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

Set the required API key:

```bash
export ARK_API_KEY="your-ark-api-key"
```

Notes:
- `ARK_API_KEY` is the only required user config
- company Qiniu defaults are already built in
- local image files are uploaded to Qiniu first, then sent to Seedream as remote URLs

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
