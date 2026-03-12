# Seedream 5.0 Image Skill

Standalone Seedream 5.0 skill with automatic local-image upload through the company Qiniu image host.

## Install

```bash
python3 -m pip install -r requirements.txt
```

Set the required environment variable:

```bash
export ARK_API_KEY="your-ark-api-key"
```

Qiniu uses the company's built-in defaults. You only need to set Qiniu-related environment variables if your company values change and you want to override them.

## Examples

```bash
python3 scripts/generate_seedream.py "Jazz Festival poster"
python3 scripts/generate_seedream.py "poster redesign" --image https://example.com/a.png
python3 scripts/generate_seedream.py "poster redesign" --image /tmp/local.png
python3 scripts/generate_seedream.py "multi reference" --image https://a.png --image /tmp/b.png --sequential --max-images 3
```

## Features

- text-to-image
- single remote URL image-to-image
- multi-image URL input
- local file auto upload to Qiniu before Seedream request
- sequential generation options with multi-image outputs saved as numbered files when Seedream returns multiple images

## Publish

Designed to be published to the user's internal GitLab project via `glab` and can be made public for team usage.
