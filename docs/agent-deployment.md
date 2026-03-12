# Agent Deployment Guide

This document is written for an agent such as Claude Code, Codex, OpenClaw, or a similar coding agent.

## What this repo does

This repo provides a standalone Seedream 5.0 image-generation skill/CLI with these behaviors:
- text-to-image
- single-image image-to-image
- multi-image input
- sequential generation with `--max-images`
- local image files are automatically uploaded to the configured Qiniu image host first, then passed to Seedream as remote URLs

## Required agent behavior

Before installing anything, ask the user this question first:

> Do you want this installed globally or only for the current project?

Use this interpretation:
- **Global install**: install into the user's shared agent/skill location so other projects can reuse it
- **Local install**: keep it only inside the current project or current working setup

Do not assume global vs local. Ask first.

## Required secrets handling

`ARK_API_KEY` and the Qiniu configuration must be provided via **environment variables**.

Do **not**:
- hardcode keys in source files
- commit keys into the repository
- write secrets into markdown docs as real values
- store secrets in tracked config files unless the user explicitly asks and understands the risk

Preferred handling:
- temporary shell export for one session
- or user-approved shell profile configuration such as `~/.zshrc`
- or user-managed local secret storage already used in their environment

Minimum required environment variables:

```bash
export ARK_API_KEY="your-ark-api-key"
export QINIU_UPLOAD_URL="https://up-z1.qiniup.com"
export QINIU_CDN_DOMAIN="https://qncweb.ktvsky.com"
export QINIU_TOKEN_API="/c/qiniu/get_upload_token"
export QINIU_CHECK_API="/vadd/facechange/mv/qiniu/check"
export QINIU_BASE_URL="https://m.ktvsky.com"
export QINIU_DIRECTORY="seedream"
```

## Agent installation steps

1. Ask whether the user wants **global** or **local** install.
2. Clone this repository.
3. Install Python dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
4. Ask the user to provide or confirm the required environment variables.
5. Verify with a prompt-only smoke test:
   ```bash
   python3 scripts/generate_seedream.py "Jazz Festival poster" --no-generate
   ```
6. If local image input will be used, verify the Qiniu bridge is configured.
7. Then use the skill or run the CLI directly.

## Typical commands

```bash
python3 scripts/generate_seedream.py "Jazz Festival poster"
python3 scripts/generate_seedream.py "poster redesign" --image /tmp/local.png
python3 scripts/generate_seedream.py "multi reference" --image https://a.png --image /tmp/b.png --sequential --max-images 3
```

## What the agent should tell the user

The agent should make these points explicit:
- local image files are not sent directly to Seedream
- local image files are uploaded to the configured Qiniu image host first
- Seedream receives remote URLs only
- API keys and upload config should stay in environment variables

## Suggested message template for agents

```text
I can install this Seedream skill for you. First, do you want it installed globally or only for this project?

Also, I’ll need the runtime configuration via environment variables, especially ARK_API_KEY and the Qiniu upload settings. I won’t write real keys into the repo.
```
