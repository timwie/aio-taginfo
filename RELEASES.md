# Release Notes
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased
* **Breaking**: Rename `TagInfo*Error` classes to `Taginfo*Error`
* Implement `/api/v4/key/chronology` endpoint

## [0.3.0] – 2024-04-27
* Implement `/api/4/tags/popular` endpoint
* Relax `aiohttp` requirement to `^3.9` (from `~3.9.0b0`)
* Relax `pydantic` requirement to `^2.4` (from `~2.4`)
* Add `py.typed` to make the package PEP 561 compatible

## [0.2.0] – 2023-10-20
* **Breaking**: Drop Python 3.9 support
* **Breaking**: Increased `aiohttp` requirement to `~3.9.0b0`
* Add Python 3.12 support
* Enable `speedups` extra of `aiohttp`

## [0.1.0] – 2023-09-27
* The Python versions supported by this release are 3.9-3.11.
* A few endpoints are implemented as proof-of-concept:
  * `/api/4/key/distribution/nodes`
  * `/api/4/key/overview`
  * `/api/4/key/prevalent_values`
  * `/api/4/key/similar`
  * `/api/4/site/config/geodistribution`

[0.1.0]: https://github.com/timwie/aio-taginfo/releases/tag/v0.1.0
[0.2.0]: https://github.com/timwie/aio-taginfo/releases/tag/v0.2.0
[0.3.0]: https://github.com/timwie/aio-taginfo/releases/tag/v0.3.0
