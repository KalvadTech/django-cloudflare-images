"""
Tests related to the CloudflareImagesWidget
"""

from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils.datastructures import MultiValueDict

from cloudflare_images.widget import CloudflareImagesWidget


class CloudflareImagesWidgetTests(TestCase):
    """
    Test case for the CloudflareImagesWidget
    """

    def setUp(self):
        self.widget = CloudflareImagesWidget()

    def test_template_name(self):
        template_name = self.widget.template_name
        self.assertEqual(template_name, "widget.html")

    def test_value_from_datadict_with_value(self):
        data = MultiValueDict({"test_field": ["image_id_123"]})
        files = MultiValueDict()
        result = self.widget.value_from_datadict(data, files, "test_field")
        self.assertEqual(result, "image_id_123")

    def test_value_from_datadict_without_value(self):
        data = MultiValueDict()
        files = MultiValueDict()
        result = self.widget.value_from_datadict(data, files, "test_field")
        self.assertIsNone(result)

    def test_value_from_datadict_with_empty_value(self):
        data = MultiValueDict({"test_field": [""]})
        files = MultiValueDict()
        result = self.widget.value_from_datadict(data, files, "test_field")
        self.assertEqual(result, "")

    @patch("cloudflare_images.widget.Config")
    @patch("cloudflare_images.widget.CloudflareImagesService")
    def test_get_context_with_value(self, mock_service, mock_config):
        mock_service.return_value.get_url.return_value = (
            "https://example.com/image_id_123/public"
        )
        mock_config.return_value.upload_endpoint = "/test/api"

        context = self.widget.get_context(
            "test_field", "image_id_123", {"class": "test"}
        )

        self.assertEqual(context["widget"]["value"], "image_id_123")
        self.assertEqual(
            context["widget"]["url"], "https://example.com/image_id_123/public"
        )
        self.assertEqual(context["widget"]["upload_endpoint"], "/test/api")
        self.assertFalse(context["widget"]["signed"])

    @patch("cloudflare_images.widget.Config")
    @patch("cloudflare_images.widget.CloudflareImagesService")
    def test_get_context_without_value(self, mock_service, mock_config):
        mock_config.return_value.upload_endpoint = "/test/api"

        context = self.widget.get_context("test_field", None, {"class": "test"})

        self.assertIsNone(context["widget"]["value"])
        self.assertIsNone(context["widget"]["url"])
        self.assertEqual(context["widget"]["upload_endpoint"], "/test/api")
        mock_service.return_value.get_url.assert_not_called()

    @patch("cloudflare_images.widget.Config")
    @patch("cloudflare_images.widget.CloudflareImagesService")
    def test_get_context_with_empty_value(self, mock_service, mock_config):
        mock_config.return_value.upload_endpoint = "/test/api"

        context = self.widget.get_context("test_field", "", {"class": "test"})

        self.assertEqual(context["widget"]["value"], "")
        self.assertIsNone(context["widget"]["url"])
        self.assertEqual(context["widget"]["upload_endpoint"], "/test/api")
        mock_service.return_value.get_url.assert_not_called()

    @override_settings(CLOUDFLARE_IMAGES_VARIANT="custom")
    def test_get_context_uses_configured_variant(self):
        context = self.widget.get_context("test_field", "image_id_123", {})
        self.assertEqual(
            context["widget"]["url"],
            "https://imagedelivery.net/account_hash/image_id_123/custom",
        )

    @patch("cloudflare_images.widget.Config")
    @patch("cloudflare_images.widget.CloudflareImagesService")
    def test_get_context_signed(self, mock_service, mock_config):
        mock_service.return_value.get_signed_url.return_value = "signed-url"
        mock_config.return_value.variant = "custom"
        mock_config.return_value.upload_endpoint = "/test/api"
        widget = CloudflareImagesWidget(signed=True)

        context = widget.get_context("test_field", "image_id_123", {})

        self.assertEqual(context["widget"]["url"], "signed-url")
        self.assertTrue(context["widget"]["signed"])
        mock_service.return_value.get_signed_url.assert_called_once_with(
            "image_id_123", "custom"
        )
        mock_service.return_value.get_url.assert_not_called()

    def test_media_css(self):
        media = CloudflareImagesWidget.Media.css
        self.assertEqual(media["all"], ["css/widget.css"])

    def test_media_js(self):
        media = CloudflareImagesWidget.Media.js
        self.assertEqual(media, ["js/widget.js"])
