"""
Contains the config for the library
"""

from django.conf import settings


class Config:
    """
    Configuration taken from Django's settings
    """

    @property
    def account_id(self) -> str | None:
        """
        Returns the setting CLOUDFLARE_IMAGES_ACCOUNT_ID
        """
        return settings.CLOUDFLARE_IMAGES_ACCOUNT_ID

    @property
    def api_token(self) -> str | None:
        """
        Returns the setting CLOUDFLARE_IMAGES_API_TOKEN
        """
        return settings.CLOUDFLARE_IMAGES_API_TOKEN

    @property
    def account_hash(self) -> str | None:
        """
        Returns the setting CLOUDFLARE_IMAGES_ACCOUNT_HASH
        """
        return settings.CLOUDFLARE_IMAGES_ACCOUNT_HASH

    @property
    def domain(self) -> str | None:
        """
        Returns the setting CLOUDFLARE_IMAGES_DOMAIN if available
        """
        return (
            settings.CLOUDFLARE_IMAGES_DOMAIN
            if hasattr(settings, "CLOUDFLARE_IMAGES_DOMAIN")
            else None
        )

    @property
    def variant(self) -> str:
        """
        Returns the default variant
        """
        return (
            settings.CLOUDFLARE_IMAGES_VARIANT
            if hasattr(settings, "CLOUDFLARE_IMAGES_VARIANT")
            else "public"
        )

    @property
    def api_timeout(self) -> int:
        """
        Returns the timeout if set, else a default of 60 seconds
        """
        return (
            settings.CLOUDFLARE_IMAGES_API_TIMEOUT
            if hasattr(settings, "CLOUDFLARE_IMAGES_API_TIMEOUT")
            else 60
        )

    @property
    def upload_endpoint(self) -> str:
        """
        Returns the endpoint used to retrieve the upload URL from cloudflare
        This library provides a default one which has NO SECURITY,
        is it therefore highly recommended to implement your own.
        """
        return (
            settings.CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT
            if hasattr(settings, "CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT")
            else "/ext/cloudflare_images/api"
        )
