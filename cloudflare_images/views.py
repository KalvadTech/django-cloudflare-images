"""
Views for the widget
"""

from django.http import JsonResponse
from django.views.generic import View
from cloudflare_images.service import CloudflareImagesService

class WidgetAPI(View):
    """
    View for the widget
    """

    def get(self, request):
        """
        Returns a one time upload URL
        """
        service = CloudflareImagesService()
        data = service.get_one_time_upload_url()
        return JsonResponse(data)
