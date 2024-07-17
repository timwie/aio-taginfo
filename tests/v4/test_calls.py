import datetime
from pathlib import Path

from aio_taginfo import (
    key_chronology,
    key_combinations,
    key_distribution_nodes,
    key_distribution_ways,
    key_overview,
    key_prevalent_values,
    key_similar,
    key_stats,
    site_config_geodistribution,
    tags_popular,
)
from aio_taginfo.api.v4 import ObjectType, SortOrder
from aio_taginfo.api.v4.key.combinations import KeyCombinationSorting
from aio_taginfo.api.v4.key.similar import SimilarKeySorting
from aio_taginfo.api.v4.tags.popular import PopularTagSorting
from aio_taginfo.error import TaginfoCallError, TaginfoValidationError, TaginfoValueError

import pytest
from aioresponses import aioresponses


@pytest.mark.asyncio()
async def test_key_distribution_nodes():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_distribtion_nodes_amenity.png"

    with data_file.open(mode="rb") as f:
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
    _, _ = str(response), repr(response)

    with aioresponses() as m:
        m.get(
            url=url,
            body=image_bytes,
            status=400,
            content_type="application/json",
        )
        with pytest.raises(TaginfoCallError):
            await key_distribution_nodes(key="amenity")

        m.get(
            url=url,
            body=b"nonsense",
            status=200,
            content_type="image/png",
        )
        with pytest.raises(TaginfoValidationError):
            await key_distribution_nodes(key="amenity")


@pytest.mark.asyncio()
async def test_key_distribution_ways():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_distribution_ways_highway.png"

    with data_file.open(mode="rb") as f:
        image_bytes = f.read()

    url = "https://taginfo.openstreetmap.org/api/4/key/distribution/ways?key=highway"

    with aioresponses() as m:
        m.get(
            url=url,
            body=image_bytes,
            status=200,
            content_type="image/png",
        )
        response = await key_distribution_ways(key="highway")

    assert response.data == image_bytes
    _, _ = str(response), repr(response)

    with aioresponses() as m:
        m.get(
            url=url,
            body=image_bytes,
            status=400,
            content_type="application/json",
        )
        with pytest.raises(TaginfoCallError):
            await key_distribution_ways(key="highway")

        m.get(
            url=url,
            body=b"nonsense",
            status=200,
            content_type="image/png",
        )
        with pytest.raises(TaginfoValidationError):
            await key_distribution_ways(key="highway")


@pytest.mark.asyncio()
async def test_key_overview():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_overview_amenity.json"
    response_str = data_file.read_text()

    url = "https://taginfo.openstreetmap.org/api/4/key/overview?key=amenity"

    with aioresponses() as m:
        m.get(
            url=url,
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await key_overview(key="amenity")

    assert response.data.key == "amenity"
    _, _ = str(response), repr(response)

    with aioresponses() as m:
        m.get(
            url=url,
            body=response_str,
            status=400,
            content_type="application/json",
        )
        with pytest.raises(TaginfoCallError):
            await key_overview(key="amenity")

        m.get(
            url=url,
            payload={},
            status=200,
            content_type="application/json",
        )
        with pytest.raises(TaginfoValidationError):
            await key_overview(key="amenity")


@pytest.mark.asyncio()
async def test_site_config_geodistribution():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "site_config_geodistribution.json"
    response_str = data_file.read_text()

    url = "https://taginfo.openstreetmap.org/api/4/site/config/geodistribution"

    with aioresponses() as m:
        m.get(
            url=url,
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await site_config_geodistribution()

    assert response.width == 360
    _, _ = str(response), repr(response)


@pytest.mark.asyncio()
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
    _, _ = str(response), repr(response)

    with pytest.raises(TaginfoValueError):
        await key_prevalent_values(key="highway", min_fraction=0.001)

    with pytest.raises(TaginfoValueError):
        await key_prevalent_values(key="    ")

    with pytest.raises(TaginfoValueError):
        await key_prevalent_values(key="highway", filter="yes")


@pytest.mark.asyncio()
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
    _, _ = str(response), repr(response)

    with aioresponses() as m:
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
    _, _ = str(response), repr(response)

    with pytest.raises(TaginfoValueError):
        await key_similar(key="highway", query="   ")

    with pytest.raises(TaginfoValueError):
        await key_similar(key="highway", sortname="something else")

    with pytest.raises(TaginfoValueError):
        await key_similar(key="highway", sortorder="something else")

    with pytest.raises(TaginfoValueError):
        await key_similar(key="highway", page=-1)

    with pytest.raises(TaginfoValueError):
        await key_similar(key="highway", rp=-1)


@pytest.mark.asyncio()
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
    _, _ = str(response), repr(response)

    with aioresponses() as m:
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
    _, _ = str(response), repr(response)

    with pytest.raises(TaginfoValueError):
        await tags_popular(query="   ")

    with pytest.raises(TaginfoValueError):
        await tags_popular(sortname="something else")

    with pytest.raises(TaginfoValueError):
        await tags_popular(sortorder="something else")

    with pytest.raises(TaginfoValueError):
        await tags_popular(page=-1)

    with pytest.raises(TaginfoValueError):
        await tags_popular(rp=-1)


@pytest.mark.asyncio()
async def test_key_chronology():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_chronology_highway.json"
    response_str = data_file.read_text()

    base_url = "https://taginfo.openstreetmap.org/api/4/key/chronology"

    with aioresponses() as m:
        m.get(
            url=f"{base_url}?key=highway",
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await key_chronology(key="highway")

    assert response.data[0].date == datetime.date(2007, 10, 7)
    _, _ = str(response), repr(response)


@pytest.mark.asyncio()
async def test_key_combinations():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_combinations_highway.json"
    response_str = data_file.read_text()

    base_url = "https://taginfo.openstreetmap.org/api/4/key/combinations"

    with aioresponses() as m:
        m.get(
            url=f"{base_url}?filter=all&key=highway&page=1&rp=0&sortname=together_count&sortorder=desc",
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await key_combinations(key="highway")

    assert response.data[0].together_count == 58128837
    _, _ = str(response), repr(response)

    with aioresponses() as m:
        m.get(
            url=f"{base_url}?filter=ways&key=highway&page=2&query=fixme&rp=10&sortname=from_fraction&sortorder=asc",
            body=response_str,
            status=200,
            content_type="application/json",
        )
        _response = await key_combinations(
            key="highway",
            query="fixme",
            sortname=KeyCombinationSorting.FROM_FRACTION,
            sortorder=SortOrder.ASC,
            filter=ObjectType.WAYS,
            page=2,
            rp=10,
        )


@pytest.mark.asyncio()
async def test_key_stats():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_stats_amenity.json"
    response_str = data_file.read_text()

    url = "https://taginfo.openstreetmap.org/api/4/key/stats?key=amenity"

    with aioresponses() as m:
        m.get(
            url=url,
            body=response_str,
            status=200,
            content_type="application/json",
        )
        response = await key_stats(key="amenity")

    assert response.data[0].count == 26451233
    _, _ = str(response), repr(response)
