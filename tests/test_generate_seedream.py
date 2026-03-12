import sys
import unittest
from unittest.mock import patch

from scripts.generate_seedream import normalize_image_input, main


class GenerateSeedreamTests(unittest.TestCase):
    def test_normalize_image_input_keeps_remote_url(self):
        result = normalize_image_input("https://example.com/a.png")
        self.assertEqual(result, "https://example.com/a.png")

    @patch("scripts.generate_seedream.upload_local_images")
    def test_normalize_image_input_uploads_local_file(self, mock_upload):
        mock_upload.return_value = ["https://qncweb.ktvsky.com/seedream/local.png"]
        result = normalize_image_input("/tmp/local.png")
        self.assertEqual(result, "https://qncweb.ktvsky.com/seedream/local.png")

    @patch("scripts.generate_seedream.upload_local_images")
    def test_normalize_image_input_uploads_local_list(self, mock_upload):
        mock_upload.return_value = ["https://cdn/a.png", "https://cdn/b.png"]
        result = normalize_image_input(["/tmp/a.png", "/tmp/b.png"])
        self.assertEqual(result, ["https://cdn/a.png", "https://cdn/b.png"])

    @patch("scripts.generate_seedream.generate_image")
    def test_cli_passes_text_to_image_args(self, mock_generate):
        mock_generate.return_value = "outputs/out.png"
        with patch.object(sys, "argv", ["generate_seedream.py", "Jazz Festival poster"]):
            main()
        mock_generate.assert_called_once()
        self.assertEqual(mock_generate.call_args.kwargs["input_image"], None)

    @patch("scripts.generate_seedream.generate_image")
    def test_cli_passes_single_image_url(self, mock_generate):
        mock_generate.return_value = "outputs/out.png"
        with patch.object(sys, "argv", ["generate_seedream.py", "poster redesign", "--image", "https://example.com/a.png"]):
            main()
        self.assertEqual(mock_generate.call_args.kwargs["input_image"], "https://example.com/a.png")

    @patch("scripts.generate_seedream.generate_image")
    def test_cli_passes_multi_image_list(self, mock_generate):
        mock_generate.return_value = "outputs/out.png"
        with patch.object(sys, "argv", ["generate_seedream.py", "multi reference", "--image", "https://example.com/a.png", "--image", "https://example.com/b.png"]):
            main()
        self.assertEqual(mock_generate.call_args.kwargs["input_image"], ["https://example.com/a.png", "https://example.com/b.png"])

    @patch("scripts.generate_seedream.generate_image")
    def test_cli_passes_sequential_options(self, mock_generate):
        mock_generate.return_value = "outputs/out.png"
        with patch.object(sys, "argv", ["generate_seedream.py", "multi reference", "--sequential", "--max-images", "3"]):
            main()
        self.assertTrue(mock_generate.call_args.kwargs["sequential_image_generation"])
        self.assertEqual(mock_generate.call_args.kwargs["max_images"], 3)
