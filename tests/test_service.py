"""
Tests related to the CloudflareImagesService
"""

from unittest.mock import patch
from django.test import TestCase, override_settings
from cloudflare_images.service import CloudflareImagesService, ApiException
from .utils import get_dummy_image, get_dummy_api_response


class CloudflareImageServiceTests(TestCase):
    """
    Test case for the CloudflareImagesService
    """

    def setUp(self):
        self.service = CloudflareImagesService()

    def test_has_config(self):
        config = self.service.config
        self.assertTrue(config is not None)

    @patch("requests.post")
    def test_failed_upload(self, mock_post):
        mock_post.return_value = get_dummy_api_response(400, '{"errors": "test"}')
        file = get_dummy_image()
        self.assertRaises(ApiException, self.service.upload, file)
        file.close()

    @patch("requests.post")
    def test_502_upload(self, mock_post):
        """
        This only ever happened once in production so far.
        Cloudflare returned a 502 with HTML content during an upload,
        breaking the service because it was always trying to parse some json.
        """
        mock_post.return_value = get_dummy_api_response(
            502, "<html>Failure</html>", False
        )
        file = get_dummy_image()
        self.assertRaises(ApiException, self.service.upload, file)
        file.close()

    @patch("requests.post")
    def test_success_upload(self, mock_post):
        mock_post.return_value = get_dummy_api_response(
            200, '{"result": {"id": "test"}}'
        )
        file = get_dummy_image()
        result_id = self.service.upload(file)
        self.assertEqual(result_id, "test")
        file.close()

    @patch("requests.get")
    def test_failed_open_default_variant(self, mock_get):
        mock_get.return_value = get_dummy_api_response(400, "", False)
        name = "image_id"
        self.assertRaises(ApiException, self.service.open, name)

    @patch("requests.get")
    def test_success_open_default_variant(self, mock_get):
        mock_get.return_value = get_dummy_api_response(200, "content", False)
        name = "image_id"
        result = self.service.open(name)
        self.assertEqual(result, "content")

    @patch("requests.delete")
    def test_failed_delete(self, mock_delete):
        mock_delete.return_value = get_dummy_api_response(400, "", False)
        name = "image_id"
        self.assertRaises(ApiException, self.service.delete, name)

    @patch("requests.delete")
    def test_success_delete(self, mock_delete):
        mock_delete.return_value = get_dummy_api_response(200, "", False)
        name = "image_id"
        self.service.delete(name)

    def test_get_url(self):
        name = "image_id"
        variant = "public"
        url = self.service.get_url(name, variant)
        hardcoded_url = "https://imagedelivery.net/account_hash/image_id/public"
        self.assertEqual(url, hardcoded_url)

    @override_settings(CLOUDFLARE_IMAGES_DOMAIN="example.com")
    def test_get_url_with_custom_domain(self):
        name = "image_id"
        variant = "public"
        url = self.service.get_url(name, variant)
        hardcoded_url = (
            "https://example.com/cdn-cgi/imagedelivery/account_hash/image_id/public"
        )
        self.assertEqual(url, hardcoded_url)

    @patch("requests.post")
    def test_failed_get_one_time_upload_url(self, mock_post):
        mock_post.return_value = get_dummy_api_response(400, "", False)
        self.assertRaises(ApiException, self.service.get_one_time_upload_url)

    @patch("requests.post")
    def test_success_get_one_time_upload_url(self, mock_post):
        mock_post.return_value = get_dummy_api_response(200, "{}")
        result = self.service.get_one_time_upload_url()
        self.assertEqual(result, {})
