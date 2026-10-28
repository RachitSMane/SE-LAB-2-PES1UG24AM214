import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# Code (line) coverage: execute every statement of weather_alert.py at least once.


# wind_alert
def test_wind_warning():
    assert wind_alert(120) == "warning"

def test_wind_watch():
    assert wind_alert(75) == "watch"

def test_wind_advisory():
    assert wind_alert(45) == "advisory"

def test_wind_none():
    assert wind_alert(20) == "none"


# rain_alert
def test_heavy_rain_saturated_soil_is_warning():
    assert rain_alert(60, True) == "warning"

def test_heavy_rain_dry_soil_is_watch():
    assert rain_alert(60, False) == "watch"

def test_moderate_rain_saturated_soil_is_watch():
    assert rain_alert(20, True) == "watch"

def test_moderate_rain_dry_soil_is_advisory():
    assert rain_alert(20, False) == "advisory"

def test_light_rain_is_none():
    assert rain_alert(2, False) == "none"


# heat_alert
def test_extreme_heat_is_warning():
    assert heat_alert(47, 30) == "warning"

def test_high_heat_is_watch():
    assert heat_alert(42, 30) == "watch"

def test_humid_heat_is_advisory():
    # 34 C at 60% humidity -> index 34 + 20 * 0.1 = 36
    assert heat_alert(34, 60) == "advisory"

def test_mild_temperature_is_none():
    assert heat_alert(25, 30) == "none"


# overall_alert
def test_overall_picks_worst_alert():
    assert overall_alert(["advisory", "warning", "watch"]) == "warning"

def test_overall_unknown_alert_raises():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["storm"])
