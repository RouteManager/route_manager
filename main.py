"""Implement route_manager."""
import route_manager.fitness as fitness
from route_manager.route_manager import RouteManager
import osmnx as ox


def main():
    """Implement key features of route_manager."""
    # Wellington Arch. Use static not to burden nominatum
    location_point = (51.5025031, -0.15081986768597055)

    route_manager = RouteManager(location_point, 1000, "skate")
    route_manager._load_graph()
    fig, ax = ox.plot_graph(route_manager.graph, node_color="r")

    route_manager.add_shortest_path_route("test_route", 60852813, 26389730)
    path = route_manager.get_route("test_route")["path"]
    fig, ax = ox.plot_graph_route(
        route_manager.graph,
        path,
        route_color="y",
        route_linewidth=6,
        node_size=0,
    )

    route_graph = route_manager.get_route("test_route")[
        "route_and_neighbour_graph"
    ]
    fig, ax = ox.plot_graph(route_graph, node_color="r")
    fig, ax = ox.plot_graph_route(
        route_graph, path, route_color="y", route_linewidth=6, node_size=0
    )

    ## ---- Fitness function

    route_manager.register_fitness_func(fitness.calc_route_fitness)
    route_manager.add_shortest_path_route("test_route_2", 60852813, 26389730)
    route_manager.calc_fitness_for_routes()

    for route_name, route_attributes in route_manager.routes.items():
        print(
            f"Route: {route_name}, "
            f"start: {route_attributes['start_node']}, "
            f"end: {route_attributes['end_node']}, "
            f"fitness: {route_attributes['fitness']}"
        )


if __name__ == "__main__":
    main()
