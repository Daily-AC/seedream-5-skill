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
- automatic upload of local image files via Qiniu before calling Seedream

## Configuration

This skill requires a `config.json` file. The user should have received it separately.

**Ask the user:**

> 请提供 config.json 配置文件（你应该已经从同事那里收到了）。

Then place the file at one of these locations (in priority order):
1. Skill root directory: `<skill-dir>/config.json`
2. Home directory: `~/.seedream-config.json`

The config file contains API keys and Qiniu settings. See `config.example.json` for the required fields.

**Do not:**
- hardcode real keys in source files
- commit config.json into the repo
- write real keys into docs
- ask the user to manually fill in Qiniu fields — they should already be in the config file

**If the user doesn't have the config file**, tell them to ask the person who shared this skill for it.

## Install steps

1. Ask whether install should be global or local.
2. Clone this repo:
   - **Global (Claude Code)**: `git clone https://github.com/Daily-AC/seedream-5-skill.git ~/.claude/skills/seedream-5-image`
   - **Local**: `git clone https://github.com/Daily-AC/seedream-5-skill.git ./seedream-5-image`
3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
4. Ask the user for `config.json` and place it in the skill root directory.
5. Run a smoke test:
   ```bash
   python3 scripts/generate_seedream.py "Jazz Festival poster" --no-generate
   ```

## Important user-facing notes

Tell the user:
- local image files are uploaded to Qiniu first
- Seedream receives remote URLs only
- all config is in config.json, no manual env var setup needed

## Typical commands

```bash
python3 scripts/generate_seedream.py "Jazz Festival poster"
python3 scripts/generate_seedream.py "poster redesign" --image /tmp/local.png
python3 scripts/generate_seedream.py "multi reference" --image https://a.png --image /tmp/b.png --sequential --max-images 3
```
