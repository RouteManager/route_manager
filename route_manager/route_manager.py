import osmnx as ox
import os
import numbers

from . import osm_filter as of


MAX_DISTANCE = 8000
MIN_DISTANCE = 1


class RouteManager:
    def __init__(self, lat_lon, distance, network_type):
        if not self.is_valid_lat_lon(lat_lon):
            msg = f"lat_lon must be a valid latitude and longitude tuple"
            raise (ValueError)
        self.lat_lon = lat_lon

        if not self.is_valid_distance(distance):
            msg = (
                f"distance must be numeric, where "
                f"{MIN_DISTANCE} <= distance <= {MAX_DISTANCE}"
            )
            raise ValueError(msg)
        self.distance = distance

        self.graph = None
        self.routes = {}
        self.fitness_func = None

        try:
            of.get_osm_filter(network_type)
            self.network_type = network_type
        except ValueError as ve:
            raise ve

    def is_valid_lat_lon(self, lat_lon):
        if not isinstance(lat_lon, tuple):
            return False
        return abs(lat_lon[0]) <= 90 and abs(lat_lon[1]) <= 180

    def is_valid_distance(self, distance):
        if not isinstance(distance, numbers.Number):
            return False
        return MIN_DISTANCE <= distance <= MAX_DISTANCE

    def load_graph(self):
        filename = (
            f"./graph_cache/graph_{self.lat_lon}_{self.distance}_"
            f"{self.network_type}.graphml"
        )
        if os.path.exists(filename):
            self.graph = ox.load_graphml(filename)
        else:
            self.graph = ox.graph_from_point(
                self.lat_lon,
                dist=self.distance,
                simplify=True,
                custom_filter=of.get_filter(self.network_type),
            )
            ox.save_graphml(self.graph, filename)

    def register_fitness_func(self, fitness_func):
        self.fitness_func = fitness_func

    def add_route(self, route_name, start_node, end_node, path):
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

    def get_path_neigbours(self, path):
        neighbours = set()
        for node in path:
            neighbours.update(self.graph.neighbors(node))
        return list(neighbours)

    def add_shortest_path_route(self, route_name, start_node, end_node):
        path = self.shortest_path_route(start_node, end_node)
        self.add_route(route_name, start_node, end_node, path)

    def get_route(self, route_name):
        if route_name not in self.routes:
            return None
        return self.routes[route_name]

    def shortest_path_route(self, start_osm_id, end_osm_id):
        return ox.shortest_path(self.graph, start_osm_id, end_osm_id)

    def calc_fitness_for_routes(self):
        if not self.fitness_func:
            print("Fitness function not registered.")
            return
        for route_name, route_attributes in self.routes.items():
            route_attributes["fitness"] = self.fitness_func(route_attributes)
