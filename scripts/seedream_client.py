#!/usr/bin/env python3
"""Seedream 5.0 client helpers."""

import base64
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    from scripts.config_loader import require
except ModuleNotFoundError:
    from config_loader import require

API_BASE = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_SIZE = "2K"
DEFAULT_OUTPUT_FORMAT = "png"


def get_api_key():
    return require("ARK_API_KEY")


def _is_remote_url(value):
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _validate_image_input(image):
    if isinstance(image, str):
        if not _is_remote_url(image):
            raise ValueError("Seedream only supports remote image URL input after normalization.")
        return

    if isinstance(image, list):
        if not image:
            raise ValueError("Image URL list cannot be empty.")
        for item in image:
            if not isinstance(item, str) or not _is_remote_url(item):
                raise ValueError("Seedream only supports remote image URL input after normalization.")
        return

    raise ValueError("Image input must be a remote image URL or list of URLs.")


def build_payload(
    prompt,
    model=DEFAULT_MODEL,
    image=None,
    size=DEFAULT_SIZE,
    output_format=DEFAULT_OUTPUT_FORMAT,
    watermark=False,
    sequential_image_generation=None,
    max_images=None,
):
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "response_format": "b64_json",
        "output_format": output_format,
        "watermark": watermark,
    }

    if image is not None:
        _validate_image_input(image)
        payload["image"] = image

    if sequential_image_generation is not None:
        payload["sequential_image_generation"] = sequential_image_generation

    if max_images is not None:
        payload["sequential_image_generation_options"] = {"max_images": max_images}

    return payload


def _write_image_item(item, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    b64_data = item.get("b64_json")
    if b64_data:
        image_data = base64.b64decode(b64_data)
        output.write_bytes(image_data)
        return str(output)

    image_url = item.get("url")
    if image_url:
        import requests

        response = requests.get(image_url, timeout=120)
        response.raise_for_status()
        output.write_bytes(response.content)
        return str(output)

    raise ValueError("Seedream response item does not contain supported image data.")


def save_image_from_response(response_data, output_path):
    data = response_data.get("data") or []
    if not data:
        raise ValueError("Seedream response does not contain image data.")

    output = Path(output_path)
    suffix = output.suffix or ".png"

    if len(data) == 1:
        return _write_image_item(data[0], output)

    saved_paths = []
    for index, item in enumerate(data, start=1):
        indexed_output = output.with_name(f"{output.stem}-{index}{suffix}")
        saved_paths.append(_write_image_item(item, indexed_output))
    return saved_paths


def generate_image(
    prompt,
    output_path=None,
    model=DEFAULT_MODEL,
    input_image=None,
    size=DEFAULT_SIZE,
    output_format=DEFAULT_OUTPUT_FORMAT,
    watermark=False,
    sequential_image_generation=None,
    max_images=None,
):
    import requests

    payload = build_payload(
        prompt,
        model=model,
        image=input_image,
        size=size,
        output_format=output_format,
        watermark=watermark,
        sequential_image_generation=sequential_image_generation,
        max_images=max_images,
    )

    if not output_path:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        output_path = f"outputs/seedream-{timestamp}.{output_format}"

    response = requests.post(
        API_BASE,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_api_key()}",
        },
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return save_image_from_response(response.json(), output_path)
