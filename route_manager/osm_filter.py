"""
OSM filter strings.

Returns
-------
str
    The OSM filter string.

Raises
------
ValueError
    If `network_type` is not a string.
"""
from typing import Dict
from osmnx import _overpass as op


def get_osm_filter(network_type: str) -> str:
    """
    Get the OpenStreetMap (OSM) filter based on the network type.

    This function returns a filter string that can be used to query OSM data.
    The filter string is determined based on the network type. If the network
    type is not recognized, it falls back to the default OSM filter.

    Parameters
    ----------
    network_type : str
        The type of the network. It must be a valid network type.

    Returns
    -------
    str
        The OSM filter string.

    Raises
    ------
    ValueError
        If `network_type` is not a string.
    """
    filters: Dict[str, str] = {}

    filters["skate"] = (
        f'["highway"]["area"!~"yes"]'
        f'["highway"!~"abandoned|bridleway|bus_guideway|construction|corridor|'
        f"elevator|escalator|no|path|planned|platform|proposed|raceway|razed|"
        f'service|steps|track"]'
        f'["bicycle"!~"no"]'
        f'["service"!~"alley|driveway|emergency_access|parking|parking_aisle|'
        f'private"]'
        f'["surface"!~"sand|cobblestone|dirt"]'
    )

    if not isinstance(network_type, str):
        msg = f"network_type must be a str value"
        raise ValueError(msg)

    if network_type in filters:
        osm_filter = filters[network_type]
    else:
        osm_filter = op._get_osm_filter(network_type)

    return osm_filter
