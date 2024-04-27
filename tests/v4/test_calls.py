from pathlib import Path

from aio_taginfo import (
    key_distribution_nodes,
    key_overview,
    key_prevalent_values,
    key_similar,
    site_config_geodistribution,
    tags_popular,
)
from aio_taginfo.api.v4 import SortOrder
from aio_taginfo.api.v4.key.similar import SimilarKeySorting
from aio_taginfo.api.v4.tags.popular import PopularTagSorting
from aio_taginfo.error import TagInfoCallError, TagInfoValidationError, TagInfoValueError

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses


@pytest.mark.asyncio
async def test_key_distribution_nodes():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_distribtion_nodes_amenity.png"

    with open(data_file, mode="rb") as f:
        image_bytes = f.read()

    url = "https://taginfo.openstreetmap.org/api/4/key/distribution/nodes?key=amenity"

    with aioresponses() as m:
        m.get(
            url=url,
            body=image_bytes,
            status=200,
            content_type="image/png",
        )
        response = await key_distribution_nodes(key="amenity")
        assert response.data == image_bytes

        m.get(
            url=url,
            body=image_bytes,
            status=400,
            content_type="application/json",
        )
        with pytest.raises(TagInfoCallError):
            await key_distribution_nodes(key="amenity")

        m.get(
            url=url,
            body=b"nonsense",
            status=200,
            content_type="image/png",
        )
        with pytest.raises(TagInfoValidationError):
            await key_distribution_nodes(key="amenity")


@pytest.mark.asyncio
async def test_key_overview():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_overview_amenity.json"
    response_str = data_file.read_text()

    url = "https://taginfo.openstreetmap.org/api/4/key/overview?key=amenity"

    async with ClientSession() as session:
        with aioresponses() as m:
            m.get(
                url=url,
                body=response_str,
                status=200,
                content_type="application/json",
            )
            response = await key_overview(key="amenity", session=session)
            assert response.data.key == "amenity"

            m.get(
                url=url,
                body=response_str,
                status=400,
                content_type="application/json",
            )
            with pytest.raises(TagInfoCallError):
                await key_overview(key="amenity", session=session)

            m.get(
                url=url,
                payload={},
                status=200,
                content_type="application/json",
            )
            with pytest.raises(TagInfoValidationError):
                await key_overview(key="amenity", session=session)


@pytest.mark.asyncio
async def test_site_config_geodistribution():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "site_config_geodistribution.json"
    response_str = data_file.read_text()

    url = "https://taginfo.openstreetmap.org/api/4/site/config/geodistribution"

    async with ClientSession() as session:
        with aioresponses() as m:
            m.get(
                url=url,
                body=response_str,
                status=200,
                content_type="application/json",
            )
            response = await site_config_geodistribution(session=session)
            assert response.width == 360


@pytest.mark.asyncio
async def test_key_prevalent_values():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_prevalent_values_highway.json"
    response_str = data_file.read_text()

    url = "https://taginfo.openstreetmap.org/api/4/key/prevalent_values?key=highway&filter=all&min_fraction=0.01"

    with aioresponses() as m:
        m.get(
            url=url,
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await key_prevalent_values(key="highway")
        assert response.data[0].count == 65032833

        with pytest.raises(TagInfoValueError):
            await key_prevalent_values(key="highway", min_fraction=0.001)

        with pytest.raises(TagInfoValueError):
            await key_prevalent_values(key="    ")

        with pytest.raises(TagInfoValueError):
            await key_prevalent_values(key="highway", filter="yes")


@pytest.mark.asyncio
async def test_key_similar():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_similar_highway.json"
    response_str = data_file.read_text()

    base_url = "https://taginfo.openstreetmap.org/api/4/key/similar"

    with aioresponses() as m:
        m.get(
            url=f"{base_url}?key=highway&page=1&rp=0&sortname=other_key&sortorder=asc",
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await key_similar(key="highway")
        assert response.data[0].other_key == "FIXME:highway"

        m.get(
            url=f"{base_url}?key=highway&page=2&query=fixme&rp=3&sortname=similarity&sortorder=desc",
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await key_similar(
            key="highway",
            query="fixme",
            sortname=SimilarKeySorting.SIMILARITY,
            sortorder=SortOrder.DESC,
            page=2,
            rp=3,
        )
        assert response.data[0].other_key == "FIXME:highway"

    with pytest.raises(TagInfoValueError):
        await key_similar(key="highway", query="   ")

    with pytest.raises(TagInfoValueError):
        await key_similar(key="highway", sortname="something else")

    with pytest.raises(TagInfoValueError):
        await key_similar(key="highway", sortorder="something else")

    with pytest.raises(TagInfoValueError):
        await key_similar(key="highway", page=-1)

    with pytest.raises(TagInfoValueError):
        await key_similar(key="highway", rp=-1)


@pytest.mark.asyncio
async def test_tags_popular():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "tags_popular.json"
    response_str = data_file.read_text()

    base_url = "https://taginfo.openstreetmap.org/api/4/tags/popular"

    with aioresponses() as m:
        m.get(
            url=f"{base_url}?page=1&rp=0&sortname=count_all&sortorder=desc",
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await tags_popular()
        assert response.data[0].key == "building"

        m.get(
            url=f"{base_url}?page=2&query=fixme&rp=3&sortname=tag&sortorder=asc",
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await tags_popular(
            query="fixme",
            sortname=PopularTagSorting.TAG,
            sortorder=SortOrder.ASC,
            page=2,
            rp=3,
        )
        assert response.data[0].key == "building"

    with pytest.raises(TagInfoValueError):
        await tags_popular(query="   ")

    with pytest.raises(TagInfoValueError):
        await tags_popular(sortname="something else")

    with pytest.raises(TagInfoValueError):
        await tags_popular(sortorder="something else")

    with pytest.raises(TagInfoValueError):
        await tags_popular(page=-1)

    with pytest.raises(TagInfoValueError):
        await tags_popular(rp=-1)
