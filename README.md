# django-cloudflare-images

This is a Django library to add support to Cloudflare Images to the ImageField.

It supports:

 * Django 3
 * Django 4
 * Django 5

## Installation

```sh
pip install django-cloudflare-images
```

## Setup

You need to add the following your settings.py:


1. If you are running Django 4.2+:

```python
STORAGES = {"default": {"BACKEND": "cloudflare_images.storage.CloudflareImagesStorage"}}
```

2. Else:


```python
DEFAULT_FILE_STORAGE = "cloudflare_images.storage.CloudflareImagesStorage"
```

And then add the remaining of the configuration:

```python
CLOUDFLARE_IMAGES_ACCOUNT_ID = "XXX"
CLOUDFLARE_IMAGES_API_TOKEN = "YYY"
CLOUDFLARE_IMAGES_ACCOUNT_HASH = "ZZZ"
```

If you wish to use a default variant for a specific field you need to change your `ImageField` to a `CloudflareImagesField` see example below:

```python
from cloudflare_images.field import CloudflareImagesField
from django.db import models

class MyModel(models.Model):
    image = CloudflareImagesField(variant="custom")


```

Please note that you will need to migrate your model(s) once you swapped the field(s). No SQL will actually be applied (you can check by running `sqlmigrate <module> <number>`).

If you wish to use a custom domain to serve your images you need to add the following to your settings.py:

```python
CLOUDFLARE_IMAGES_DOMAIN = "example.com"
```

If you wish to use a default variant other than "public" to serve your images you need to add the following to your settings.py:

```python
CLOUDFLARE_IMAGES_VARIANT = "custom"
```

If you wish to override the default timeout of 60 seconds for API requests, you need to add the following to your settings.py:

```python
CLOUDFLARE_IMAGES_API_TIMEOUT = 120
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

Check the code (for linting errors):

```sh
make check
```

Check the code (python type checker):

```sh
make static-check
```

Running all tests:

```sh
make test
```

Create a sdist+bdist package in dist/:

```sh
make package
```
