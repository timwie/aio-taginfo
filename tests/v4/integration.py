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


def _log_response(resp: Any) -> None:
    if isinstance(resp, Response) and isinstance(resp.data, list):
        resp = replace(resp, data=resp.data[:_MAX_ITEMS_LOGGED])

    for line in pformat(resp).splitlines():
        logger.info(line)


async def _call_all_endpoints() -> None:
    headers = {"User-Agent": "Automated integration test (https://github.com/timwie/aio-taginfo)"}

    async with aiohttp.ClientSession(headers=headers) as session:
        logger.info("key_chronology")  # TODO: logging should be integrated into the library
        resp = await key_chronology(key="highway", session=session)
        _log_response(resp)

        logger.info("key_combinations")  # TODO: logging should be integrated into the library
        resp = await key_combinations(key="highway", session=session)
        _log_response(resp)

        logger.info("key_distribution_nodes")  # TODO: logging should be integrated into the library
        resp = await key_distribution_nodes(key="amenity", session=session)
        _log_response(resp)

        logger.info("key_distribution_ways")  # TODO: logging should be integrated into the library
        resp = await key_distribution_ways(key="highway", session=session)
        _log_response(resp)

        logger.info("key_overview")  # TODO: logging should be integrated into the library
        resp = await key_overview(key="amenity", session=session)
        _log_response(resp)

        logger.info("key_prevalent_values")  # TODO: logging should be integrated into the library
        resp = await key_prevalent_values(
            key="highway", min_fraction=0.01, filter=ObjectType.WAYS, session=session
        )
        _log_response(resp)

        logger.info("key_projects")  # TODO: logging should be integrated into the library
        resp = await key_projects(key="highway", session=session)
        _log_response(resp)

        logger.info("key_similar")  # TODO: logging should be integrated into the library
        resp = await key_similar(
            key="highway",
            session=session,
            sortname=SimilarKeySorting.SIMILARITY,
            sortorder=SortOrder.DESC,
            rp=10,
            page=2,
        )
        _log_response(resp)

        logger.info("key_stats")  # TODO: logging should be integrated into the library
        resp = await key_stats(key="amenity", session=session)
        _log_response(resp)

        logger.info("relation_projects")  # TODO: logging should be integrated into the library
        resp = await relation_projects(rtype="route", session=session)
        _log_response(resp)

        logger.info(
            "site_config_geodistribution"
        )  # TODO: logging should be integrated into the library
        resp = await site_config_geodistribution(session=session)
        _log_response(resp)

        logger.info("tag_projects")  # TODO: logging should be integrated into the library
        resp = await tag_projects(key="highway", value="residential", session=session)
        _log_response(resp)

        logger.info("tags_popular")  # TODO: logging should be integrated into the library
        resp = await tags_popular(
            query="addr",
            sortname=PopularTagSorting.TAG,
            sortorder=SortOrder.ASC,
            rp=10,
            page=2,
            session=session,
        )
        _log_response(resp)


asyncio.run(_call_all_endpoints())
