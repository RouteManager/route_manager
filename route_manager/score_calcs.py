"""Fitness score calculators."""
import logging
import numbers
from typing import Any, List, Dict
import networkx as nx
from collections import defaultdict


def calculate_distance_score(desired_dist, actual_dist, max_variance) -> float:
    """
    Calculate and return the score for the desired distance criterion.

    This method calculates the score based on how close the route's
    distance is to the desired distance. If the route's distance is
    within a set error margin of the desired distance, a higher score is
    returned. If it's outside this margin, the route is deemed unfit and a
    score of negative infinity (`float('-inf')`) is returned.

    Returns
    -------
    float
        The score for the desired distance criterion. If the route's
        distance is outside the set error margin of the desired distance,
        it returns negative infinity (`float('-inf')`).
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

    actual_variance = abs(desired_dist - actual_dist)
    if actual_variance > max_variance:
        score = float("-inf")
    else:
        score = float(1 - actual_variance / max_variance)

    logging.warning(
        f"Route distance: {desired_dist}/{actual_dist}, "
        f"Route variance: {actual_variance}/{max_variance}, "
        f"Score: {score}"
    )

    return score


def calculate_road_type_score(highway_lengths: dict[float]) -> float:
    """
    Calculate score for road type.

    Parameters
    ----------
    highway_lengths : dict[float]
        A dictionary providing a breakdown of distance by highway type

    Returns
    -------
    float
        The score for the road type criterion.

    """
    PREFER = 3
    OK = 2
    AVOID = 1
    highway_weights = {
        "primary": PREFER,
        "residential": PREFER,
        "cycleway": AVOID,
        "pedestrian": AVOID,
        "footway": AVOID,
        "trunk": OK,
    }

    # Calculate total fitness score
    route_score = 0.0
    length = 0.0
    for highway, weight in highway_weights.items():
        route_score += weight * highway_lengths[highway]
        length += highway_lengths[highway]

    score = route_score / (length * PREFER)

    return score


def path_length_over_weight(
    G: nx.MultiDiGraph, path: List[Any], weight: str
) -> Dict[str, float]:
    """
    Calculate the total length for each 'weight' category in the given path.

    Parameters
    ----------
    G : nx.MultiDiGraph
        The graph on which to calculate path lengths.
    path : list
        The path for which to calculate lengths.
    weight : str
        The edge attribute to calculate total distance for.

    Returns
    -------
    dict
        A dictionary where keys are categories of the weight attribute and
        values are their total lengths.

    Raises
    ------
    nx.NetworkXNoPath
        If the given path does not exist in the graph.
    """
    if not nx.is_path(G, path):
        raise nx.NetworkXNoPath("path does not exist")

    multigraph = G.is_multigraph()
    highway_lengths = defaultdict(float)

    for node, nbr in nx.utils.pairwise(path):
        if multigraph:
            length = float("inf")
            for v in G[node][nbr].values():
                if "length" in v and v["length"] < length:
                    highway = v[weight]
                    length = v["length"]
            if length != float("inf"):
                highway_lengths[highway] += length
        else:
            if "length" in G[node][nbr]:
                highway_lengths[G[node][nbr][weight]] += G[node][nbr]["length"]

    return highway_lengths
