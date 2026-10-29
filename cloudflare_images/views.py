"""
Views for the widget
"""

import json
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views.generic import View

from cloudflare_images.service import ApiException, CloudflareImagesService


class WidgetAPI(View):
    """
    View for the widget
    """

    def get_upload_options(self, request: HttpRequest) -> dict[str, Any]:
        """
        Returns the options passed to get_one_time_upload_url.
        Override this method to request private images.
        """
        return {}

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Returns a one time upload URL.
        This endpoint has no security and should just be used as an example
        on how to implement your own. See the Config object's documentation.
        """
        service = CloudflareImagesService()
        try:
            data = service.get_one_time_upload_url(**self.get_upload_options(request))
            return JsonResponse(data)
        except ApiException as e:
            return self._error_response(e)

    def _error_response(self, exception: ApiException) -> JsonResponse:
        """
        Returns a JSON error response, even when Cloudflare sends HTML or text.
        The upstream status is not forwarded; this example endpoint always
        returns 400 for Cloudflare API errors.
        """
        try:
            payload = json.loads(str(exception))
        except (json.JSONDecodeError, TypeError):
            payload = {"error": str(exception)}

        if not isinstance(payload, dict):
            payload = {"error": payload}

        return JsonResponse(payload, status=400)
