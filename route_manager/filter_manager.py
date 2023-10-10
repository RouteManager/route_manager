class FilterManager:
    skate = (
        f'["highway"]["area"!~"yes"]'
        f'["highway"!~"abandoned|bridleway|bus_guideway|construction|corridor|'
        f"elevator|escalator|no|path|planned|platform|proposed|raceway|razed|"
        f'service|steps|track"]'
        f'["bicycle"!~"no"]'
        f'["service"!~"alley|driveway|emergency_access|parking|parking_aisle|'
        f'private"]'
        f'["surface"!~"sand|cobblestone|dirt"]'
    )

    def __init__(self):
        self.filters = {"skate": self.skate}

    def get_filter(self, route_type):
        if route_type not in self.filters:
            raise ValueError(f"Invalid route type: {route_type}")
        return self.filters[route_type]
