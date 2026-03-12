import os
import unittest
from unittest.mock import patch

from scripts.qiniu_uploader import QiniuUploader, build_key_name


class QiniuUploaderTests(unittest.TestCase):
    def test_build_key_name_uses_directory_prefix(self):
        key = build_key_name("seedream", 1700000000)
        self.assertEqual(key, "seedream/1700000000.png")

    def test_build_key_name_keeps_suffix(self):
        key = build_key_name("seedream", 1700000000, ".jpg")
        self.assertEqual(key, "seedream/1700000000.jpg")

    @patch.dict(os.environ, {
        "QINIU_UPLOAD_URL": "https://up-z1.qiniup.com",
        "QINIU_CDN_DOMAIN": "https://qncweb.ktvsky.com",
        "QINIU_TOKEN_API": "/c/qiniu/get_upload_token",
        "QINIU_CHECK_API": "/vadd/facechange/mv/qiniu/check",
        "QINIU_BASE_URL": "https://m.ktvsky.com",
        "QINIU_DIRECTORY": "seedream",
    }, clear=True)
    @patch("builtins.open", create=True)
    @patch("requests.post")
    @patch("requests.get")
    @patch("scripts.qiniu_uploader.build_key_name")
    def test_upload_image_runs_token_upload_check_flow(self, mock_build_key, mock_get, mock_post, mock_open):
        mock_build_key.return_value = "seedream/1700000000.png"
        mock_get.side_effect = [
            type("Resp", (), {"raise_for_status": lambda self: None, "json": lambda self: {"errcode": 200, "token": "upload-token"}})(),
            type("Resp", (), {"raise_for_status": lambda self: None, "json": lambda self: {"errcode": 200}})(),
        ]
        mock_post.return_value.raise_for_status.return_value = None
        mock_post.return_value.json.return_value = {"key": "seedream/1700000000.png"}
        mock_open.return_value.__enter__.return_value = object()

        uploader = QiniuUploader()
        result = uploader.upload_image("/tmp/input.png", directory="seedream")

        self.assertEqual(result, "https://qncweb.ktvsky.com/seedream/1700000000.png")

    @patch.dict(os.environ, {}, clear=True)
    def test_uses_company_defaults_when_env_missing(self):
        uploader = QiniuUploader()
        self.assertEqual(uploader.upload_url, "https://up-z1.qiniup.com")
        self.assertEqual(uploader.cdn_domain, "https://qncweb.ktvsky.com")
        self.assertEqual(uploader.token_api, "/c/qiniu/get_upload_token")
        self.assertEqual(uploader.check_api, "/vadd/facechange/mv/qiniu/check")
        self.assertEqual(uploader.base_url, "https://m.ktvsky.com")
