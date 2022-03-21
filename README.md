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

Installing for development:

```sh
make install
```

Cleaning the installation:

```sh
make clean
```

Format the code:

```sh
make black
```

Running all tests:

```sh
make test
```

Setup.py commands:

```sh
make package-develop
make package-build
make package-install
make package-sdist
```
