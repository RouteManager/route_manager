"""
A module to manage routes for a given location.

Returns
-------
RouteManager
    This class provides methods to add routes, get routes, calculate the
    shortest path between two points, and calculate fitness for all routes. It
    uses the OSMnx library to work with OpenStreetMap data.

Raises
------
ValueError
    If lat_lon is not a valid latitude and longitude tuple.
ValueError
    If distance is not a valid number
"""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import osmnx as ox
import os
import numbers
import logging

from . import osm_filter as of


# Maximum distance for a route. The distance for a route must be less than or
# equal to this value. BEWARE: Increasing this value will result in very large
# downloads form OSM and may get your IP banned.
MAX_DISTANCE = 7000

# Minimum distance for a route. The distance for a route must be greater than
# or equal to this value.
MIN_DISTANCE = 1


class RouteManager:
    """
    A class to manage routes for a given location.

    This class provides methods to add routes, get routes, calculate the
    shortest path between two points, and calculate fitness for all routes. It
    uses the OSMnx library to work with OpenStreetMap data.

    Attributes
    ----------
    lat_lon : Tuple[float, float]
        Latitude and longitude for the route.
    distance : numbers.Number
        Distance for the route.
    network_type : str
        Type of the network.
    graph : NoneType
        Graph for the route. Initialized as None.
    routes : dict
        Dictionary to store routes. Initialized as an empty dictionary.
    fitness_func : NoneType
        Fitness function for the route. Initialized as None.
    """

    def __init__(
        self,
        lat_lon: Tuple[float, float],
        distance: numbers.Number,
        network_type: str,
    ) -> None:
        """
        Initialize the RouteManager.

        Set the latitude, longitude, distance and
        network type.

        Parameters
        ----------
        lat_lon : Tuple[float, float]
            A tuple containing latitude and longitude.
        distance : numbers.Number
            The distance for the route, where 1 <= distance <= MAX_DISTANCE.
        network_type : str
            The type of the network. It must be a valid network type.

        Raises
        ------
        ValueError
            If lat_lon is not a valid latitude and longitude tuple.
        ValueError
            If distance is not a valid number
        """
        if not self.is_valid_lat_lon(lat_lon):
            msg = f"lat_lon must be a valid latitude and longitude tuple"
            raise ValueError(msg)
        self.lat_lon = lat_lon

        if not self.is_valid_distance(distance):
            msg = (
                f"distance must be numeric, where "
                f"{MIN_DISTANCE} <= distance <= {MAX_DISTANCE}"
            )
            raise ValueError(msg)
        self.distance = distance

        try:
            of.get_osm_filter(network_type)
            self.network_type = network_type
        except ValueError:
            raise

        self.graph = None
        self.routes = {}
        self.fitness_func = None

    def is_valid_lat_lon(self, lat_lon: Tuple[float, float]) -> bool:
        """
        Check if the given latitude and longitude are valid.

        Parameters
        ----------
        lat_lon : Tuple[float, float]
            A tuple containing latitude and longitude.

        Returns
        -------
        bool
            True if the latitude is between -90 and 90 degrees, and the
            longitude is between -180 and 180 degrees. False otherwise.
        """
        if not isinstance(lat_lon, tuple):
            return False
        return abs(lat_lon[0]) <= 90 and abs(lat_lon[1]) <= 180

    def is_valid_distance(self, distance: numbers.Number) -> bool:
        """
        Check if the given distance is valid.

        Parameters
        ----------
        distance : numbers.Number
            The distance to be checked.

        Returns
        -------
        bool
            True if the distance is a number and is between MIN_DISTANCE and
            MAX_DISTANCE. False otherwise.
        """
        if not isinstance(distance, numbers.Number):
            return False
        return MIN_DISTANCE <= distance <= MAX_DISTANCE

    def construct_filename(self) -> str:
        """
        Construct the filename for the graph.

        Returns
        -------
        str
            The filename for the graph.
        """
        return (
            f"./graph_cache/graph_{self.lat_lon}_{self.distance}_"
            f"{self.network_type}.graphml"
        )

    def load_graph_from_file(self, filename: str) -> None:
        """
        Load a graph from file.

        Parameters
        ----------
        filename : str
            The name of the file from which to load the graph.
        """
        self.graph = ox.load_graphml(filename)

    def generate_graph(self) -> None:
        """
        Download OSM data as a graph.

        Uses the the area described by self.lat_lon and self.distance
        """
        self.graph = ox.graph_from_point(
            self.lat_lon,
            dist=self.distance,
            simplify=True,
            custom_filter=of.get_filter(self.network_type),
        )

    def save_graph_to_file(self, filename: str) -> None:
        """
        Save the graph to a file.

        Parameters
        ----------
        filename : str
            The name of the file to which to save the graph.
        """
        ox.save_graphml(self.graph, filename)

    def load_graph(self) -> None:
        """
        Load the graph from a file or generates a new one.

        If the graph file exists, this method loads the graph from the file.
        Otherwise, it generates a new graph and saves it to a file.
        """
        filename = self.construct_filename()

        if os.path.exists(filename):
            self.load_graph_from_file(filename)
        else:
            self.generate_graph()
            self.save_graph_to_file(filename)

    def register_fitness_func(self, fitness_func: Callable) -> None:
        """
        Register a fitness function.

        This method sets the `fitness_func` attribute to the provided function.

        Parameters
        ----------
        fitness_func : Callable
            The fitness function to be registered.

        Returns
        -------
        None
        """
        self.fitness_func = fitness_func

    def add_route(
        self, route_name: str, start_node: int, end_node: int, path: List[int]
    ) -> None:
        """Add a route to the routes dictionary.

        This method calculates the neighbours of the path, creates a subgraph
        for the path and its neighbours, and adds all this information to the
        routes dictionary under the provided route name.

        Parameters
        ----------
        route_name : str
            The name of the route.
        start_node : int
            The starting node of the route.
        end_node : int
            The ending node of the route.
        path : List[int]
            The path of the route as a list of node IDs.

        Returns
        -------
        None
        """
        neighbours = self.get_path_neigbours(path)
        self.routes[route_name] = {
            "start_node": start_node,
            "end_node": end_node,
            "path": path,
            "route_graph": self.graph.subgraph(path).copy(),
            "route_and_neighbour_graph": self.graph.subgraph(
                list(set(neighbours) | set(path))
            ).copy(),
        }

    def get_path_neigbours(self, path: List[int]) -> List[int]:
        """
        Get the neighbours of all nodes in the path.

        This method iterates over all nodes in the path, finds their neighbours
        in the graph, and returns a list of all unique neighbours.

        Parameters
        ----------
        path : List[int]
            The path as a list of node IDs.

        Returns
        -------
        List[int]
            The list of unique neighbours of all nodes in the path.
        """
        neighbours: Set[int] = set()
        for node in path:
            neighbours.update(self.graph.neighbors(node))
        return list(neighbours)

    def add_shortest_path_route(
        self, route_name: str, start_node: int, end_node: int
    ) -> None:
        """
        Add the shortest path route between the start node and end node.

        This method calculates the shortest path between the start node and end
        node, and then calls the `add_route` method to add this route to the
        routes dictionary.

        Parameters
        ----------
        route_name : str
            The name of the route.
        start_node : int
            The starting node of the route.
        end_node : int
            The ending node of the route.

        Returns
        -------
        None
        """
        path = self.shortest_path_route(start_node, end_node)
        self.add_route(route_name, start_node, end_node, path)

    def get_route(self, route_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a route from the routes dictionary.

        This method checks if a route with the given name exists in the routes
        dictionary. If it does, it returns the route. Otherwise, it returns
        None.

        Parameters
        ----------
        route_name : str
            The name of the route.

        Returns
        -------
        Optional[Dict[str, Any]]
            The route if it exists in the routes dictionary, None otherwise.
        """
        if route_name not in self.routes:
            return None
        return self.routes[route_name]

    def shortest_path_route(
        self, start_osm_id: int, end_osm_id: int
    ) -> List[int]:
        """
        Calculate the shortest path between two nodes in the graph.

        This method uses the `shortest_path` function from the OSMnx library to
        calculate the shortest path between the start node and end node in the
        graph.

        Parameters
        ----------
        start_osm_id : int
            The OSM ID of the start node.
        end_osm_id : int
            The OSM ID of the end node.

        Returns
        -------
        List[int]
            The shortest path as a list of node IDs.
        """
        return ox.shortest_path(self.graph, start_osm_id, end_osm_id)

    def calc_fitness_for_routes(self) -> None:
        """
        Calculate fitness for all routes.

        This method iterates over all routes in the routes dictionary and
        calculates their fitness using the registered fitness function. If no
        fitness function is registered, it logs a warning and returns.

        Returns
        -------
        None
        """
        if not self.fitness_func:
            logging.warning("Fitness function not registered.")
            return
        for route_name, route_attributes in self.routes.items():
            route_attributes["fitness"] = self.fitness_func(route_attributes)
