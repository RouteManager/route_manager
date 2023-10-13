"""Fitness function to calculate route fitness."""
import math
import numbers
from typing import Dict
from route_manager.constants import (
    MAX_INCLINE_PERCENT,
    MAX_DECLINE_PERCENT,
    MIN_DISTANCE_VARIANCE,
    MAX_DISTANCE_VARIANCE,
    MIN_ROUTE_DISTANCE,
    MAX_ROUTE_DISTANCE,
)


class Fitness:
    """A class to calculate the fitness of a route based on a set of criteria.

    The fitness function is additive in nature, meaning that it sums up the
    weighted scores for each criterion to calculate the total fitness score
    for a route.

    Attributes
    ----------
    distance : float
        Positive value for the desired route distance in meters.
    dist_variance : float
        Maximum distance variance, longer or shorter, in meters for the route.
    max_incline_percent : float
        Maximum inline for uphills expressed as a percentage.
    max_decline_percent : float
        Maximum decline for downhills expressed as a percentage

    Methods
    -------
    calculate_fitness():
        Calculates the fitness of a route based on the set criteria.
    _calculate_desired_distance_score():
        Calculates the score for the desired distance criterion.
    _calculate_road_type_score():
        Calculates the score for the road type criterion.
    _calculate_number_of_junctions_score():
        Calculates the score for the number of junctions criterion.
    _calculate_complexity_of_junctions_score():
        Calculates the score for the complexity of junctions criterion.
    _calculate_turns_score():
        Calculates the score for the turns criterion.
    _calculate_uphill_sections_score():
        Calculates the score for the uphill sections criterion.
    _calculate_downhill_sections_score():
        Calculates the score for the downhill sections criterion.
    _calculate_number_of_lanes_score():
        Calculates the score for the number of lanes criterion.
    _calculate_one_way_routes_score():
        Calculates the score for the one-way routes criterion.
    _calculate_narrow_roads_score():
        Calculates the score for two-way traffic on narrow roads criterion.
    _calculate_downhills_with_lights():
        Calculates the score for downhill roads with traffic lights criterion.
    """

    def __init__(
        self,
        distance: numbers.Number,
        dist_variance: numbers.Number,
        max_incline_percent: numbers.Number,
        max_decline_percent: numbers.Number,
    ):
        """Create Fitness instance.

        Parameters
        ----------
        distance : numbers.Number
            The desired route distance in meters,
            where MIN_ROUTE_DISTANCE < distance <= MAX_ROUTE_DISTANCE
        dist_variance : numbers.Number
            The allowable variance for route distance, where
            MIN_DISTANCE_VARIANCE <= dist_variance <= MAX_DISTANCE_VARIANCE
        max_incline_percent : numbers.Number
            _description_
        max_decline_percent : numbers.Number
            _description_

        Raises
        ------
        ValueError
            If distance is not of type `numbers.Number`, or outside of the
            valid range.
        ValueError
            If dist_variance is not of type `numbers.Number`, or outside of the
            valid range.
        ValueError
            If max_incline_percent is not of type `numbers.Number`, or outside
            of the valid range.
        ValueError
            If max_decline_percent is not of type `numbers.Number`, or outside
            of the valid range.
        """
        if not self._is_valid_distance(distance):
            msg = (
                f"{distance} must be "
                f"MIN_ROUTE_DISTANCE <= distance <= MAX_ROUTE_DISTANCE"
            )
            raise ValueError(msg)
        self.distance = distance

        if not self._is_valid_dist_variance(dist_variance):
            msg = (
                f"{dist_variance} must be "
                f"MIN_DISTANCE_VARIANCE <= dist_variance <= "
                f"MAX_DISTANCE_VARIANCE"
            )
            raise ValueError(msg)
        self.dist_variance = dist_variance

        if not self._is_max_inclide_percent_valid(max_incline_percent):
            msg = (
                f"{max_incline_percent} must be a float value, where"
                f"0 <= max_incline_percent <= MAX_INCLINE_PERCENT"
            )
            raise ValueError(msg)
        self.max_inclide_percent = max_incline_percent

        if not self._is_max_decline_percent_valid(max_decline_percent):
            msg = (
                f"{max_decline_percent} must be a float value, where"
                f"0 <= max_decline_percent <= MAX_DECLINE_PERCENT"
            )
            raise ValueError(msg)
        self.max_decline_percent = max_decline_percent

        self.weights = {
            "desired_distance": 1,
            "road_type": 1,
            "number_of_junctions": 1,
            "junctions": 1,
            "turns": 1,
            "uphill_sections": 1,
            "downhill_sections": 1,
            "number_of_lanes": 1,
            "one_way_routes": 1,
            "narrow_roads": 1,
            "downhills_with_lights": 1,
        }

    def _is_max_inclide_percent_valid(
        self, max_inclide_percent: numbers.Number
    ):
        """Validate maximum incline.

        Parameters
        ----------
        max_inclide_percent : numbers.Number
            Max percentag inclide as a percentage

        Returns
        -------
        bool
            True if the incline is valid.
        """
        if not isinstance(max_inclide_percent, numbers.Number):
            return False
        return 0 <= max_inclide_percent <= MAX_INCLINE_PERCENT

    def _is_max_decline_percent_valid(
        self, max_decline_percent: numbers.Number
    ):
        """
        Validate maximum decline.

        Parameters
        ----------
        max_decline_percent : float
            Max decline inclide as a percentage

        Returns
        -------
        bool
            True if the decline is valid.
        """
        if not isinstance(max_decline_percent, numbers.Number):
            return False
        return 0 <= max_decline_percent <= MAX_DECLINE_PERCENT

    def _is_valid_dist_variance(self, dist_variance: numbers.Number):
        """
        Validate distance variance.

        Parameters
        ----------
        dist_variance : float
            The maximum allowed distance variance.

        Returns
        -------
        bool
            True id the dist_variance is within allowed parameters.
        """
        if not isinstance(dist_variance, numbers.Number):
            return False
        return MIN_DISTANCE_VARIANCE <= dist_variance <= MAX_DISTANCE_VARIANCE

    def _is_valid_distance(self, distance: numbers.Number):
        """
        Validate distance attribute.

        Parameters
        ----------
        distance : float
            Desired route distance

        Returns
        -------
        bool
            True if the distance is within allowed parameters.
        """
        if not isinstance(distance, numbers.Number):
            return False
        return MIN_ROUTE_DISTANCE <= distance <= MAX_ROUTE_DISTANCE

    def _calculate_desired_distance_score(self) -> float:
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
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_road_type_score(self) -> float:
        """
        Calculate and return the score for the road type criterion.

        This method calculates the score based on the types of roads in the
        route. Different types of roads have different fitness impacts. Some
        roads are preferable to others and contribute to a higher score.

        Returns
        -------
        float
            The score for the road type criterion. The score is higher for
            preferable road types and lower for less preferable ones.
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_number_of_junctions_score(self) -> float:
        """
        Calculate and return the score for the number of junctions criterion.

        This method calculates the score based on the number of junctions along
        the route. Fewer junctions are generally preferable and contribute to a
        higher score.

        Returns
        -------
        float
            The score for the number of junctions criterion. The score is
            higher for routes with fewer junctions.
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_complexity_of_junctions_score(self) -> float:
        """
        Calculate and return the score for complex junctions criterion.

        This method calculates the score based on the complexity of junctions
        along the route. Less complex junctions are generally preferable and
        contribute to a higher score.

        Returns
        -------
        float
            The score for the complexity of junctions criterion. The score is
            higher for routes with less complex junctions.
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_turns_score(self) -> float:
        """
        Calculate and return the score for the turns criterion.

        This method calculates the score based on the turns along the route.
        Certain turns, such as not crossing other roads when turning from one
        road into another, are generally preferable and contribute to a higher
        score.

        Returns
        -------
        float
            The score for the turns criterion. The score is higher for routes
            with preferable turns.
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_uphill_sections_score(self) -> float:
        """
        Calculate and return the score for the uphill sections criterion.

        This method calculates the score based on the uphill sections along the
        route. Uphill sections negatively impact route fitness. If it is
        steeper than a certain angle, it is deemed unfit and a score of
        negative infinity (`float('-inf')`) is returned.

        Returns
        -------
        float
            The score for the uphill sections criterion. If an uphill section
            is steeper than a certain angle, it returns negative infinity
              (`float('-inf')`).
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_downhill_sections_score(self) -> float:
        """
        Calculate and return the score for the downhill sections criterion.

        This method calculates the score based on the downhill sections along
        the route. Downhill sections positively impact fitness, up to a certain
        limit. Exceeding that limit deems it unfit and a score of negative
        infinity (`float('-inf')`) is returned.

        Returns
        -------
        float
            The score for the downhill sections criterion. If a downhill
            section exceeds a certain limit, it returns negative infinity
            (`float('-inf')`).
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_number_of_lanes_score(self) -> float:
        """
        Calculate and return the score for the number of lanes criterion.

        This method calculates the score based on the number of lanes on the
        roads in the route. More lanes generally contribute to a higher score.

        Returns
        -------
        float
            The score for the number of lanes criterion. The score is higher
            for routes with more lanes.
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_one_way_routes_score(self) -> float:
        """
        Calculate and return the score for the one-way routes criterion.

        This method calculates the score based on the presence of one-way
        routes in the route. One-way routes generally contribute to a higher
        score.

        Returns
        -------
        float
            The score for the one-way routes criterion. The score is higher for
            routes with more one-way routes.
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_narrow_roads_score(self) -> float:
        """
        Calculate and return the score for the two-way roads.

        This method calculates the score based on the presence of two-way
        traffic on narrow roads in the route. Two-way traffic on narrow roads
        generally contributes to a lower score.

        Returns
        -------
        float
            The score for the two-way traffic on narrow roads criterion. The
            score is lower for routes with more two-way traffic on narrow roads.
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def _calculate_downhills_with_lights(self) -> float:
        """
        Calculate and return the score for the downhill roads with lights.

        This method calculates the score based on the presence of downhill
        roads with traffic lights in the route. Downhill roads with traffic
        lights generally contribute to a lower score.

        Returns
        -------
        float
            The score for the downhill roads with traffic lights criterion. The
            score is lower for routes with more downhill roads with traffic
            lights.
        """
        # TODO: Implement this method based on your specific requirements
        return 0

    def calculate_fitness(self, route_attributes: Dict) -> float:
        """
        Calculate route fitness score.

        This method calculates the fitness of a route by summing up the
        weighted scores for each criterion. If any hard criteria are not
        met (e.g., exceeding allowable distance range or uphill steepness),
        then fitness is set to negative infinity (`float('-inf')`).

        Parameters
        ----------
        data : dict
            A dictionary containing the graph and route. The graph represents
            road infrastructure and the route is a list of nodes describing a
            route along the graph.

        Returns
        -------
        float
            The fitness value of the route. If any hard criteria are not met,
            it returns negative infinity (`float('-inf')`).
        """
        fitness = 0.0

        # Calculate scores for each criterion based on the route and graph
        scores = {
            "desired_distance": self._calculate_desired_distance_score(),
            "road_type": self._calculate_road_type_score(),
            "number_of_junctions": self._calculate_number_of_junctions_score(),
            "junctions": self._calculate_complexity_of_junctions_score(),
            "turns": self._calculate_turns_score(),
            "uphill_sections": self._calculate_uphill_sections_score(),
            "downhill_sections": self._calculate_downhill_sections_score(),
            "number_of_lanes": self._calculate_number_of_lanes_score(),
            "one_way_routes": self._calculate_one_way_routes_score(),
            "narrow_roads": self._calculate_narrow_roads_score(),
            "downhills_with_lights": self._calculate_downhills_with_lights(),
        }

        # Check if any hard criteria are not met
        if scores["desired_distance"] == float("-inf") or scores[
            "uphill_sections"
        ] == float("-inf"):
            return float("-inf")

        # Calculate total fitness score
        for criterion, weight in self.weights.items():
            fitness += weight * scores[criterion]

        return fitness
