# Seedream 5.0 Image Skill

Standalone Seedream 5.0 skill with automatic local-image upload through the company Qiniu image host.

## Install

```bash
python3 -m pip install -r requirements.txt
```

Set environment variables:

```bash
export ARK_API_KEY="your-ark-api-key"
export QINIU_UPLOAD_URL="https://up-z1.qiniup.com"
export QINIU_CDN_DOMAIN="https://qncweb.ktvsky.com"
export QINIU_TOKEN_API="/c/qiniu/get_upload_token"
export QINIU_CHECK_API="/vadd/facechange/mv/qiniu/check"
export QINIU_BASE_URL="https://m.ktvsky.com"
export QINIU_DIRECTORY="seedream"
```

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
