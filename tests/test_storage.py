"""
Test related to the CloudflareImagesStorage
"""

from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from cloudflare_images.service import ApiException
from cloudflare_images.storage import CloudflareImagesStorage

from .utils import get_dummy_image, get_dummy_image_name


class CloudflareImageStorageTests(TestCase):
    """
    Test case for the CloudflareImagesStorage
    """

    def setUp(self):
        self.storage = CloudflareImagesStorage()

    def test_has_service(self):
        service = self.storage.service
        self.assertTrue(service is not None)

    @patch("cloudflare_images.service.CloudflareImagesService.upload")
    def test_save(self, mock_upload):
        mock_upload.side_effect = ApiException("Upload failed")
        name = get_dummy_image_name()
        content = get_dummy_image()
        self.assertRaises(ApiException, self.storage.save, name, content)
        content.close()

    @patch("cloudflare_images.service.CloudflareImagesService.open")
    def test_open(self, mock_open):
        mock_open.side_effect = ApiException("Open failed")
        name = "image_id"
        self.assertRaises(ApiException, self.storage.open, name)

    @patch("cloudflare_images.service.CloudflareImagesService.open")
    def test_open_mocked(self, mock_open):
        mock_open.return_value = b"content"
        name = get_dummy_image_name()
        fff = self.storage.open(name)
        self.assertEqual(fff.file, b"content")
        self.assertEqual(fff.name, name)

    @patch("cloudflare_images.service.CloudflareImagesService.delete")
    def test_delete(self, mock_delete):
        mock_delete.side_effect = ApiException("Delete failed")
        name = "image_id"
        self.assertRaises(ApiException, self.storage.delete, name)

    def test_url(self):
        name = "image_id"
        url = self.storage.url(name)
        hardcoded_url = "https://imagedelivery.net/account_hash/image_id/public"
        self.assertEqual(url, hardcoded_url)

    def test_url_with_variant(self):
        name = "image_id"
        variant = "custom"
        url = self.storage.url_with_variant(name, variant)
        hardcoded_url = "https://imagedelivery.net/account_hash/image_id/custom"
        self.assertEqual(url, hardcoded_url)

    @override_settings(CLOUDFLARE_IMAGES_DOMAIN="example.com")
    def test_url_with_custom_domain(self):
        name = "image_id"
        url = self.storage.url(name)
        hardcoded_url = (
            "https://example.com/cdn-cgi/imagedelivery/account_hash/image_id/public"
        )
        self.assertEqual(url, hardcoded_url)

    @override_settings(CLOUDFLARE_IMAGES_DOMAIN="example.com")
    def test_url_with_variant_with_custom_domain(self):
        name = "image_id"
        variant = "custom"
        url = self.storage.url_with_variant(name, variant)
        hardcoded_url = (
            "https://example.com/cdn-cgi/imagedelivery/account_hash/image_id/custom"
        )
        self.assertEqual(url, hardcoded_url)

    def test_get_valid_name(self):
        name = "image_id"
        self.assertEqual(name, self.storage.get_valid_name(name))

    @patch("cloudflare_images.service.CloudflareImagesService.get_image_details")
    def test_exists_true(self, mock_get_details):
        mock_get_details.return_value = {
            "id": "image_id",
            "uploaded": "2024-01-01T00:00:00Z",
        }
        name = "image_id"
        result = self.storage.exists(name)
        self.assertTrue(result)
        mock_get_details.assert_called_once_with(name)

    @patch("cloudflare_images.service.CloudflareImagesService.get_image_details")
    def test_exists_false(self, mock_get_details):
        mock_get_details.side_effect = ApiException("Not found", status_code=404)
        name = "image_id"
        result = self.storage.exists(name)
        self.assertFalse(result)
        mock_get_details.assert_called_once_with(name)

    @patch("cloudflare_images.service.CloudflareImagesService.get_image_details")
    def test_exists_api_error(self, mock_get_details):
        mock_get_details.side_effect = ApiException("Server error", status_code=500)
        name = "image_id"
        self.assertRaises(ApiException, self.storage.exists, name)

    @patch("cloudflare_images.service.CloudflareImagesService.get_image_details")
    def test_exists_no_status_code(self, mock_get_details):
        mock_get_details.side_effect = ApiException("Network error", status_code=None)
        name = "image_id"
        self.assertRaises(ApiException, self.storage.exists, name)

    def test_listdir(self):
        path = "/my/path"
        self.assertRaises(NotImplementedError, self.storage.listdir, path)

    @patch("cloudflare_images.service.CloudflareImagesService.open")
    def test_size(self, mock_open):
        mock_open.side_effect = ApiException("Open failed")
        name = "image_id"
        self.assertRaises(ApiException, self.storage.size, name)

    @patch("cloudflare_images.service.CloudflareImagesService.open")
    def test_size_mocked(self, mock_open):
        mock_open.return_value = b"content"
        name = get_dummy_image_name()
        fff = self.storage.size(name)
        self.assertEqual(fff, 7)

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("cloudflare_images.service.CloudflareImagesService.upload")
    def test_private_storage_save(self, mock_upload):
        mock_upload.return_value = "image_id"
        storage = CloudflareImagesStorage(require_signed_urls=True)
        content = get_dummy_image()
        storage.save(get_dummy_image_name(), content)
        self.assertTrue(mock_upload.call_args.kwargs["require_signed_urls"])
        content.close()

    @patch("cloudflare_images.service.CloudflareImagesService.upload")
    def test_private_storage_save_without_signing_key(self, mock_upload):
        storage = CloudflareImagesStorage(require_signed_urls=True)
        content = get_dummy_image()
        self.assertRaises(
            ImproperlyConfigured,
            storage.save,
            get_dummy_image_name(),
            content,
        )
        mock_upload.assert_not_called()
        content.close()

    @patch("cloudflare_images.service.CloudflareImagesService.open")
    def test_private_storage_open(self, mock_open):
        mock_open.return_value = b"content"
        storage = CloudflareImagesStorage(require_signed_urls=True)
        storage.open("image_id")
        mock_open.assert_called_once_with("image_id", signed=True)

    @patch("cloudflare_images.service.CloudflareImagesService.open")
    def test_private_storage_size(self, mock_open):
        mock_open.return_value = b"content"
        storage = CloudflareImagesStorage(require_signed_urls=True)
        self.assertEqual(storage.size("image_id"), 7)
        mock_open.assert_called_once_with("image_id", signed=True)

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("cloudflare_images.service.time.time", return_value=1700000000)
    def test_private_storage_url(self, mock_time):
        storage = CloudflareImagesStorage(require_signed_urls=True)
        self.assertEqual(
            storage.url("image_id"),
            "https://imagedelivery.net/account_hash/image_id/public"
            "?exp=1700086400"
            "&sig=47d894d4a839199008e704e6719ef4073c056af30fb694d70342e8c4b951bce8",
        )

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    @patch("cloudflare_images.service.time.time", return_value=1700000000)
    def test_private_storage_url_with_variant(self, mock_time):
        storage = CloudflareImagesStorage(require_signed_urls=True)
        url = storage.url_with_variant("image_id", "custom")
        self.assertIn("/image_id/custom?", url)
        self.assertIn("&sig=", url)

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    def test_public_storage_url_stays_public(self):
        self.assertNotIn("sig=", self.storage.url("image_id"))

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    def test_explicit_signed_url(self):
        url = self.storage.signed_url("image_id")
        self.assertIn("?exp=", url)
        self.assertIn("&sig=", url)

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="secret")
    def test_explicit_signed_url_custom_variant(self):
        url = self.storage.signed_url("image_id", "custom")
        self.assertIn("/image_id/custom?", url)
        self.assertIn("&sig=", url)

    def test_private_storage_deconstruct(self):
        storage = CloudflareImagesStorage(require_signed_urls=True)
        path, args, kwargs = storage.deconstruct()  # ty: ignore[unresolved-attribute]
        self.assertEqual(path, "cloudflare_images.storage.CloudflareImagesStorage")
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {"require_signed_urls": True})

    def test_public_storage_deconstruct(self):
        path, args, kwargs = self.storage.deconstruct()  # ty: ignore[unresolved-attribute]
        self.assertEqual(path, "cloudflare_images.storage.CloudflareImagesStorage")
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})

    def test_get_accessed_time(self):
        name = "image_id"
        self.assertRaises(NotImplementedError, self.storage.get_accessed_time, name)

    def test_get_created_time(self):
        name = "image_id"
        self.assertRaises(NotImplementedError, self.storage.get_created_time, name)

    def test_get_modified_time(self):
        name = "image_id"
        self.assertRaises(NotImplementedError, self.storage.get_modified_time, name)
