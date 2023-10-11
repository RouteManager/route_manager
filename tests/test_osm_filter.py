import pytest
from route_manager import osm_filter as fm


@pytest.mark.parametrize(
    "valid_network",
    ["skate", "drive", "drive_service", "walk", "bike", "all", "all_private"],
)
def test_get_valid_osm_filter(valid_network):
    assert fm.get_osm_filter(valid_network) is not None


@pytest.mark.parametrize(
    "invalid_network",
    ["skates", None, ["skate", "drive"], 0, -1, object],
)
def test_get_invalid_osm_filter(invalid_network):
    with pytest.raises(ValueError):
        fm.get_osm_filter(invalid_network)
