"""Test the OSM filter module."""

import pytest
from route_manager import osm_filter as fm


@pytest.mark.parametrize(
    "valid_network",
    ["skate", "drive", "drive_service", "walk", "bike", "all", "all_private"],
)
def test_get_valid_osm_filter(valid_network):
    """
    Verify `get_osm_filter` function returns.

    This test checks that the `get_osm_filter` function in the
    `route_manager.osm_filter` module returns a non-None result when called
    with a valid network type.

    Parameters
    ----------
    valid_network : str
        A valid network type.
    """
    assert fm.get_osm_filter(valid_network) is not None


@pytest.mark.parametrize(
    "invalid_network",
    ["skates", None, ["skate", "drive"], 0, -1, object],
)
def test_get_invalid_osm_filter(invalid_network):
    """
    Test `get_osm_filter` raises a ValueError for invalid types.

    This test checks that the `get_osm_filter` function in the
    `route_manager.osm_filter` module raises a ValueError when called with an
    invalid network type.

    Parameters
    ----------
    invalid_network : str
        An invalid network type.
    """
    with pytest.raises(ValueError):
        fm.get_osm_filter(invalid_network)
