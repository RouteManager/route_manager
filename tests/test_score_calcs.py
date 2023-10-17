"""Test test score calculators."""
import route_manager.score_calcs as calcs
import pytest


@pytest.mark.parametrize(
    "distance, actual, variance, result",
    [
        (1000, 1000, 100, 1.0),
        (1000, 950, 100, 0.5),
        (1000, 900, 100, 0.0),
        (1000, 800, 100, float("-inf")),
        (1000, 1050, 100, 0.5),
        (1000, 1100, 100, 0.0),
        (1000, 1200, 100, float("-inf")),
        (1000, 100, 999, 0.09909),
        (1000, 1, 100, float("-inf")),
        (1, 1, 0.99, 1),
    ],
)
def test_calculate_distance_score(distance, actual, variance, result):
    """
    Test the distance score calculator.

    Parameters
    ----------
    distance : number.Numeric
        desired route distance
    actual : number.Numeric
        actual route distance
    variance : _type_
        allowable distance variance
    result : float
        calculated score
    """
    assert calcs.calculate_distance_score(
        distance, actual, variance
    ) == pytest.approx(result, abs=1e-5)


@pytest.mark.parametrize(
    "distance, actual, variance",
    [
        # Invalid variance
        (1000, 100, 0),
        (1000, 100, float("-inf")),
        (1000, 100, 1000),
        (1000, 100, float("inf")),
        (1000, 100, "foo"),
        # Invalid actuals
        (1000, -100, 100),
        (1000, 0, 100),
        (1000, float("-inf"), 100),
        (1000, float("inf"), 100),
        (1000, "foo", 100),
        # Invalid desired
        (0, 1000, 100),
        (1, 1000, 100),
        (float("-inf"), 1000, 100),
        (float("inf"), 1000, 100),
        ("foo", 1000, 100),
    ],
)
def test_calculate_distance_score_invalid(distance, actual, variance):
    """
    Test the distance score calculator for invalid values.

    Parameters
    ----------
    distance : number.Numeric
        desired route distance
    actual : number.Numeric
        actual route distance
    variance : _type_
        allowable distance variance
    result : float
        calculated score
    """
    with pytest.raises(ValueError):
        calcs.calculate_distance_score(distance, actual, variance)
