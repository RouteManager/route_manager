"""Test test score calculators."""
import route_manager.score_calcs as calcs
import pytest


@pytest.mark.parametrize(
    "distance, actual, variance, result",
    [
        # 18km route, 5% (900m) variance either way.
        (18000, 18000, 900, 1.00),  # Exactely on target
        (18000, 17775, 900, 0.71),  #  225m under target
        (18000, 17550, 900, 0.52),  #  450m under target
        (18000, 17100, 900, 0.30),  #  900m under target
        (18000, 16200, 900, 0.12),  # 1800m under target
        (18000, 18225, 900, 0.71),  #  225m over target
        (18000, 18450, 900, 0.52),  #  450m over target
        (18000, 18900, 900, 0.30),  #  900m over target
        (18000, 19800, 900, 0.12),  # 1800m over target
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
    ) == pytest.approx(result, abs=1e-2)


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
