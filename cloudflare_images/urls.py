"""
Routers for the widget's API
"""

from django.urls import path
from cloudflare_images.views import WidgetAPI

urlpatterns = [
    path("cloudflare_images/api", WidgetAPI.as_view(), name="widget-api"),
]
