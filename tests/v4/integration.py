import asyncio
from dataclasses import replace
from pprint import pformat
from typing import Any

from aio_taginfo import (
    key_chronology,
    key_combinations,
    key_distribution_nodes,
    key_distribution_ways,
    key_overview,
    key_prevalent_values,
    key_projects,
    key_similar,
    key_stats,
    relation_projects,
    site_config_geodistribution,
    tag_projects,
    tags_popular,
)
from aio_taginfo.api.v4 import ObjectType, Response, SortOrder
from aio_taginfo.api.v4.key.similar import SimilarKeySorting
from aio_taginfo.api.v4.tags.popular import PopularTagSorting

import aiohttp
from loguru import logger


_MAX_ITEMS_LOGGED = 10  # keep the log reasonably short


# TODO: add more than one call per endpoint
_CALLS = [
    (key_chronology, dict(key="highway")),
    (key_combinations, dict(key="highway")),
    (key_distribution_nodes, dict(key="amenity")),
    (key_distribution_ways, dict(key="highway")),
    (key_overview, dict(key="amenity")),
    (key_prevalent_values, dict(key="highway", min_fraction=0.01, filter=ObjectType.WAYS)),
    (key_projects, dict(key="highway")),
    (
        key_similar,
        dict(
            key="highway",
            sortname=SimilarKeySorting.SIMILARITY,
            sortorder=SortOrder.DESC,
            rp=10,
            page=2,
        ),
    ),
    (key_stats, dict(key="amenity")),
    (relation_projects, dict(rtype="route")),
    (site_config_geodistribution, dict()),
    (tag_projects, dict(key="highway", value="residential")),
    (
        tags_popular,
        dict(query="addr", sortname=PopularTagSorting.TAG, sortorder=SortOrder.ASC, rp=10, page=2),
    ),
]


def _log_response(resp: Any) -> None:
    if isinstance(resp, Response) and isinstance(resp.data, list):
        resp = replace(resp, data=resp.data[:_MAX_ITEMS_LOGGED])

    for line in pformat(resp).splitlines():
        logger.info(line)


async def _call_all_endpoints() -> None:
    headers = {"User-Agent": "Automated integration test (https://github.com/timwie/aio-taginfo)"}

    async with aiohttp.ClientSession(headers=headers) as session:
        for func, kwargs in _CALLS:
            resp = await func(session=session, **kwargs)
            _log_response(resp)


asyncio.run(_call_all_endpoints())
