import pytest
from route_manager.route_manager import RouteManager, MIN_DISTANCE, MAX_DISTANCE


WELLINGTON_ARCH = (51.5025031, -0.15081986768597055)


@pytest.fixture(scope="module")
def rm_ldn_skate():
    return RouteManager(WELLINGTON_ARCH, 1000, "skate")


@pytest.mark.parametrize("location", [WELLINGTON_ARCH, (90, 180, (-90, -180))])
@pytest.mark.parametrize("distance", [1000, MIN_DISTANCE, MAX_DISTANCE])
@pytest.mark.parametrize(
    "network_type",
    ["skate", "drive", "drive_service", "walk", "bike", "all", "all_private"],
)
def test_valid_init(location, distance, network_type):
    rm = RouteManager(tuple(location), distance, network_type)
    assert rm.distance == distance
    assert rm.lat_lon == location
    assert rm.network_type == network_type


@pytest.mark.parametrize("location", [WELLINGTON_ARCH])
@pytest.mark.parametrize("distance", [MIN_DISTANCE - 1, MAX_DISTANCE + 1])
@pytest.mark.parametrize("network_type", ["skate"])
def test_invalid_distance_init(location, distance, network_type):
    with pytest.raises(ValueError):
        RouteManager(location, distance, network_type)


@pytest.mark.parametrize("location", [WELLINGTON_ARCH])
@pytest.mark.parametrize("distance", [MAX_DISTANCE])
@pytest.mark.parametrize("network_type", ["foo", "None"])
def test_invalid_network_type_init(location, distance, network_type):
    with pytest.raises(ValueError):
        RouteManager(location, distance, network_type)


@pytest.mark.parametrize(
    "location", [(-91, 50), (91, 50), (90, 181), (90, -181), (-91, -181)]
)
@pytest.mark.parametrize("distance", [MAX_DISTANCE])
@pytest.mark.parametrize("network_type", ["skate"])
def test_invalid_lat_lon_init(location, distance, network_type):
    with pytest.raises(ValueError):
        RouteManager(location, distance, network_type)


def test_init_graph(rm_ldn_skate):
    rm_ldn_skate.load_graph()
    assert rm_ldn_skate.graph is not None


def test_register_fitness_func(rm_ldn_skate):
    def fitness_func_abc(route_attributes):
        return len(route_attributes["path"])

    rm_ldn_skate.register_fitness_func(fitness_func_abc)
    assert rm_ldn_skate.fitness_func == fitness_func_abc


def test_add_route(rm_ldn_skate):
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
