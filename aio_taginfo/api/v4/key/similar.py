"""`/api/4/key/similar` endpoint."""

from enum import Enum

from aio_taginfo.api.v4 import Response, SortOrder
from aio_taginfo.api.v4._internal import NonEmptyString, api_get_json, api_params

from aiohttp import ClientSession
from pydantic import Field
from pydantic.dataclasses import dataclass


__all__ = (
    "call",
    "SimilarKey",
    "SimilarKeySorting",
)


@dataclass(kw_only=True, frozen=True)
class SimilarKey:
    """
    Result of a key that is similar to a given key.

    Attributes:
        other_key: other key
        count_all: number of objects that have the other key
        similarity: integer measuring the similarity of the two keys (smaller is more similar)
    """

    other_key: str = Field(min_length=1, repr=True)
    count_all: int = Field(ge=0, repr=True)
    similarity: int = Field(ge=0, repr=True)


class SimilarKeySorting(str, Enum):
    """Sort options for similar keys."""

    OTHER_KEY = "other_key"
    COUNT_ALL = "count_all"
    SIMILARITY = "similarity"


@dataclass(kw_only=True, frozen=True)
class _Params:
    key: NonEmptyString = Field(repr=True)
    query: NonEmptyString | None = Field(repr=True)
    sortname: SimilarKeySorting = Field(repr=True)
    sortorder: SortOrder = Field(repr=True)
    page: int = Field(gt=0, repr=True)
    rp: int = Field(ge=0, repr=True)


async def call(
    key: str,
    query: str | None = None,
    sortname: SimilarKeySorting = SimilarKeySorting.OTHER_KEY,
    sortorder: SortOrder = SortOrder.ASC,
    page: int = 1,
    rp: int = 0,
    session: ClientSession | None = None,
) -> Response[list[SimilarKey]]:
    """
    Find keys that are similar to a given key.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_key_similar

    Args:
        key: tag key
        query: only show results where the ``other_key`` matches this query (substring match)
        sortname: what field to sort by
        sortorder: sort order
        page: page number (starting at 1)
        rp: results per page
        session: request client session

    Raises:
        TaginfoError
    """
    params = api_params(
        _Params, key=key, query=query, sortname=sortname, sortorder=sortorder, page=page, rp=rp
    )
    return await api_get_json(
        path="key/similar",
        cls=Response[list[SimilarKey]],
        session=session,
        params=params,
    )


__docformat__ = "google"
