#!/usr/bin/env python3
"""Company Qiniu uploader for converting local image files to remote URLs."""

import os
import time
from pathlib import Path

import requests


def build_key_name(directory, ts=None, suffix=".png"):
    timestamp = int(ts if ts is not None else time.time() * 1000)
    normalized_suffix = suffix if suffix.startswith(".") else f".{suffix}"
    return f"{directory}/{timestamp}{normalized_suffix}"


class QiniuUploader:
    def __init__(self):
        self.upload_url = os.getenv("QINIU_UPLOAD_URL")
        self.cdn_domain = os.getenv("QINIU_CDN_DOMAIN")
        self.token_api = os.getenv("QINIU_TOKEN_API")
        self.check_api = os.getenv("QINIU_CHECK_API")
        self.base_url = os.getenv("QINIU_BASE_URL", "")
        self.default_directory = os.getenv("QINIU_DIRECTORY", "seedream")

        missing = [
            name
            for name, value in {
                "QINIU_UPLOAD_URL": self.upload_url,
                "QINIU_CDN_DOMAIN": self.cdn_domain,
                "QINIU_TOKEN_API": self.token_api,
                "QINIU_CHECK_API": self.check_api,
            }.items()
            if not value
        ]
        if missing:
            raise RuntimeError(f"QINIU environment variables are required: {', '.join(missing)}")

    def _get_json(self, path, params):
        response = requests.get(f"{self.base_url}{path}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_token(self, key_name):
        data = self._get_json(self.token_api, {"filename": key_name})
        if data.get("errcode") != 200 or not data.get("token"):
            raise RuntimeError(data.get("errmsg") or "Failed to get Qiniu upload token")
        return data["token"]

    def upload_file(self, file_path, token, key_name):
        suffix = Path(file_path).suffix.lower() or ".png"
        content_type = "image/png" if suffix == ".png" else "application/octet-stream"
        with open(file_path, "rb") as f:
            response = requests.post(
                self.upload_url,
                files={"file": (Path(file_path).name, f, content_type)},
                data={"key": key_name, "token": token},
                timeout=120,
            )
        response.raise_for_status()
        payload = response.json()
        key = payload.get("key")
        if not key:
            raise RuntimeError("Qiniu upload response does not contain key")
        return f"{self.cdn_domain}/{key}"

    def check_image(self, file_url):
        data = self._get_json(self.check_api, {"k": file_url, "is_record": 0})
        if data.get("errcode") != 200:
            raise RuntimeError(data.get("errmsg") or "Qiniu image check failed")
        return data

    def upload_image(self, file_path, directory=None):
        suffix = Path(file_path).suffix.lower() or ".png"
        key_name = build_key_name(directory or self.default_directory, suffix=suffix)
        token = self.get_token(key_name)
        file_url = self.upload_file(file_path, token, key_name)
        self.check_image(file_url)
        return file_url
