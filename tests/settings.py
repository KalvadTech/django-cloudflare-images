INSTALLED_APPS = ("images",)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
SECRET_KEY = "top_secret"

CLOUDFLARE_IMAGES_ACCOUNT_ID = "account_id"
CLOUDFLARE_IMAGES_API_TOKEN = "api_token"
CLOUDFLARE_IMAGES_ACCOUNT_HASH = "account_hash"
