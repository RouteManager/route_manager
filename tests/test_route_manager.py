"""Test cases for route_manager module."""
import pytest
from route_manager.route_manager import RouteManager, MIN_DISTANCE, MAX_DISTANCE


WELLINGTON_ARCH = (51.5025031, -0.15081986768597055)


@pytest.fixture(scope="module")
def rm_ldn_skate():
    """
    Create a RouteManager instance for testing.

    This fixture creates a RouteManager instance with a fixed location,
    distance, and network type. The instance is used for testing the
    RouteManager class methods.

    Returns
    -------
    RouteManager
        A RouteManager instance.
    """
    return RouteManager(WELLINGTON_ARCH, 1000, "skate")


@pytest.mark.parametrize("location", [WELLINGTON_ARCH, (90, 180, (-90, -180))])
@pytest.mark.parametrize("distance", [1000, MIN_DISTANCE, MAX_DISTANCE])
@pytest.mark.parametrize(
    "network_type",
    ["skate", "drive", "drive_service", "walk", "bike", "all", "all_private"],
)
def test_valid_init(location, distance, network_type):
    """
    Test the initialization of a RouteManager instance.

    This test checks that a RouteManager instance can be successfully
    initialized with valid parameters.

    Parameters
    ----------
    location : tuple
        A tuple containing latitude and longitude.
    distance : int or float
        The distance for the route.
    network_type : str
        The type of the network.
    """
    rm = RouteManager(tuple(location), distance, network_type)
    assert rm.distance == distance
    assert rm.lat_lon == location
    assert rm.network_type == network_type


@pytest.mark.parametrize("location", [WELLINGTON_ARCH])
@pytest.mark.parametrize("distance", [MIN_DISTANCE - 1, MAX_DISTANCE + 1])
@pytest.mark.parametrize("network_type", ["skate"])
def test_invalid_distance_init(location, distance, network_type):
    """
    Test RouteManager initialization with invalid distances.

    This test checks that the RouteManager initialization raises a ValueError
    when an invalid distance is provided.

    Parameters
    ----------
    location : tuple
        A tuple containing latitude and longitude.
    distance : int or float
        An invalid distance for the route.
    network_type : str
        The type of the network.
    """
    with pytest.raises(ValueError):
        RouteManager(location, distance, network_type)


@pytest.mark.parametrize("location", [WELLINGTON_ARCH])
@pytest.mark.parametrize("distance", [MAX_DISTANCE])
@pytest.mark.parametrize("network_type", ["foo", "None"])
def test_invalid_network_type_init(location, distance, network_type):
    """
    Test RouteManager initialization with invalid network types.

    This test checks that the RouteManager initialization raises a ValueError
    when an invalid network type is provided.

    Parameters
    ----------
    location : tuple
        A tuple containing latitude and longitude.
    distance : int or float
        The distance for the route.
    network_type : str
        An invalid type of the network.
    """
    with pytest.raises(ValueError):
        RouteManager(location, distance, network_type)


@pytest.mark.parametrize(
    "location", [(-91, 50), (91, 50), (90, 181), (90, -181), (-91, -181)]
)
@pytest.mark.parametrize("distance", [MAX_DISTANCE])
@pytest.mark.parametrize("network_type", ["skate"])
def test_invalid_lat_lon_init(location, distance, network_type):
    """
    Test RouteManager initialization with invalid latitude and longitude.

    This test checks that the RouteManager initialization raises a ValueError
    when an invalid latitude and longitude are provided.

    Parameters
    ----------
    location : tuple
        A tuple containing invalid latitude and longitude.
    distance : int or float
        The distance for the route.
    network_type : str
        The type of the network.
    """
    with pytest.raises(ValueError):
        RouteManager(location, distance, network_type)


def test_init_graph(rm_ldn_skate):
    """
    Test the initialization of the graph in a RouteManager instance.

    This test checks that the `load_graph` method of a RouteManager instance
    correctly initializes the graph attribute.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.
    """
    rm_ldn_skate.load_graph()
    assert rm_ldn_skate.graph is not None


def test_register_fitness_func(rm_ldn_skate):
    """
    Test the registration of a fitness function in a RouteManager instance.

    This test checks that the `register_fitness_func` method of a RouteManager
    instance correctly sets the fitness function attribute.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.
    """

    def fitness_func_abc(route_attributes):
        return len(route_attributes["path"])

    rm_ldn_skate.register_fitness_func(fitness_func_abc)
    assert rm_ldn_skate.fitness_func == fitness_func_abc


def test_add_route(rm_ldn_skate):
    """
    Test the addition and retrieval of a route in a RouteManager instance.

    This test checks that the `add_route` and `get_route` methods of a
    RouteManager instance correctly add a route to the instance and retrieve
    it.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.
    """
    # Test add_route and get_route methods
    route_name = "test_route"
    start_node = 60852813
    end_node = 26389730
    path = [60852813, 26389730]
    rm_ldn_skate.add_route(route_name, start_node, end_node, path)
    route = rm_ldn_skate.get_route(route_name)

    assert route is not None
    assert route["start_node"] == start_node
    assert route["end_node"] == end_node
    assert route["path"] == path
    assert route["route_and_neighbour_graph"] is not None
