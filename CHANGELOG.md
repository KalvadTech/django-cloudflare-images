## 1.0.0

### Features

 * Added a `CloudflareImageIDField` which allows you to upload files on the client side thanks to Cloudflare's Direct Creator Upload feature

## 0.6.0

### Features

 * Added timeout on Cloudflare's API requests, can be customized through `CLOUDFLARE_IMAGES_API_TIMEOUT`. Thanks to @mschfh

## 0.5.3

### Misc

 * Updated tests and documentation for Django 5 support

## 0.5.2

### Misc

 * Updated tests and documentation for Django 4.2 support (new `STORAGES` setting)

## 0.5.1

### Misc

 * Using `pyproject.toml` to standardize builds. It will provide a wheel package by default and therefore get rid of the warning from pip 23.y.z

## 0.5.0

### Features

 * Added support for the `size` Storage subclass

## 0.4.1

### Misc

 * Set the minimum requirements for `Django` to 3.0

## 0.4.0

### Features

 * Added support for global custom variant (to override default "public")

### Bugfix

 * Fixed a rare bug where Cloudflare would return a 502 timeout (HTML page, not JSON) during an upload and the service would explode when trying to parse json

## 0.3.1

### Misc

 * Set the minimum requirements for `requests` to 2.20.0 (latest secure release to date)

## 0.3.0

### Features

 * Added support for custom domain name when serving images

## 0.2.0

### Features

 * Added support for variants at the field level

## 0.1.0

### Features

 * First release
