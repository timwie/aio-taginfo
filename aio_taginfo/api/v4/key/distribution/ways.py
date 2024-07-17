"""`/api/4/key/distribution/ways` endpoint."""

from aio_taginfo.api.v4 import PngResponse
from aio_taginfo.api.v4._internal import StringParam, api_get_png, api_params

from aiohttp import ClientSession
from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class _Params:
    key: StringParam = Field(repr=True)


async def call(key: str, session: ClientSession | None = None) -> PngResponse:
    """
    Get map with distribution of this key in the database (ways only).

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_key_distribution_ways

    Args:
        key: tag key
        session: request client session

    Raises:
        TaginfoError
    """
    params = api_params(_Params, key=key)
    return await api_get_png(
        path="/api/4/key/distribution/ways",
        session=session,
        params=params,
    )


__docformat__ = "google"
