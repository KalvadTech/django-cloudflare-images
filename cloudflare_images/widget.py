"""
Custom widget for Direct Creator Uploads
"""

from typing import Any

from django.forms.widgets import Widget
from django.utils.datastructures import MultiValueDict

from cloudflare_images.config import Config
from cloudflare_images.service import CloudflareImagesService


class CloudflareImagesWidget(Widget):
    """
    Widget
    """

    template_name = "widget.html"

    def __init__(
        self,
        attrs: dict[str, Any] | None = None,
        *,
        signed: bool = False,
    ) -> None:
        super().__init__(attrs)
        self.signed = signed

    def value_from_datadict(
        self, data: MultiValueDict, files: MultiValueDict, name: str
    ) -> str | None:
        return data.get(name)

    def get_context(
        self, name: str, value: str | None, attrs: dict[str, Any]
    ) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        service = CloudflareImagesService()
        config = Config()

        context["widget"]["value"] = value
        context["widget"]["url"] = None
        if value:
            if self.signed:
                context["widget"]["url"] = service.get_signed_url(value, config.variant)
            else:
                context["widget"]["url"] = service.get_url(value, config.variant)
        context["widget"]["upload_endpoint"] = config.upload_endpoint
        context["widget"]["signed"] = self.signed

        return context

    class Media:
        """
        Inner class defining the static assets for the widget
        """

        css = {"all": ["css/widget.css"]}
        js = ["js/widget.js"]
