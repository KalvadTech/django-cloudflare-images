# django-cloudflare-images

A Django integration for Cloudflare Images, providing a storage backend, model
fields, and a Direct Creator Upload widget.

It supports:

 * Django 3
 * Django 4
 * Django 5
 * Django 6

## Installation

```sh
pip install django-cloudflare-images
```

Python 3.10 or later is required.

## Setup

Add your Cloudflare Images credentials to `settings.py`:

```python
CLOUDFLARE_IMAGES_ACCOUNT_ID = "XXX"
CLOUDFLARE_IMAGES_API_TOKEN = "YYY"
CLOUDFLARE_IMAGES_ACCOUNT_HASH = "ZZZ"
```

Then configure the storage backend.

For Django 4.2+:

```python
STORAGES = {
    "default": {
        "BACKEND": "cloudflare_images.storage.CloudflareImagesStorage",
    },
}
```

For older Django versions:

```python
DEFAULT_FILE_STORAGE = "cloudflare_images.storage.CloudflareImagesStorage"
```

### Optional settings

| Setting | Default | Description |
| --- | --- | --- |
| `CLOUDFLARE_IMAGES_DOMAIN` | `None` | Custom domain used to serve images. |
| `CLOUDFLARE_IMAGES_VARIANT` | `"public"` | Default variant used to serve images. |
| `CLOUDFLARE_IMAGES_API_TIMEOUT` | `60` | Timeout for Cloudflare API requests, in seconds. |
| `CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT` | `"/ext/cloudflare_images/api"` | Endpoint used to retrieve Direct Creator Upload URLs. |
| `CLOUDFLARE_IMAGES_SIGNING_KEY` | `None` | Signing key used to serve private images. |
| `CLOUDFLARE_IMAGES_SIGNED_URL_TTL` | `86400` | Lifetime of signed URLs, in seconds. |

## Usage

### Per-field variants

To use a specific variant for a field, replace `ImageField` with
`CloudflareImagesField`:

```python
from django.db import models

from cloudflare_images.field import CloudflareImagesField


class MyModel(models.Model):
    image = CloudflareImagesField(variant="custom")
```

You will need to generate a migration after swapping the fields. No SQL is
applied; you can verify this with `sqlmigrate <app> <migration>`.

### Checking if an image exists

Use the storage's `exists()` method:

```python
from django.core.files.storage import default_storage

if default_storage.exists("image_id"):
    print("Image exists!")
else:
    print("Image not found")
```

**Note:** This makes an HTTP API call to Cloudflare on every invocation. If you
check many images, consider adding your own caching layer.

## Private Images and Signed URLs

Cloudflare Images can serve private images that require a signed URL. Add your
signing key from the Cloudflare dashboard (Images > Keys):

```python
CLOUDFLARE_IMAGES_SIGNING_KEY = "..."
```

### Server-side uploads

Use a storage configured with `require_signed_urls=True` and attach it to your
field:

```python
from django.db import models

from cloudflare_images.field import CloudflareImagesField
from cloudflare_images.storage import CloudflareImagesStorage


private_storage = CloudflareImagesStorage(require_signed_urls=True)


class Document(models.Model):
    image = CloudflareImagesField(storage=private_storage)
```

With this storage:

- uploads are created with `requireSignedURLs=true`;
- `document.image.url` returns a signed URL;
- `storage.open()` and `storage.size()` use signed URLs internally.

If the whole project uses private images, you can configure the default storage
instead of attaching a storage to each field (Django 4.2+):

```python
STORAGES = {
    "default": {
        "BACKEND": "cloudflare_images.storage.CloudflareImagesStorage",
        "OPTIONS": {"require_signed_urls": True},
    },
}
```

### Explicit signed URLs

You can generate a signed URL explicitly, with a custom lifetime in seconds:

```python
url = document.image.signed_url(expires_in=300)

# Or, without a field:
url = private_storage.signed_url("image_id", "public", expires_in=300)
```

If `expires_in` is omitted, `CLOUDFLARE_IMAGES_SIGNED_URL_TTL` is used (24 hours
by default).

### Caveats

- Generate signed URLs when rendering; do not store them, as they expire.
- Rotating the signing key invalidates all existing signed URLs.
- Cloudflare's custom paths feature does not support private images.
- Images uploaded with a custom ID cannot be made private with signed URLs.

## Direct Creator Upload

Cloudflare's Direct Creator Upload lets users upload images directly to
Cloudflare without exposing your API token.

### Setup

Add the app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "cloudflare_images",
]
```

Add the endpoint to your URL configuration:

```python
from cloudflare_images.views import WidgetAPI

# Add this inside your urlpatterns:
path("ext/cloudflare_images/api", WidgetAPI.as_view(), name="widget-api"),
```

**Note:** The provided endpoint has no security and should be treated as an
example. It is strongly recommended to implement your own endpoint. See
[cloudflare_images/views.py](https://github.com/KalvadTech/django-cloudflare-images/blob/main/cloudflare_images/views.py)
for the base implementation.

To point the widget at a custom endpoint:

```python
CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT = "/my/endpoint/api"
```

### Model

Replace your image field with `CloudflareImageIDField`:

```python
from cloudflare_images.field import CloudflareImageIDField

# In your model:
image = CloudflareImageIDField(variant="custom")
```

Generate a migration after changing the field. This field is not backward
compatible with `CloudflareImagesField`, particularly for `.url`; use a helper
to generate URLs.

### Template

Load the widget assets from your form:

```html
{{ form.media.js }}
{{ form.media.css }}
```

### Private uploads

To create private images, subclass the provided view and request private
uploads:

```python
from cloudflare_images.views import WidgetAPI


class PrivateWidgetAPI(WidgetAPI):
    def get_upload_options(self, request):
        return {"require_signed_urls": True}
```

Use this view in your URL configuration, and enable signed previews in the form:

```python
from django import forms

from cloudflare_images.widget import CloudflareImagesWidget


class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ["image"]
        widgets = {"image": CloudflareImagesWidget(signed=True)}
```

After a private upload, the widget displays the image ID without a link until
the form is saved and the page is rendered again.

### Generating URLs

`CloudflareImageIDField` stores only the image ID, so use the service to build
the URL:

```python
from cloudflare_images.service import CloudflareImagesService


@property
def image_url(self) -> str | None:
    if not self.image:
        return None
    return CloudflareImagesService().get_url(self.image, "public")
```

For private images, use `get_signed_url()` instead:

```python
return CloudflareImagesService().get_signed_url(self.image, "public")
```

For basic troubleshooting, check your browser's console or open an issue.

## Contributing

See [CONTRIBUTING.md](https://github.com/KalvadTech/django-cloudflare-images/blob/main/CONTRIBUTING.md)
for development setup, tests, and packaging.
