"""
Contains the Cloudflare Image storage which is supposed to replace Django's
default Storage (see README.md)
Django's default storage class: https://github.com/django/django/blob/main/django/core/files/storage.py
"""

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from cloudflare_images.service import CloudflareImagesService


class CloudflareImagesStorage(Storage):
    """
    Django storage for Cloudflare Images
    """

    def __init__(self):
        """
        Setups the storage
        """
        super().__init__()

        self.service = CloudflareImagesService()

    def _open(self, name, mode="rb"):
        """
        Returns the image as a File
        The parameter "mode" has been kept to respect the original signature
        (and it fails without it) but it wont have any impact
        Has to be implemented.
        """
        return self.service.open(name)

    def _save(self, name, content):
        """
        Tries to upload the file and return its name
        Has to be implemented.
        """
        new_name = self.generate_filename(name)
        content.name = new_name
        return self.service.upload(content)

    def get_valid_name(self, name):
        """
        Returns a valid name for the file.
        Has to be implemented.
        """
        return name

    def get_available_name(self, name, max_length=None):
        """
        Returns the available name for the file.
        Has to be implemented.
        """
        return self.generate_filename(name)

    def generate_filename(self, filename):
        """
        Returns the name of the file.
        Has to be implemented.
        """
        return filename

    def delete(self, name):
        """
        Tries to delete the specified file from the storage system.
        Has to be implemented.
        """
        self.service.delete(name)

    def exists(self, name):
        """
        Return True if a file referenced by the given name already exists in the
        storage system, or False if the name is available for a new file.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide an exists() method"
        )

    def listdir(self, path):
        """
        List the contents of the specified path. Return a 2-tuple of lists:
        the first item being directories, the second item being files.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a listdir() method"
        )

    def size(self, name):
        """
        Return the total size, in bytes, of the file specified by name.
        """
        raise NotImplementedError("subclasses of Storage must provide a size() method")

    def url(self, name):
        """
        Return an absolute URL where the file's contents can be accessed
        directly by a web browser.
        Has to be implemented.
        """
        return self.service.get_url(name)

    def get_accessed_time(self, name):
        """
        Return the last accessed time (as a datetime) of the file specified by
        name. The datetime will be timezone-aware if USE_TZ=True.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a get_accessed_time() method"
        )

    def get_created_time(self, name):
        """
        Return the creation time (as a datetime) of the file specified by name.
        The datetime will be timezone-aware if USE_TZ=True.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a get_created_time() method"
        )

    def get_modified_time(self, name):
        """
        Return the last modified time (as a datetime) of the file specified by
        name. The datetime will be timezone-aware if USE_TZ=True.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a get_modified_time() method"
        )
