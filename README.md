# django-cloudflare-images

This is a Django library to add support to Cloudflare Images to the ImageField.

## Installation

```sh
pip install django-cloudflare-images
```

## Setup

You need to add the following your settings.py:

```python
DEFAULT_FILE_STORAGE = "cloudflare_images.storage.CloudflareImageStorage"
CLOUDFLARE_IMAGES_ACCOUNT_ID = "XXX"
CLOUDFLARE_IMAGES_API_TOKEN = "YYY"
CLOUDFLARE_IMAGES_ACCOUNT_HASH = "ZZZ"
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
make format
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

## TODO

This is a list of non exhaustive list of things I would like to add to the project:

 * Ability to pass down variants instead of hardcoding "public"
 * Support custom domains (optional)
 * Functional tests with real credentials (to be passed in the environment)
