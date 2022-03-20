"""
Contains the Cloudflare Image storage which is supposed to replace Django's
default Storage (see README.md)
Django's default storage class: https://github.com/django/django/blob/main/django/core/files/storage.py
"""

import uuid
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from images.service import CloudflareImagesService

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
        TODO
        """
        raise NotImplementedError("Oops !")

    def _save(self, name, content):
        """
        Tries to upload the file and return its name
        """
        new_name = self.generate_filename(name)
        file = ContentFile(content, name=name)
        return self.service.upload(file)

    def get_valid_name(self, name):
        """
        TODO
        """
        return name

    def get_available_name(self, name, max_length=None):
        """
        TODO
        """
        raise NotImplementedError("Oops !")

    def generate_filename(self, filename):
        """
        TODO: this probably will be a problem with the path
        """
        extension = filename.split('.').pop()
        filename = str(uuid.uuidv4())
        return "{}.{}".format(filename, extension)

    def path(self, name):
        """
        TODO
        """
        raise NotImplementedError("Oops !")

    def delete(self, name):
        """
        Delete the specified file from the storage system.
        """
        raise NotImplementedError(
            "subclasses of Storage must provide a delete() method"
        )

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
        """
        raise NotImplementedError("subclasses of Storage must provide a url() method")

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
