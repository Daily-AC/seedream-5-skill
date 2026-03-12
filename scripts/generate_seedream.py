#!/usr/bin/env python3
"""Standalone Seedream 5.0 CLI with local-file auto upload."""

import argparse
from urllib.parse import urlparse

try:
    from scripts.qiniu_uploader import QiniuUploader
    from scripts.seedream_client import DEFAULT_MODEL, generate_image
except ModuleNotFoundError:
    from qiniu_uploader import QiniuUploader
    from seedream_client import DEFAULT_MODEL, generate_image


def is_remote_url(value):
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def upload_local_images(paths):
    uploader = QiniuUploader()
    return [uploader.upload_image(path) for path in paths]


def normalize_image_input(image):
    if image is None:
        return None

    if isinstance(image, str):
        if is_remote_url(image):
            return image
        return upload_local_images([image])[0]

    normalized = []
    local_paths = []
    local_indexes = []
    for index, item in enumerate(image):
        if is_remote_url(item):
            normalized.append(item)
        else:
            normalized.append(None)
            local_paths.append(item)
            local_indexes.append(index)

    if local_paths:
        uploaded = upload_local_images(local_paths)
        for index, url in zip(local_indexes, uploaded):
            normalized[index] = url

    return normalized


def parse_args():
    parser = argparse.ArgumentParser(description="Generate images with Seedream 5.0")
    parser.add_argument("prompt")
    parser.add_argument("--image", action="append", help="Remote URL or local file path. Repeat for multiple images.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--output")
    parser.add_argument("--size", default="2K")
    parser.add_argument("--output-format", default="png")
    parser.add_argument("--watermark", action="store_true")
    parser.add_argument("--sequential", action="store_true")
    parser.add_argument("--max-images", type=int)
    parser.add_argument("--no-generate", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    normalized_image = None
    if args.image:
        normalized_image = normalize_image_input(args.image[0] if len(args.image) == 1 else args.image)

    if args.no_generate:
        print(args.prompt)
        if normalized_image is not None:
            print(normalized_image)
        return

    result = generate_image(
        args.prompt,
        output_path=args.output,
        model=args.model,
        input_image=normalized_image,
        size=args.size,
        output_format=args.output_format,
        watermark=args.watermark,
        sequential_image_generation=args.sequential,
        max_images=args.max_images,
    )
    print(result)


if __name__ == "__main__":
    main()
