"""
Tests related to the CloudflareImagesField
"""

from django.test import TestCase, override_settings
from django.conf import settings
from cloudflare_images.field import CloudflareImagesField, CloudflareImagesFieldFile


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
