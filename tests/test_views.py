"""
Tests related to the CloudflareImagesWidget Views
"""

import json
from unittest.mock import patch

from django.http import JsonResponse
from django.test import RequestFactory, TestCase

from cloudflare_images.service import ApiException
from cloudflare_images.views import WidgetAPI


class PrivateWidgetAPI(WidgetAPI):
    """
    Test view requesting private uploads
    """

    def get_upload_options(self, request):
        return {"require_signed_urls": True}


class WidgetAPITests(TestCase):
    """
    Test case for the WidgetAPI view
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.view = WidgetAPI()

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_success(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.return_value = {
            "uploadURL": "https://upload.example.com/token"
        }

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_api_exception(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.side_effect = ApiException(
            '{"error": "Invalid token"}'
        )

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_api_exception_with_json_parsing(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.side_effect = ApiException(
            '{"error": {"message": "Rate limit exceeded"}}'
        )

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_api_exception_with_html(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.side_effect = ApiException(
            "<html>Bad gateway</html>", status_code=502
        )

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"error": "<html>Bad gateway</html>"},
        )

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_api_exception_with_plain_text(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.side_effect = ApiException(
            "Service unavailable", status_code=503
        )

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"error": "Service unavailable"},
        )

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_api_exception_does_not_forward_status(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.side_effect = ApiException(
            "Rate limited", status_code=429
        )

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_api_exception_with_non_dict_json(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.side_effect = ApiException(
            '["error"]', status_code=400
        )

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"error": ["error"]})

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_upload_options(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.return_value = {
            "uploadURL": "https://upload.example.com/token"
        }

        request = self.factory.get("/")
        response = PrivateWidgetAPI().get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        mock_service.return_value.get_one_time_upload_url.assert_called_once_with(
            require_signed_urls=True
        )
