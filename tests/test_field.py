"""
Tests related to the CloudflareImagesField
"""

from django.test import TestCase, override_settings
from django import forms
from cloudflare_images.widget import CloudflareImagesWidget
from cloudflare_images.field import (
    CloudflareImagesField,
    CloudflareImagesFieldFile,
    CloudflareImageIDField,
)


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

        # This line is here to satisfy `ty` as formfield returns either a forms.Field or None
        if form_field is not None:
            self.assertIsInstance(form_field.widget, CloudflareImagesWidget)
