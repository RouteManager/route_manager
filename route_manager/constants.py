"""Settings."""

# The minimum latitude value used ofr lat_lon tuples
MIN_LAT = -90

# The maximum latitude value used ofr lat_lon tuples
MAX_LAT = 90

# The minimum longitude value used ofr lat_lon tuples
MIN_LON = -180

# The maximum longitude value used ofr lat_lon tuples
MAX_LON = 180

# Maximum distance for a route. The distance for a route must be less than or
# equal to this value. BEWARE: Increasing this value will result in very large
# downloads form OSM and may get your IP banned.
MAX_ROUTE_DISTANCE = 1500

# Minimum distance for a route. The distance for a route must be greater than
# or equal to this value.
MIN_ROUTE_DISTANCE = 1

# The maximum allowed route distance in meters.
MAX_DISTANCE_VARIANCE = 3000
# The minimum allowed route distance in meters.
MIN_DISTANCE_VARIANCE = 0

# The maximum incline allowed
MAX_INCLINE_PERCENT = 5

# The maximum decline allowed
MAX_DECLINE_PERCENT = 5
