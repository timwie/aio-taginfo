"""
Typed async client for the taginfo API.

The ``aio_taginfo.api`` module structure is derived from the endpoint path segments.
All the calls are re-exported here at the top level for convenience.

**Jump to:**
* ``aio_taginfo.api.v4.key.distribution.nodes``
* ``aio_taginfo.api.v4.key.overview``
* ``aio_taginfo.api.v4.key.prevalent_values``
* ``aio_taginfo.api.v4.key.similar``
* ``aio_taginfo.api.v4.site.config.geodistribution``
* ``aio_taginfo.api.v4.tags.popular``
"""

import importlib.metadata


__version__: str = importlib.metadata.version("aio-taginfo")

# we add this to all modules for pdoc;
# see https://pdoc.dev/docs/pdoc.html#use-numpydoc-or-google-docstrings
__docformat__ = "google"

# we also use __all__ in all modules for pdoc; this lets us control the order
__all__ = (
    "api",  # pyright: ignore[reportUnsupportedDunderAll]
    "error",  # pyright: ignore[reportUnsupportedDunderAll]
    "key_distribution_nodes",
    "key_overview",
    "key_prevalent_values",
    "key_similar",
    "site_config_geodistribution",
    "tags_popular",
    "TagInfoError",
)

from aio_taginfo.api.v4.key.distribution.nodes import call as key_distribution_nodes
from aio_taginfo.api.v4.key.overview import call as key_overview
from aio_taginfo.api.v4.key.prevalent_values import call as key_prevalent_values
from aio_taginfo.api.v4.key.similar import call as key_similar
from aio_taginfo.api.v4.site.config.geodistribution import call as site_config_geodistribution
from aio_taginfo.api.v4.tags.popular import call as tags_popular
from aio_taginfo.error import TagInfoError
