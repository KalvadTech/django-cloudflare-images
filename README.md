# django-cloudflare-images

This is a Django library to add support to Cloudflare Images to the ImageField.

## Installation

```sh
pip install django-cloudflare-images
```

## Setup

You need to add the following your settings.py:

```python
DEFAULT_FILE_STORAGE = "images.storage.CloudflareImageStorage"
CLOUDFLARE_IMAGES_ACCOUNT_ID = "XXX"
CLOUDFLARE_IMAGES_API_TOKEN = "YYY"

```

## Development

Packaging:

```sh
python setup.py develop
```

Tests:

```sh
DJANGO_SETTINGS_MODULE=tests.settings django-admin test
```
