"""
Contains the Cloudflare Image service which handles the API exchanges
"""

import hashlib
import hmac
import time
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import requests
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File

from cloudflare_images.config import Config


class ApiException(Exception):
    """
    Exception raised by Cloudflare Images API
    """

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class CloudflareImagesService:
    """
    API client for Cloudflare Images
    """

    def __init__(self) -> None:
        """
        Loads the configuration
        """
        self.config = Config()

    def upload(self, file: File, *, require_signed_urls: bool = False) -> str:
        """
        Uploads a file and returns its name, otherwise raises an exception
        """
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.config.account_id}/images/v1"

        headers = {"Authorization": f"Bearer {self.config.api_token}"}

        files = {"file": file}
        data = {"requireSignedURLs": "true"} if require_signed_urls else None

        response = requests.post(
            url,
            headers=headers,
            timeout=self.config.api_timeout,
            files=files,
            data=data,
        )

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(str(response.content), status_code=status_code)

        response_body = response.json()
        return response_body.get("result").get("id")

    def get_url(self, name: str, variant: str) -> str:
        """
        Returns the public URL for the given image ID
        """
        if self.config.domain:
            return f"https://{self.config.domain}/cdn-cgi/imagedelivery/{self.config.account_hash}/{name}/{variant}"

        return f"https://imagedelivery.net/{self.config.account_hash}/{name}/{variant}"

    def get_signed_url(
        self, name: str, variant: str, expires_in: int | None = None
    ) -> str:
        """
        Returns a signed URL for the given image ID and variant.
        The URL is valid for `expires_in` seconds, or the configured
        CLOUDFLARE_IMAGES_SIGNED_URL_TTL if not provided.
        """
        signing_key = self.config.signing_key
        if not signing_key:
            raise ImproperlyConfigured(
                "CLOUDFLARE_IMAGES_SIGNING_KEY must be set to generate signed URLs."
            )

        ttl = int(self.config.signed_url_ttl if expires_in is None else expires_in)
        if ttl <= 0:
            raise ValueError("expires_in must be a positive number of seconds")

        expiry = int(time.time()) + ttl
        url = self.get_url(name, variant)
        parts = urlsplit(url)

        query = f"exp={expiry}"
        if parts.query:
            query = f"{parts.query}&{query}"

        string_to_sign = f"{parts.path}?{query}"
        signature = hmac.new(
            signing_key.encode(),
            string_to_sign.encode(),
            hashlib.sha256,
        ).hexdigest()

        return urlunsplit(
            (
                parts.scheme,
                parts.netloc,
                parts.path,
                f"{query}&sig={signature}",
                "",
            )
        )

    def open(
        self,
        name: str,
        variant: str | None = None,
        *,
        signed: bool = False,
    ) -> bytes:
        """
        Retrieves a file and returns its content, otherwise raises an exception
        """

        if signed:
            url = self.get_signed_url(name, variant or self.config.variant)
        else:
            url = self.get_url(name, variant or self.config.variant)

        response = requests.get(url, timeout=self.config.api_timeout)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(str(response.content), status_code=status_code)

        return response.content

    def delete(self, name: str) -> None:
        """
        Deletes a file if it exists, otherwise raise an exception
        """

        url = f"https://api.cloudflare.com/client/v4/accounts/{self.config.account_id}/images/v1/{name}"

        headers = {"Authorization": f"Bearer {self.config.api_token}"}

        response = requests.delete(
            url, timeout=self.config.api_timeout, headers=headers
        )

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(str(response.text), status_code=status_code)

    def get_image_details(self, name: str) -> dict[str, Any]:
        """
        Fetches image details from Cloudflare API
        Returns the result dict on success
        Raises ApiException on any error (including 404)
        """

        url = f"https://api.cloudflare.com/client/v4/accounts/{self.config.account_id}/images/v1/{name}"

        headers = {"Authorization": f"Bearer {self.config.api_token}"}

        response = requests.get(url, timeout=self.config.api_timeout, headers=headers)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(response.text, status_code=status_code)

        return response.json().get("result")

    def get_one_time_upload_url(
        self, *, require_signed_urls: bool = False
    ) -> dict[str, Any]:
        """
        Direct Creator Upload endpoint
        Generates a one time upload URL
        """
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.config.account_id}/images/v2/direct_upload"

        headers = {"Authorization": f"Bearer {self.config.api_token}"}

        files = {"requireSignedURLs": (None, "true")} if require_signed_urls else None

        response = requests.post(
            url, headers=headers, timeout=self.config.api_timeout, files=files
        )

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(response.text, status_code=status_code)

        return response.json()
