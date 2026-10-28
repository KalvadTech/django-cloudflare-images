"""
Tests related to the CloudflareImagesField
"""

from unittest.mock import patch

from django import forms
from django.test import TestCase, override_settings

from cloudflare_images.field import (
    CloudflareImageIDField,
    CloudflareImagesField,
    CloudflareImagesFieldFile,
)
from cloudflare_images.storage import CloudflareImagesStorage
from cloudflare_images.widget import CloudflareImagesWidget


class CloudflareImageFieldTests(TestCase):
    """
    Test case for the CloudflareImagesField
    """

    def test_default_variant(self):
        field = CloudflareImagesField()
        self.assertEqual(field.variant, "public")

    def test_custom_variant(self):
        variant = "custom"
        field = CloudflareImagesField(variant=variant)
        self.assertEqual(field.variant, variant)

    def test_deconstruct_default_variant(self):
        field = CloudflareImagesField()
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(kwargs.get("variant"), "public")

    def test_deconstruct_custom_variant(self):
        variant = "custom"
        field = CloudflareImagesField(variant=variant)
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(kwargs.get("variant"), variant)

    def test_custom_storage(self):
        storage = CloudflareImagesStorage(require_signed_urls=True)
        field = CloudflareImagesField(storage=storage)
        self.assertIs(field.storage, storage)

    def test_deconstruct_custom_storage(self):
        storage = CloudflareImagesStorage(require_signed_urls=True)
        field = CloudflareImagesField(storage=storage)
        name, path, args, kwargs = field.deconstruct()
        self.assertIs(kwargs.get("storage"), storage)
        self.assertTrue(kwargs["storage"].require_signed_urls)


class CloudflareImageFieldFileTests(TestCase):
    """
    Test case for the CloudflareImagesFieldFile
    """

    def test_url_default_variant(self):
        field = CloudflareImagesField()
        field_file = CloudflareImagesFieldFile(None, field, "image_id")
        url = field_file.url
        hardcoded_url = "https://imagedelivery.net/account_hash/image_id/public"
        self.assertEqual(url, hardcoded_url)

    def test_url_custom_variant(self):
        field = CloudflareImagesField(variant="custom")
        field_file = CloudflareImagesFieldFile(None, field, "image_id")
        url = field_file.url
        hardcoded_url = "https://imagedelivery.net/account_hash/image_id/custom"
        self.assertEqual(url, hardcoded_url)

    @override_settings(CLOUDFLARE_IMAGES_DOMAIN="example.com")
    def test_url_default_variant_with_custom_domain(self):
        field = CloudflareImagesField()
        field_file = CloudflareImagesFieldFile(None, field, "image_id")
        url = field_file.url
        hardcoded_url = (
            "https://example.com/cdn-cgi/imagedelivery/account_hash/image_id/public"
        )
        self.assertEqual(url, hardcoded_url)

    @override_settings(CLOUDFLARE_IMAGES_DOMAIN="example.com")
    def test_url_custom_variant_with_custom_domain(self):
        field = CloudflareImagesField(variant="custom")
        field_file = CloudflareImagesFieldFile(None, field, "image_id")
        url = field_file.url
        hardcoded_url = (
            "https://example.com/cdn-cgi/imagedelivery/account_hash/image_id/custom"
        )
        self.assertEqual(url, hardcoded_url)

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("cloudflare_images.service.time.time", return_value=1700000000)
    def test_signed_url_default_variant(self, mock_time):
        field = CloudflareImagesField()
        field_file = CloudflareImagesFieldFile(None, field, "image_id")
        self.assertEqual(
            field_file.signed_url(),
            "https://imagedelivery.net/account_hash/image_id/public"
            "?exp=1700086400"
            "&sig=47d894d4a839199008e704e6719ef4073c056af30fb694d70342e8c4b951bce8",
        )

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    def test_signed_url_custom_variant_and_ttl(self):
        field = CloudflareImagesField(variant="custom")
        field_file = CloudflareImagesFieldFile(None, field, "image_id")
        url = field_file.signed_url(expires_in=120)
        self.assertIn("/image_id/custom?", url)
        self.assertIn("&sig=", url)

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    def test_url_with_private_storage(self):
        storage = CloudflareImagesStorage(require_signed_urls=True)
        field = CloudflareImagesField(storage=storage)
        field_file = CloudflareImagesFieldFile(None, field, "image_id")
        self.assertIn("&sig=", field_file.url)


class CloudflareImageIDTests(TestCase):
    """
    Test case for the CloudflareImageIDField
    """

    def test_default_variant(self):
        field = CloudflareImageIDField()
        variant = field.variant
        self.assertEqual(variant, "public")

    def test_custom_variant(self):
        field = CloudflareImageIDField(variant="custom")
        variant = field.variant
        self.assertEqual(variant, "custom")

    def test_formfield(self):
        field = CloudflareImageIDField(variant="custom")
        form_field = field.formfield()
        self.assertIsInstance(form_field, forms.CharField)

        # This line is here to satisfy `ty` as formfield returns either a
        # forms.Field or None
        if form_field is not None:
            self.assertIsInstance(form_field.widget, CloudflareImagesWidget)
