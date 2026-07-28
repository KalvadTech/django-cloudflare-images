"""
Contains the Cloudflare Image storage which is supposed to replace Django's
default Storage (see README.md)
Django's default storage class: https://github.com/django/django/blob/main/django/core/files/storage.py
"""

from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from cloudflare_images.config import Config
from cloudflare_images.service import CloudflareImagesService


@deconstructible
class CloudflareImagesStorage(Storage):
    """
    Django storage for Cloudflare Images
    """

    def __init__(self) -> None:
        """
        Sets up the storage
        """
        super().__init__()

        self.service = CloudflareImagesService()

    def _open(self, name: str, mode: str = "rb") -> File:
        """
        Returns the image as a File
        The parameter "mode" has been kept to respect the original signature
        (and it fails without it) but it won't have any impact
        Has to be implemented.
        """
        content = self.service.open(name)
        return File(content, name=name)

    def _save(self, name: str, content: File) -> str:
        """
        Tries to upload the file and return its name
        Has to be implemented.
        """
        new_name = self.generate_filename(name)
        content.name = new_name
        return self.service.upload(content)

    def get_valid_name(self, name: str) -> str:
        """
        Returns a valid name for the file.
        Has to be implemented.
        """
        return name

    def get_available_name(self, name: str, max_length: str | None = None) -> str:
        """
        Returns the available name for the file.
        Has to be implemented.
        """
        return self.generate_filename(name)

    def generate_filename(self, filename: str) -> str:
        """
        Returns the name of the file.
        Has to be implemented.
        """
        return filename

    def delete(self, name: str) -> None:
        """
        Tries to delete the specified file from the storage system.
        Has to be implemented.
        """
        self.service.delete(name)

    def exists(self, name: str) -> bool:
        """
        Check if an image exists in Cloudflare Images.

        Note: This makes an HTTP API call to Cloudflare on every invocation.
        If you need to check many images, consider implementing your own
        caching layer to reduce API calls.

        Args:
            name: The Cloudflare image ID to check

        Returns:
            True if the image exists, False if it doesn't

        Raises:
            ApiException: If the API call fails for reasons other than 404
        """
        from cloudflare_images.service import ApiException

        try:
            self.service.get_image_details(name)
            return True
        except ApiException as e:
            if e.status_code == 404:
                return False
            raise

    def listdir(self, path: str) -> None:
        """
        List the contents of the specified path. Return a 2-tuple of lists:
        the first item being directories, the second item being files.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a listdir() method"
        )

    def size(self, name: str) -> int:
        """
        Return the total size, in bytes, of the file specified by name.
        """
        content = self.service.open(name)
        return len(content)

    def url(self, name: str) -> str:
        """
        Return an absolute URL where the file's contents can be accessed
        directly by a web browser.
        Has to be implemented.
        """
        return self.url_with_variant(name, Config().variant)

    def url_with_variant(self, name: str, variant: str) -> str:
        """
        Custom methods which allow to pass a variant and respect the original
        signature of `url`
        """
        return self.service.get_url(name, variant)

    def get_accessed_time(self, name: str) -> None:
        """
        Return the last accessed time (as a datetime) of the file specified by
        name. The datetime will be timezone-aware if USE_TZ=True.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a get_accessed_time() method"
        )

    def get_created_time(self, name: str) -> None:
        """
        Return the creation time (as a datetime) of the file specified by name.
        The datetime will be timezone-aware if USE_TZ=True.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a get_created_time() method"
        )

    def get_modified_time(self, name: str) -> None:
        """
        Return the last modified time (as a datetime) of the file specified by
        name. The datetime will be timezone-aware if USE_TZ=True.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a get_modified_time() method"
        )
