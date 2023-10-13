"""Test cases for route_manager module."""
import pytest
import logging
from unittest.mock import MagicMock, patch
from route_manager.route_manager import (
    RouteManager,
    MIN_ROUTE_DISTANCE,
    MAX_ROUTE_DISTANCE,
)


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
@pytest.mark.parametrize(
    "distance", [1000, MIN_ROUTE_DISTANCE, MAX_ROUTE_DISTANCE]
)
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
@pytest.mark.parametrize(
    "distance", [MIN_ROUTE_DISTANCE - 1, MAX_ROUTE_DISTANCE + 1, "foo"]
)
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
@pytest.mark.parametrize("distance", [MAX_ROUTE_DISTANCE])
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
    "location",
    [(-91, 50), (91, 50), (90, 181), (90, -181), (-91, -181), "foo"],
)
@pytest.mark.parametrize("distance", [MAX_ROUTE_DISTANCE])
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

    This test checks that the `_load_graph` method of a RouteManager instance
    correctly initializes the graph attribute.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.
    """
    rm_ldn_skate._load_graph()
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


def test_get_route_not_exist(rm_ldn_skate):
    """
    Test retieving a route by a non existing name returns None.

    This test checks that the `get_route` method of a
    RouteManager instance returns `None` id the route is not in
    the route dictionarty.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.
    """
    assert rm_ldn_skate.get_route("foo") == None


def test_add_shortest_path_route(rm_ldn_skate):
    """
    Test the creation of a shortest path route.

    This test checks that the `add_shortest_path_route` methods of a
    RouteManager instance correctly add a route to the instance.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.
    """
    rm_ldn_skate.add_shortest_path_route("foo", 60852813, 26389730)
    route = rm_ldn_skate.get_route("foo")

    assert route is not None
    assert route["start_node"] == 60852813
    assert route["end_node"] == 26389730
    assert route["path"] is not None
    assert route["route_and_neighbour_graph"] is not None


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


def test_calc_fitness_for_routes(rm_ldn_skate):
    """
    Test calculation of routes fitness.

    This test checks that the `alc_fitness_for_routes` calls the supplied
    fitness function to calculate a fitness for each route and that the fitness
    values is added to the route dictionary.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.
    """
    # Mock the fitness_func and routes attributes
    rm_ldn_skate.fitness_func.calculate_fitness = MagicMock(return_value=15)

    # Call the method
    start_node = 60852813
    end_node = 26389730
    path = [60852813, 26389730]
    rm_ldn_skate.add_route("foo", start_node, end_node, path)
    rm_ldn_skate.add_route("bar", start_node, end_node, path)
    rm_ldn_skate.calc_fitness_for_routes()

    # Assert that the fitness_func was called with the correct arguments
    for route_name, route_attributes in rm_ldn_skate.routes.items():
        # Get the args of the last call to mock
        last_call_args = rm_ldn_skate.fitness_func.calculate_fitness.call_args[
            0
        ]

        assert last_call_args[0]["start_node"] == route_attributes["start_node"]
        assert last_call_args[0]["end_node"] == route_attributes["end_node"]
        assert last_call_args[0]["path"] == route_attributes["path"]
        assert last_call_args[0]["route_and_neighbour_graph"] is not None
        assert last_call_args[0]["route_graph"] is not None
        assert route_attributes["fitness"] == 15


def test_calc_fitness_for_routes_no_fitness_func(rm_ldn_skate):
    """
    Test calc_fitness_for_routes method when no fitness function is registered.

    This test checks if a warning is logged when the fitness function is not
    registered.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.

    Returns
    -------
    None

    Notes
    -----
    The test uses the `patch` function from the `mock` module to replace the
    `logging.warning` method with a mock. It then asserts that this mock was
    called once with the expected warning message.
    """
    # Set fitness_func to None
    rm_ldn_skate.fitness_func = None

    # Mock the logging.warning method
    with patch("logging.warning") as mock_warning:
        # Call the method
        rm_ldn_skate.calc_fitness_for_routes()

        # Assert that a warning was logged
        mock_warning.assert_called_once_with("Fitness function not registered.")


def test__load_graph_file_exists(rm_ldn_skate):
    """
    Test _load_graph method when the file exists.

    This test checks if the correct methods are called when the graph file
    exists.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.

    Returns
    -------
    None

    Notes
    -----
    The test uses the `patch` function from the `mock` module to replace the
    `os.path.exists`, `self._construct_filename`, and
    `self._load_graph_from_file` methods with mocks. It then asserts that these
    mocks were called with the expected arguments.
    """
    # Mock the _construct_filename method to return a specific filename
    filename = "test_filename"
    rm_ldn_skate._construct_filename = MagicMock(return_value=filename)

    # Mock os.path.exists to return True
    with patch("os.path.exists", return_value=True):
        # Mock the _load_graph_from_file method
        with patch.object(rm_ldn_skate, "_load_graph_from_file") as mock_load:
            # Call the method
            rm_ldn_skate._load_graph()

            # Assert that _load_graph_from_file was called with the correct
            # argument
            mock_load.assert_called_once_with(filename)


def test__load_graph_file_not_exists(rm_ldn_skate):
    """
    Test _load_graph method when the file does not exist.

    This test checks if the correct methods are called when the graph file does
    not exist.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.

    Returns
    -------
    None

    Notes
    -----
    The test uses the `patch` function from the `mock` module to replace the
    `os.path.exists`,`self._construct_filename`, `self._generate_graph`, and
    `self._save_graph_to_file` methods with mocks. It then asserts that these
    mocks were called with the expected arguments.
    """
    # Mock the _construct_filename method to return a specific filename
    filename = "test_filename"
    rm_ldn_skate._construct_filename = MagicMock(return_value=filename)

    # Mock os.path.exists to return False
    with patch("os.path.exists", return_value=False):
        # Mock the _generate_graph and _save_graph_to_file methods
        with patch.object(
            rm_ldn_skate, "_generate_graph"
        ) as mock__generate_graph, patch.object(
            rm_ldn_skate, "_save_graph_to_file"
        ) as mock__save_graph:
            # Call the method
            rm_ldn_skate._load_graph()

            # Assert that _generate_graph and _save_graph_to_file were called
            # with the correct arguments
            mock__generate_graph.assert_called_once()
            mock__save_graph.assert_called_once_with(filename)


def test__generate_graph(rm_ldn_skate):
    """
    Test _generate_graph method.

    This test checks if the correct methods are called with the correct
    arguments.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.

    Returns
    -------
    None

    Notes
    -----
    The test uses the `patch` function from the `mock` module to replace the
    `ox.graph_from_point` and `osm_filter.get_filter` methods with mocks. It
    then asserts that these mocks were called with the expected arguments.
    """
    # Set lat_lon, distance, and network_type attributes
    rm_ldn_skate.lat_lon = (0, 0)
    rm_ldn_skate.distance = 1000
    rm_ldn_skate.network_type = "drive"

    # Mock ox.graph_from_point and osm_filter.get_filter methods
    with patch("osmnx.graph_from_point") as mock_graph, patch(
        "route_manager.osm_filter.get_osm_filter"
    ) as mock_filter:
        # Call the method
        rm_ldn_skate._generate_graph()

        # Assert that get_filter was called with the correct argument
        mock_filter.assert_called_once_with(rm_ldn_skate.network_type)

        # Assert that graph_from_point was called with the correct arguments
        mock_graph.assert_called_once_with(
            rm_ldn_skate.lat_lon,
            dist=rm_ldn_skate.distance,
            simplify=True,
            custom_filter=mock_filter.return_value,
        )


from unittest import mock


def test__save_graph_to_file(rm_ldn_skate):
    """
    Test _save_graph_to_file method.

    This test checks if the correct method is called with the correct arguments.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager instance.

    Returns
    -------
    None

    Notes
    -----
    The test uses the `patch` function from the `mock` module to replace the
    `osmnx.save_graphml` method with a mock. It then asserts that this mock
    was called with the expected arguments.
    """
    # Mock osmnx.save_graphml method
    with mock.patch("osmnx.save_graphml") as mock_save:
        # Call the method with a test filename
        filename = "test_filename"
        rm_ldn_skate._save_graph_to_file(filename)

        # Assert that save_graphml was called with the correct arguments
        mock_save.assert_called_once_with(rm_ldn_skate.graph, filename)
