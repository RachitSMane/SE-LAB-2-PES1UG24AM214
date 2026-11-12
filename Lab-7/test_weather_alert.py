import math

from hypothesis import given, strategies as st
from weather_alert import parse_reading, wind_category, rainfall_spread

VALID_CATEGORIES = {'warning', 'advisory', 'none'}


# ---------------------------------------------------------------------------
# Starter fuzz tests: arbitrary text or None.
# ValueError is the only accepted way to reject malformed input.
# Any other exception (TypeError, AttributeError, IndexError, ...) is a defect
# and is deliberately NOT caught, so Hypothesis will report it.
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_reading_no_crash(s):
    try:
        result = parse_reading(s)
    except ValueError:
        return  # malformed input correctly rejected

    assert isinstance(result, tuple) and len(result) == 2
    temp, humidity = result
    assert isinstance(temp, float)
    assert isinstance(humidity, int)
    assert math.isfinite(temp), f"non-finite temperature accepted: {temp!r}"
    assert 0 <= humidity <= 100, f"impossible humidity accepted: {humidity!r}"


@given(st.text() | st.none())
def test_wind_category_no_crash(s):
    try:
        result = wind_category(s)
    except ValueError:
        return  # malformed input correctly rejected

    assert result in VALID_CATEGORIES, f"unknown category: {result!r}"


@given(st.text() | st.none())
def test_rainfall_spread_no_crash(s):
    try:
        result = rainfall_spread(s)
    except ValueError:
        return  # malformed input correctly rejected

    assert isinstance(result, float)
    assert math.isfinite(result), f"non-finite spread returned: {result!r}"
    assert result >= 0, f"negative spread returned: {result!r}"


# ---------------------------------------------------------------------------
# Additional property-based tests: well-formed but semantically invalid input.
# Random text almost never produces strings like "nan/5" or "-3", so these
# strategies build numeric strings directly to reach those edge cases.
# ---------------------------------------------------------------------------

@given(st.floats(allow_nan=True, allow_infinity=True), st.integers())
def test_parse_reading_numeric_values(temp, humidity):
    text = f"{temp}/{humidity}"
    try:
        result_temp, result_humidity = parse_reading(text)
    except ValueError:
        # Rejection is only correct for non-finite or out-of-range values.
        assert not math.isfinite(temp) or not 0 <= humidity <= 100, (
            f"valid reading rejected: {text!r}"
        )
        return

    assert math.isfinite(result_temp), f"non-finite temperature accepted: {text!r}"
    assert 0 <= result_humidity <= 100, f"impossible humidity accepted: {text!r}"
    assert result_temp == temp
    assert result_humidity == humidity


@given(st.integers())
def test_wind_category_thresholds(speed):
    try:
        result = wind_category(str(speed))
    except ValueError:
        assert speed < 0, f"valid wind speed rejected: {speed!r}"
        return

    assert speed >= 0, f"negative wind speed accepted: {speed!r} -> {result!r}"
    if speed >= 89:
        assert result == 'warning'
    elif speed >= 39:
        assert result == 'advisory'
    else:
        assert result == 'none'


@given(st.lists(st.floats(allow_nan=True, allow_infinity=True), min_size=1))
def test_rainfall_spread_numeric_values(readings):
    text = ",".join(str(r) for r in readings)
    valid = all(math.isfinite(r) and r >= 0 for r in readings)
    try:
        result = rainfall_spread(text)
    except ValueError:
        assert not valid, f"valid readings rejected: {text!r}"
        return

    assert valid, f"invalid readings accepted: {text!r} -> {result!r}"
    assert math.isfinite(result) and result >= 0
    assert result == max(readings) - min(readings)
