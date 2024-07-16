import datetime
from pathlib import Path

from aio_taginfo.api.v4.key import PrevalentValue
from aio_taginfo.api.v4.key.chronology import KeyChronology
from aio_taginfo.api.v4.key.combinations import KeyCombination
from aio_taginfo.api.v4.key.overview import KeyOverview, Response
from aio_taginfo.api.v4.key.similar import SimilarKey
from aio_taginfo.api.v4.site.config.geodistribution import SiteConfigGeodistribution
from aio_taginfo.api.v4.tags.popular import PopularTag

import pytest
from pydantic import TypeAdapter, ValidationError


def test_existing_key_overview():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_overview_amenity.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[KeyOverview])
    response = type_adapter.validate_json(response_str, strict=True)
    assert response.data.key == "amenity"


def test_nonexistent_key_overview():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_overview_nonexistent.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[KeyOverview])
    response = type_adapter.validate_json(response_str, strict=True)
    assert response.data.key == "thereisnosuchkey"


def test_empty_key_overview():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_overview_empty.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[KeyOverview])
    with pytest.raises(ValidationError):
        type_adapter.validate_json(response_str, strict=True)


def test_unset_key_overview():
    # you get this response by not providing a ?key= to the endpoint:
    # https://taginfo.openstreetmap.org/api/4/key/overview
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_overview_unset.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[KeyOverview])
    with pytest.raises(ValidationError):
        type_adapter.validate_json(response_str, strict=True)


def test_site_config_geodistribution():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "site_config_geodistribution.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(SiteConfigGeodistribution)
    response = type_adapter.validate_json(response_str, strict=True)
    assert response.width == 360


def test_key_prevalent_values():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_prevalent_values_highway.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[list[PrevalentValue]])
    response = type_adapter.validate_json(response_str, strict=True)
    assert response.data[0].count == 65032833


def test_key_similar():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_similar_highway.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[list[SimilarKey]])
    response = type_adapter.validate_json(response_str, strict=True)
    assert response.data[0].other_key == "FIXME:highway"


def test_tags_popular():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "tags_popular.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[list[PopularTag]])
    response = type_adapter.validate_json(response_str, strict=True)
    assert response.data[0].key == "building"

    invalid_in_wiki = {
        "key": "building",
        "value": "yes",
        "in_wiki": "neither 0 nor 1",
        "count_all": 483603796,
        "count_all_fraction": 0.0476,
        "count_nodes": 298594,
        "count_nodes_fraction": 0.0013,
        "count_ways": 482665535,
        "count_ways_fraction": 0.4731,
        "count_relations": 639667,
        "count_relations_fraction": 0.0528,
        "projects": 13,
    }
    with pytest.raises(ValidationError):
        _tag = PopularTag(**invalid_in_wiki)


def test_key_chronology():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_chronology_highway.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[list[KeyChronology]])
    response = type_adapter.validate_json(response_str, strict=True)
    assert response.data[0].date == datetime.date(2007, 10, 7)


def test_key_combinations():
    test_dir = Path(__file__).resolve().parent
    data_file = test_dir / "responses" / "key_combinations_highway.json"
    response_str = data_file.read_text()
    type_adapter = TypeAdapter(Response[list[KeyCombination]])
    response = type_adapter.validate_json(response_str, strict=True)
    assert response.data[0].together_count == 58128837
