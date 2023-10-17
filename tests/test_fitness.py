"""Test cases for fitnes function."""
import logging
from route_manager.fitness import Fitness
from route_manager.route_manager import RouteManager
import pytest
from tests.test_data import WELLINGTON_ARCH, START_OSM_NODE_ID, END_OSM_NODE_ID


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
    rm = RouteManager(WELLINGTON_ARCH, 1000, "skate")
    rm._load_graph()
    rm.add_shortest_path_route(
        "serp_to_pub", START_OSM_NODE_ID, END_OSM_NODE_ID
    )
    return rm


@pytest.fixture(scope="module")
def fitness():
    """Fitness object.

    Returns
    -------
    Fitness
        Instance of Fitness class
    """
    Fitness(1000, 1000 * 0.5, 0.05, 0.05)
    return Fitness(1000, 1000 * 0.5, 0.05, 0.05)


def test_calculate_fitness(fitness):
    """
    Calculate route fitness based on its attributes.

    Parameters
    ----------
    route_attributes : dict
        A dictionary containing all the route attributes.

    Returns
    -------
    int
        An float value representing the fitness of the route.
    """
    # TODO: Implement tests for `test_calculate_fitness`
    pass


def test__get_desired_distance_score(
    rm_ldn_skate: RouteManager, fitness: Fitness
):
    """Test distance calculator.

    Parameters
    ----------
    rm_ldn_skate : RouteManager
        A RouteManager object with a populated route for testing
    """
    # TODO: Implement test for `_get_desired_distance_score`
    pass
