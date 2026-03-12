#!/usr/bin/env python3
"""Company Qiniu uploader for converting local image files to remote URLs."""

import time
from pathlib import Path

import requests

try:
    from scripts.config_loader import get
except ModuleNotFoundError:
    from config_loader import get


def build_key_name(directory, ts=None, suffix=".png"):
    timestamp = int(ts if ts is not None else time.time() * 1000)
    normalized_suffix = suffix if suffix.startswith(".") else f".{suffix}"
    return f"{directory}/{timestamp}{normalized_suffix}"


def _no_proxy_session():
    """Create a requests session that bypasses proxy for company domains."""
    session = requests.Session()
    session.trust_env = False  # ignore env proxy settings
    return session


class QiniuUploader:
    def __init__(self):
        self.upload_url = get("QINIU_UPLOAD_URL", "https://up-z1.qiniup.com")
        self.cdn_domain = get("QINIU_CDN_DOMAIN")
        self.token_api = get("QINIU_TOKEN_API")
        self.check_api = get("QINIU_CHECK_API")
        self.base_url = get("QINIU_BASE_URL")
        self.default_directory = get("QINIU_DIRECTORY", "seedream")
        self._session = _no_proxy_session()
        if not all([self.cdn_domain, self.token_api, self.base_url]):
            raise RuntimeError(
                "Missing Qiniu config. Place config.json in skill root or ~/.seedream-config.json. "
                "Required keys: QINIU_CDN_DOMAIN, QINIU_TOKEN_API, QINIU_BASE_URL"
            )

    def _get_json(self, path, params):
        response = self._session.get(f"{self.base_url}{path}", params=params, timeout=30)
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
        upload_urls = [self.upload_url] + [
            u for u in ["https://up.qiniup.com", "https://up-z2.qiniup.com"]
            if u != self.upload_url
        ]
        last_error = None
        for url in upload_urls:
            try:
                with open(file_path, "rb") as f:
                    response = self._session.post(
                        url,
                        files={"file": (Path(file_path).name, f, content_type)},
                        data={"key": key_name, "token": token},
                        timeout=300,
                    )
                response.raise_for_status()
                payload = response.json()
                key = payload.get("key")
                if not key:
                    raise RuntimeError("Qiniu upload response does not contain key")
                return f"{self.cdn_domain}/{key}"
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                last_error = e
                continue
        raise RuntimeError(f"All Qiniu upload endpoints failed: {last_error}")

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
