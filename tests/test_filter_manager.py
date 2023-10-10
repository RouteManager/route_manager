import pytest
from route_manager.filter_manager import FilterManager


def test_filter_manager():
    fm = FilterManager()

    # Test that the skate filter is correctly set
    assert fm.get_filter("skate") == fm.skate

    # Test that an invalid route type raises a ValueError
    with pytest.raises(ValueError):
        fm.get_filter("invalid_route_type")
