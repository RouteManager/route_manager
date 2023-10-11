from osmnx import _overpass as op


def get_osm_filter(network_type):
    filters = {}
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
