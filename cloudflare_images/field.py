"""
Contains all the fields related classes to support custom features
such as variants in Cloudflare Images
"""

from django import forms
from django.db.models import CharField
from django.db.models.fields.files import (
    ImageFieldFile,
    ImageField,
    ImageFileDescriptor,
)
from cloudflare_images.config import Config
from cloudflare_images.widget import CloudflareImagesWidget


class CloudflareImagesFileDescriptor(ImageFileDescriptor):
    """
    Inherits ImageField's descriptor class
    """

    pass


class CloudflareImagesFieldFile(ImageFieldFile):
    """
    Inherits ImageField's attr class
    """

    @property
    def url(self) -> str:
        """
        Overriding the default url method to pass our variant
        """
        return self.storage.url_with_variant(self.name, variant=self.field.variant)


class CloudflareImagesField(ImageField):
    """
    Custom field based on ImageField allowing us to pass a variant
    """

    attr_class = CloudflareImagesFieldFile
    descriptor_class = CloudflareImagesFileDescriptor
    description = "Image"

    def __init__(
        self,
        verbose_name: str | None = None,
        name: str | None = None,
        width_field: str | None = None,
        height_field: str | None = None,
        variant: str | None = None,
        **kwargs,
    ):
        """
        Calling ImageFieldFile constructor and setting our variant
        """
        self.variant = variant or Config().variant
        super().__init__(verbose_name, name, width_field, height_field, **kwargs)

    def deconstruct(self):
        """
        Returns the deconstructed version of our field.
        Same as ImageField with variant on top
        """
        name, path, args, kwargs = super().deconstruct()
        kwargs["variant"] = self.variant
        return name, path, args, kwargs


class CloudflareImageIDField(CharField):
    """
    Stores a Cloudflare Image ID (for direct uploads)"
    """

    def __init__(self, *args, variant: str | None = None, **kwargs):
        """
        Calling CharField constructor and setting our variant
        """
        self.variant = variant or Config().variant
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """
        Will set the custom uploader widget by default (no need to everytime change widgets{} in your forms)
        """
        defaults = {"widget": CloudflareImagesWidget()}
        defaults.update(kwargs)
        return super().formfield(**defaults)
