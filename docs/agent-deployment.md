# Agent Deployment Guide

For Claude Code, Codex, OpenClaw, or similar coding agents.

## Required behavior

Before installing anything, ask:

> Do you want this installed globally or only for the current project?

Do not assume.

- **Global**: shared skill location for reuse across projects
- **Local**: only for the current repo or current setup

## What this repo provides

- text-to-image
- image-to-image
- multi-image input
- sequential generation with `--max-images`
- automatic upload of local image files to the company Qiniu host before calling Seedream

## Required secret handling

`ARK_API_KEY` must be provided via environment variable.

Use:

```bash
export ARK_API_KEY="your-ark-api-key"
```

Do not:
- hardcode real keys in source files
- commit real keys into the repo
- write real keys into docs

Qiniu company defaults are already built in. Do not ask the user to configure Qiniu unless they explicitly want to override those defaults.

## Install steps

1. Ask whether install should be global or local.
2. Clone this repo:
   - **Global (Claude Code)**: `git clone git@g.ktvsky.com:zhangyilin/seedream-5-skill.git ~/.claude/skills/seedream-5-image`
   - **Local**: `git clone git@g.ktvsky.com:zhangyilin/seedream-5-skill.git ./seedream-5-image`
3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
4. Ask the user to provide or confirm `ARK_API_KEY`.
5. Run a smoke test:
   ```bash
   python3 scripts/generate_seedream.py "Jazz Festival poster" --no-generate
   ```

## Important user-facing notes

Tell the user:
- local image files are uploaded to Qiniu first
- Seedream receives remote URLs only
- `ARK_API_KEY` should stay in an environment variable
- Qiniu defaults are already built in

## Typical commands

```bash
python3 scripts/generate_seedream.py "Jazz Festival poster"
python3 scripts/generate_seedream.py "poster redesign" --image /tmp/local.png
python3 scripts/generate_seedream.py "multi reference" --image https://a.png --image /tmp/b.png --sequential --max-images 3
```
