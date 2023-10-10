import pytest
from route_manager.route_manager import RouteManager
from route_manager.filter_manager import FilterManager


@pytest.fixture(scope="module")
def fm():
    return FilterManager()


@pytest.fixture(scope="module")
def rm_ldn_skate(fm):
    # Wellington Arch. Use static not to burden nominatum
    location_point = (51.5025031, -0.15081986768597055)
    return RouteManager(location_point, 1000, "skate", fm)


def test_rm_init(rm_ldn_skate, fm):
    # Test that the filter is correctly set
    assert rm_ldn_skate.filter == fm.get_filter("skate")


def test_fm_invalid_route_type(fm):
    # Test that an invalid route type raises a ValueError
    with pytest.raises(ValueError):
        fm.get_filter("invalid_route_type")


def test_rm_init_graph(rm_ldn_skate):
    # Test load_graph method
    rm_ldn_skate.load_graph()
    assert rm_ldn_skate.graph is not None


def test_rm_register_fitness_func(rm_ldn_skate):
    # Test register_fitness_func method
    def fitness_func_abc(route_attributes):
        return len(route_attributes["path"])

    rm_ldn_skate.register_fitness_func(fitness_func_abc)
    assert rm_ldn_skate.fitness_func == fitness_func_abc


def test_rm_add_route(rm_ldn_skate):
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
