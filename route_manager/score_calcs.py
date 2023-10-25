"""Fitness score calculators."""
import logging
import numbers
import math
from typing import Any, List, Dict
import networkx as nx
from collections import defaultdict


def calculate_distance_score(desired_dist, actual_dist, max_variance) -> float:
    """
    Evaluate route fitness based on distance from desired distance.

    Parameters
    ----------
    desired_dist: float
        The desired distance for the route.
    actual_dist: float
        The actual distance of the route.
    max_variance: float
        The maximum allowed variance from the desired distance.

    Returns
    -------
    float
        Normalized route score between 0 and 1, with lower scores indicating
        larger deviations from the desired distance and a sigmoid penalty
        for exceeding the maximum variance.
    """
    if not isinstance(desired_dist, numbers.Number):
        msg = f"desired_dist must of type numbers.Numeric"
        raise ValueError(msg)

    if not isinstance(actual_dist, numbers.Number):
        msg = f"actual_dist must of type numbers.Numeric"
        raise ValueError(msg)

    if not isinstance(max_variance, numbers.Number):
        msg = f"max_variance must of type numbers.Numeric"
        raise ValueError(msg)

    if not (0 < max_variance < desired_dist):
        msg = (
            f"Invalid value for max_variance, it must be"
            f" 0 < max_variance < desired_dist"
        )
        raise ValueError(msg)

    if not (0 < actual_dist < float("inf")):
        msg = (
            f"Invalid value for actual_dist, it must be"
            f"0 < actual_dist < float('inf')"
        )
        raise ValueError(msg)

    if not (0 < desired_dist < float("inf")):
        msg = (
            f"Invalid value for desired_dist, it must be"
            f"0 < desired_dist < float('inf')"
        )
        raise ValueError(msg)

    PENALTY_FACTOR = 0.01

    actual_variance = abs(desired_dist - actual_dist)
    score = 1 - actual_variance / (max_variance + actual_variance)

    if actual_variance > max_variance:
        # Apply a non-linear penalty factor to significantly reduce the score
        score *= PENALTY_FACTOR
        logging.warning(
            f"Route length of {actual_dist} is longer than the required "
            f"distance and variance of {desired_dist} +- {max_variance}"
        )

    return score


def calculate_road_type_score(highway_lengths: dict[float]) -> float:
    """
    Evaluate route fitness based on highway type composition.

    Parameters
    ----------
    highway_lengths: dict[float]
        Dictionary mapping highway types to their lengths in the route.

    Returns
    -------
    float
        Normalized route score between 0 and 1, with lower scores indicating
        less desirable highway types and a significant penalty for prohibited
        sections.
    """
    # Weight classifications for diffirent type of highways.
    OPTIMAL = 4
    PREFER = 3
    NEUTRAL = 2
    AVOID = 1
    PROHIBIT = 0

    # Non-linear penalty factor applied to routes containing a prohibited
    # section.
    PENALTY_FACTOR = 0.1

    # https://wiki.openstreetmap.org/wiki/Key:highway
    highway_weights = {
        "motorway": PROHIBIT,
        "trunk": NEUTRAL,
        "primary": PREFER,
        "secondary": PREFER,
        "tertiary": PREFER,
        "unclassified": PREFER,
        "motorway_link": PROHIBIT,
        "trunk_link": NEUTRAL,
        "primary_link": PREFER,
        "secondary_link": PREFER,
        "tertiary_link": PREFER,
        "living_street": PREFER,
        "service": AVOID,
        "track": AVOID,
        "bus_guideway": PROHIBIT,
        "road": PREFER,
        "footway": AVOID,
        "bridleway": PROHIBIT,
        "steps": PROHIBIT,
        "corridor": AVOID,
        "path": PROHIBIT,
        "via_ferrata": PROHIBIT,
        "escape": PROHIBIT,
        "raceway": PROHIBIT,
        "pedestrian": AVOID,
        "residential": PREFER,
        "cycleway": AVOID,
        "proposed": PROHIBIT,
        "construction": PROHIBIT,
    }

    # Calculate total fitness score
    route_score = 0.0
    length = 0.0
    prohibited_length = 0.0

    for highway, weight in highway_weights.items():
        if highway in highway_lengths:
            if weight == PROHIBIT:
                prohibited_length += highway_lengths[highway]
            else:
                route_score += weight * highway_lengths[highway]
            length += highway_lengths[highway]
            logging.warning(
                f"{highway_lengths[highway]:.2f} meters of "
                f"{highway} found for route."
            )
        else:
            logging.info(
                f"OSM highway ({highway}) not found in `highway_lengths`."
            )

    if prohibited_length > 0:
        # Apply a non-linear penalty factor to significantly reduce the score
        route_score *= PENALTY_FACTOR
        logging.warning(
            f"Route contains {prohibited_length} meters of PROHIBIT highway. "
            f"A penalty factor of {PENALTY_FACTOR} is applied."
        )

    if length == 0:
        route_score = 0
    else:
        route_score /= length * OPTIMAL

    return route_score


def calculate_path_lengths_by_edge_attribute(
    G: nx.MultiDiGraph, path: List[Any], edge_attribute: str
) -> Dict[str, float]:
    """
    Aggregate edge lengths by discrete edge attribute values along a path.

    Parameters
    ----------
    G: nx.MultiDiGraph
        The input graph.
    path: List[Any]
        The path through the graph, represented as a list of nodes.
    edge_attribute: str
        The name of the edge attribute to consider.

    Returns
    -------
    Dict[str, float]
        A dictionary mapping each discrete value of the edge attribute to the
        sum of edge lengths for that value along the path.

    Raises
    ------
    nx.NetworkXNoPath
        If the given path does not exist in the graph.
    """
    if not nx.is_path(G, path):
        raise nx.NetworkXNoPath("path does not exist")

    multigraph = G.is_multigraph()
    attribute_lengths = defaultdict(float)

    for node, nbr in nx.utils.pairwise(path):
        if multigraph:
            length = float("inf")
            for v in G[node][nbr].values():
                # If there are multiple edges with the same minimum length,
                # select the first one. This is because the order of edges in a
                # multigraph is arbitrary, and selecting the first one ensures
                # consistent behavior regardless of the edge order.
                if "length" in v and v["length"] < length:
                    highway = v[edge_attribute]
                    length = v["length"]
            if length != float("inf"):
                attribute_lengths[highway] += length
        else:
            if "length" in G[node][nbr]:
                attribute_lengths[G[node][nbr][edge_attribute]] += G[node][nbr][
                    "length"
                ]

    return attribute_lengths
