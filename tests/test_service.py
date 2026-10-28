"""
Tests related to the CloudflareImagesService
"""

from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from cloudflare_images.service import ApiException, CloudflareImagesService

from .utils import get_dummy_api_response, get_dummy_image


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
        try:
            self.service.upload(file)
            self.fail("ApiException should have been raised")
        except ApiException as e:
            self.assertEqual(e.status_code, 400)
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
        try:
            self.service.upload(file)
            self.fail("ApiException should have been raised")
        except ApiException as e:
            self.assertEqual(e.status_code, 502)
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
        try:
            self.service.open(name)
            self.fail("ApiException should have been raised")
        except ApiException as e:
            self.assertEqual(e.status_code, 400)

    @patch("requests.get")
    def test_success_open_default_variant(self, mock_get):
        mock_get.return_value = get_dummy_api_response(200, b"content", False)
        name = "image_id"
        result = self.service.open(name)
        self.assertEqual(result, b"content")

    @patch("requests.delete")
    def test_failed_delete(self, mock_delete):
        mock_delete.return_value = get_dummy_api_response(400, "", False)
        name = "image_id"
        try:
            self.service.delete(name)
            self.fail("ApiException should have been raised")
        except ApiException as e:
            self.assertEqual(e.status_code, 400)

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
        try:
            self.service.get_one_time_upload_url()
            self.fail("ApiException should have been raised")
        except ApiException as e:
            self.assertEqual(e.status_code, 400)

    @patch("requests.post")
    def test_success_get_one_time_upload_url(self, mock_post):
        mock_post.return_value = get_dummy_api_response(200, "{}")
        result = self.service.get_one_time_upload_url()
        self.assertEqual(result, {})

    @patch("requests.get")
    def test_success_get_image_details(self, mock_get):
        mock_get.return_value = get_dummy_api_response(
            200, '{"result": {"id": "test", "uploaded": "2024-01-01T00:00:00Z"}}'
        )
        name = "image_id"
        result = self.service.get_image_details(name)
        self.assertEqual(result["id"], "test")
        self.assertEqual(result["uploaded"], "2024-01-01T00:00:00Z")

    @patch("requests.get")
    def test_not_found_get_image_details(self, mock_get):
        mock_get.return_value = get_dummy_api_response(
            404, '{"errors": [{"message": "Image not found"}]}'
        )
        name = "image_id"
        try:
            self.service.get_image_details(name)
            self.fail("ApiException should have been raised")
        except ApiException as e:
            self.assertEqual(e.status_code, 404)

    @patch("requests.get")
    def test_server_error_get_image_details(self, mock_get):
        mock_get.return_value = get_dummy_api_response(
            500, '{"errors": [{"message": "Internal server error"}]}'
        )
        name = "image_id"
        try:
            self.service.get_image_details(name)
            self.fail("ApiException should have been raised")
        except ApiException as e:
            self.assertEqual(e.status_code, 500)

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("cloudflare_images.service.time.time", return_value=1700000000)
    def test_get_signed_url(self, mock_time):
        url = self.service.get_signed_url("image_id", "public")
        self.assertEqual(
            url,
            "https://imagedelivery.net/account_hash/image_id/public"
            "?exp=1700086400"
            "&sig=47d894d4a839199008e704e6719ef4073c056af30fb694d70342e8c4b951bce8",
        )

    @override_settings(
        CLOUDFLARE_IMAGES_SIGNING_KEY="secret",
        CLOUDFLARE_IMAGES_SIGNED_URL_TTL=120,
    )
    @patch("cloudflare_images.service.time.time", return_value=1700000000)
    def test_get_signed_url_custom_ttl(self, mock_time):
        url = self.service.get_signed_url("image_id", "public")
        self.assertEqual(
            url,
            "https://imagedelivery.net/account_hash/image_id/public"
            "?exp=1700000120"
            "&sig=424ebe102ae30624d00c12e23cb375697e61f5286c82d7f219727dde85f53de8",
        )

    @override_settings(
        CLOUDFLARE_IMAGES_SIGNING_KEY="secret",
        CLOUDFLARE_IMAGES_DOMAIN="example.com",
    )
    @patch("cloudflare_images.service.time.time", return_value=1700000000)
    def test_get_signed_url_with_custom_domain(self, mock_time):
        url = self.service.get_signed_url("image_id", "public")
        self.assertEqual(
            url,
            "https://example.com/cdn-cgi/imagedelivery/account_hash"
            "/image_id/public?exp=1700086400"
            "&sig=6c5be941d5b2280f3514f15448b15ed670162145a4af28ceb9865a39338b8c8a",
        )

    def test_get_signed_url_without_signing_key(self):
        self.assertRaises(
            ImproperlyConfigured,
            self.service.get_signed_url,
            "image_id",
            "public",
        )

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch.object(
        CloudflareImagesService,
        "get_url",
        return_value="https://imagedelivery.net/account_hash/image_id/public?foo=bar",
    )
    @patch("cloudflare_images.service.time.time", return_value=1700000000)
    def test_get_signed_url_with_existing_query(self, mock_time, mock_get_url):
        self.assertEqual(
            self.service.get_signed_url("image_id", "public"),
            "https://imagedelivery.net/account_hash/image_id/public"
            "?foo=bar&exp=1700086400"
            "&sig=6098f3a62664fbde77e25200876a8a4abe5ccd5f7f3e4e0aff21ffe5903ae16e",
        )

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    def test_get_signed_url_invalid_expiry(self):
        self.assertRaises(
            ValueError,
            self.service.get_signed_url,
            "image_id",
            "public",
            0,
        )

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("requests.post")
    def test_upload_require_signed_urls(self, mock_post):
        mock_post.return_value = get_dummy_api_response(
            200, '{"result": {"id": "test"}}'
        )
        file = get_dummy_image()
        result = self.service.upload(file, require_signed_urls=True)
        self.assertEqual(result, "test")
        self.assertEqual(
            mock_post.call_args.kwargs["data"],
            {"requireSignedURLs": "true"},
        )
        file.close()

    @patch("requests.post")
    def test_upload_public_by_default(self, mock_post):
        mock_post.return_value = get_dummy_api_response(
            200, '{"result": {"id": "test"}}'
        )
        file = get_dummy_image()
        self.service.upload(file)
        self.assertIsNone(mock_post.call_args.kwargs["data"])
        file.close()

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("requests.post")
    def test_get_one_time_upload_url_require_signed_urls(self, mock_post):
        mock_post.return_value = get_dummy_api_response(200, "{}")
        result = self.service.get_one_time_upload_url(require_signed_urls=True)
        self.assertEqual(result, {})
        self.assertEqual(
            mock_post.call_args.kwargs["files"],
            {"requireSignedURLs": (None, "true")},
        )

    @patch("requests.post")
    def test_get_one_time_upload_url_public_by_default(self, mock_post):
        mock_post.return_value = get_dummy_api_response(200, "{}")
        self.service.get_one_time_upload_url()
        self.assertIsNone(mock_post.call_args.kwargs["files"])

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("cloudflare_images.service.time.time", return_value=1700000000)
    @patch("requests.get")
    def test_open_signed(self, mock_get, mock_time):
        mock_get.return_value = get_dummy_api_response(200, b"content", False)
        result = self.service.open("image_id", signed=True)
        self.assertEqual(result, b"content")
        self.assertEqual(
            mock_get.call_args.args[0],
            "https://imagedelivery.net/account_hash/image_id/public"
            "?exp=1700086400"
            "&sig=47d894d4a839199008e704e6719ef4073c056af30fb694d70342e8c4b951bce8",
        )

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("requests.get")
    def test_open_public_by_default(self, mock_get):
        mock_get.return_value = get_dummy_api_response(200, b"content", False)
        self.service.open("image_id")
        self.assertNotIn("sig=", mock_get.call_args.args[0])
