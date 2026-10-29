"""
Custom widget for Direct Creator Uploads
"""

from typing import Any

from django.forms.utils import flatatt
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

        widget_attrs = dict(context["widget"]["attrs"])
        explicit_id = self.attrs.get("id")
        file_id = explicit_id or f"{name}-file"
        hidden_id = f"{explicit_id}-value" if explicit_id else name
        error_id = f"{file_id}-error"

        file_attrs = {
            key: attr
            for key, attr in widget_attrs.items()
            if key
            not in {
                "name",
                "value",
                "type",
                "multiple",
                "id",
                "accept",
                "aria-describedby",
            }
        }
        file_attrs["id"] = file_id
        file_attrs["accept"] = widget_attrs.get("accept") or "image/*"

        if value and "required" in file_attrs:
            file_attrs.pop("required")

        described_by = widget_attrs.get("aria-describedby")
        described_by_ids = str(described_by).split() if described_by else []
        if error_id not in described_by_ids:
            described_by_ids.append(error_id)
        file_attrs["aria-describedby"] = " ".join(described_by_ids)

        context["widget"]["value"] = value
        context["widget"]["url"] = None
        if value:
            if self.signed:
                context["widget"]["url"] = service.get_signed_url(value, config.variant)
            else:
                context["widget"]["url"] = service.get_url(value, config.variant)
        context["widget"]["upload_endpoint"] = config.upload_endpoint
        context["widget"]["signed"] = self.signed
        context["widget"]["file_attrs"] = flatatt(file_attrs)
        context["widget"]["file_id"] = file_id
        context["widget"]["hidden_id"] = hidden_id
        context["widget"]["error_id"] = error_id
        context["widget"]["button_disabled"] = bool(widget_attrs.get("disabled"))

        return context

    class Media:
        """
        Inner class defining the static assets for the widget
        """

        css = {"all": ["css/widget.css"]}
        js = ["js/widget.js"]
