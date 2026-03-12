import os
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.seedream_client import build_payload, get_api_key, save_image_from_response


class BuildPayloadTests(unittest.TestCase):
    def test_build_payload_for_text_to_image_uses_defaults(self):
        payload = build_payload("poster prompt")

        self.assertEqual(payload["model"], "doubao-seedream-5-0-260128")
        self.assertEqual(payload["prompt"], "poster prompt")
        self.assertEqual(payload["size"], "2K")
        self.assertEqual(payload["output_format"], "png")
        self.assertFalse(payload["watermark"])
        self.assertNotIn("image", payload)

    def test_build_payload_accepts_remote_url_list(self):
        payload = build_payload("poster prompt", image=["https://a.png", "https://b.png"])
        self.assertEqual(payload["image"], ["https://a.png", "https://b.png"])

    def test_build_payload_adds_sequential_options(self):
        payload = build_payload("poster prompt", sequential_image_generation="auto", max_images=3)
        self.assertEqual(payload["sequential_image_generation"], "auto")
        self.assertEqual(payload["sequential_image_generation_options"], {"max_images": 3})


class ValidationTests(unittest.TestCase):
    def tearDown(self):
        for path in [
            Path("outputs/test-seedream.png"),
            Path("outputs/test-seedream-1.png"),
            Path("outputs/test-seedream-2.png"),
        ]:
            if path.exists():
                path.unlink()

    def test_get_api_key_raises_when_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "ARK_API_KEY"):
                get_api_key()

    def test_build_payload_rejects_local_image_path(self):
        with self.assertRaisesRegex(ValueError, "remote image URL"):
            build_payload("poster prompt", image="poster.png")

    def test_save_image_from_response_writes_png_from_b64(self):
        response_data = {
            "data": [{"b64_json": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+yhZ0AAAAASUVORK5CYII="}]
        }

        output_path = save_image_from_response(response_data, "outputs/test-seedream.png")

        self.assertTrue(Path(output_path).exists())

    @patch("requests.get")
    def test_save_image_from_response_downloads_png_from_url(self, mock_get):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.content = b"png-bytes"
        response_data = {
            "data": [{"url": "https://example.com/test.png"}]
        }

        output_path = save_image_from_response(response_data, "outputs/test-seedream.png")

        self.assertTrue(Path(output_path).exists())
        self.assertEqual(Path(output_path).read_bytes(), b"png-bytes")

    @patch("requests.get")
    def test_save_image_from_response_saves_multiple_images(self, mock_get):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.content = b"png-bytes"
        response_data = {
            "data": [
                {"url": "https://example.com/test-1.png"},
                {"url": "https://example.com/test-2.png"},
            ]
        }

        output_paths = save_image_from_response(response_data, "outputs/test-seedream.png")

        self.assertEqual(output_paths, [
            "outputs/test-seedream-1.png",
            "outputs/test-seedream-2.png",
        ])
        self.assertTrue(Path(output_paths[0]).exists())
        self.assertTrue(Path(output_paths[1]).exists())
