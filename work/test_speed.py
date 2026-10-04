"My own tests for minutes_per_km."

import pytest

from orders import minutes_per_km


def test_slow_delivery():
    # Assert that 60 minutes over 6 km is 10.0
    assert minutes_per_km(60, 6) == 10.0


def test_negative_distance_raises():
    # Assert that a distance of -3 raises ValueError
    with pytest.raises(ValueError):
        minutes_per_km(30, -3)
