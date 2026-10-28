"""
Contains the config for the library
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_SIGNED_URL_TTL = 60 * 60 * 24


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
        it is therefore highly recommended to implement your own.
        """
        return (
            settings.CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT
            if hasattr(settings, "CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT")
            else "/ext/cloudflare_images/api"
        )

    @property
    def signing_key(self) -> str | None:
        """
        Returns the setting CLOUDFLARE_IMAGES_SIGNING_KEY if available
        """
        return getattr(settings, "CLOUDFLARE_IMAGES_SIGNING_KEY", None) or None

    @property
    def signed_url_ttl(self) -> int:
        """
        Returns the lifetime of signed URLs in seconds, 24 hours by default
        """
        ttl = getattr(
            settings, "CLOUDFLARE_IMAGES_SIGNED_URL_TTL", DEFAULT_SIGNED_URL_TTL
        )

        try:
            ttl = int(ttl)
        except (TypeError, ValueError) as exc:
            raise ImproperlyConfigured(
                "CLOUDFLARE_IMAGES_SIGNED_URL_TTL must be a positive integer."
            ) from exc

        if ttl <= 0:
            raise ImproperlyConfigured(
                "CLOUDFLARE_IMAGES_SIGNED_URL_TTL must be a positive integer."
            )

        return ttl
