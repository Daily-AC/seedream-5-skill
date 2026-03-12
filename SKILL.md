---
name: seedream-5-image
description: Use when generating images with Seedream 5.0, including text-to-image, image-to-image, multi-image inputs, or local image files that need automatic URL upload first.
---

# Seedream 5.0 Image Skill

This skill can:
- generate images from text prompts
- accept one or more image inputs
- save numbered output files when Seedream returns multiple generated images
- auto-upload local image files through the configured Qiniu bridge
- call Seedream 5.0 directly with Ark auth

## Usage

```bash
python3 scripts/generate_seedream.py "Jazz Festival poster"
python3 scripts/generate_seedream.py "poster redesign" --image https://example.com/a.png
python3 scripts/generate_seedream.py "poster redesign" --image /tmp/local.png
python3 scripts/generate_seedream.py "multi reference" --image https://a.png --image /tmp/b.png --sequential --max-images 3
```

## Requirements

- `config.json` in skill root or `~/.seedream-config.json` (contains ARK_API_KEY and Qiniu settings)
