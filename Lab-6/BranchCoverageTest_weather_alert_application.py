import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# Branch coverage: drive every decision in weather_alert.py to both True and
# False, using the exact threshold values and the values just below them.


# wind_alert: speed >= 89 / >= 62 / >= 39
@pytest.mark.parametrize("speed, expected", [
    (89, "warning"),     # >= 89 True at the boundary
    (88.9, "watch"),     # >= 89 False, >= 62 True
    (62, "watch"),       # >= 62 True at the boundary
    (61.9, "advisory"),  # >= 62 False, >= 39 True
    (39, "advisory"),    # >= 39 True at the boundary
    (38.9, "none"),      # all conditions False
    (0, "none"),
])
def test_wind_alert_thresholds(speed, expected):
    assert wind_alert(speed) == expected


# rain_alert: mm_per_hour >= 50 / >= 10, each combined with soil_saturated
@pytest.mark.parametrize("mm, saturated, expected", [
    (50, True, "warning"),       # >= 50 True,  saturated True
    (50, False, "watch"),        # >= 50 True,  saturated False
    (49.9, True, "watch"),       # >= 50 False, >= 10 True, saturated True
    (49.9, False, "advisory"),   # >= 50 False, >= 10 True, saturated False
    (10, True, "watch"),         # >= 10 True at the boundary
    (10, False, "advisory"),
    (9.9, True, "none"),         # both rate checks False; soil irrelevant
    (9.9, False, "none"),
    (0, False, "none"),
])
def test_rain_alert_rate_and_soil_combinations(mm, saturated, expected):
    assert rain_alert(mm, saturated) == expected


# heat_alert: humidity > 40 adjustment, then index >= 45 / >= 40 / >= 35
@pytest.mark.parametrize("temp, humidity, expected", [
    (45, 40, "warning"),    # humidity > 40 False, index >= 45 True
    (44.9, 40, "watch"),    # index >= 45 False, >= 40 True
    (40, 0, "watch"),
    (39.9, 40, "advisory"), # index >= 40 False, >= 35 True
    (35, 40, "advisory"),
    (34.9, 40, "none"),     # all index checks False
])
def test_heat_alert_without_humidity_adjustment(temp, humidity, expected):
    assert heat_alert(temp, humidity) == expected


@pytest.mark.parametrize("temp, humidity, expected", [
    (40, 90, "warning"),    # 40 + 50 * 0.1 = 45  -> raised from watch
    (35, 90, "watch"),      # 35 + 5.0 = 40       -> raised from advisory
    (30, 90, "advisory"),   # 30 + 5.0 = 35       -> raised from none
    (30, 60, "none"),       # 30 + 2.0 = 32       -> adjusted but still none
])
def test_heat_alert_with_humidity_adjustment(temp, humidity, expected):
    assert heat_alert(temp, humidity) == expected


def test_heat_alert_humidity_boundary():
    # humidity == 40 is not adjusted; 41 adds 0.1 and crosses the threshold
    assert heat_alert(34.95, 40) == "none"
    assert heat_alert(34.95, 41) == "advisory"


# overall_alert: loop entered / skipped, unknown alert, severity comparison
def test_overall_empty_list_skips_loop():
    assert overall_alert([]) == "none"

def test_overall_all_none_never_updates_worst():
    assert overall_alert(["none", "none"]) == "none"

def test_overall_single_alert():
    assert overall_alert(["watch"]) == "watch"

def test_overall_ascending_order_updates_each_time():
    assert overall_alert(["none", "advisory", "watch", "warning"]) == "warning"

def test_overall_descending_order_keeps_first_worst():
    assert overall_alert(["warning", "watch", "advisory", "none"]) == "warning"

def test_overall_equal_severity_does_not_change_result():
    assert overall_alert(["advisory", "advisory"]) == "advisory"

def test_overall_unknown_alert_after_valid_alerts_raises():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["advisory", "warning", "hurricane"])

def test_overall_alert_names_are_case_sensitive():
    with pytest.raises(ValueError):
        overall_alert(["Warning"])

def test_overall_combines_individual_alerts():
    alerts = [wind_alert(70), rain_alert(15, False), heat_alert(30, 40)]
    assert alerts == ["watch", "advisory", "none"]
    assert overall_alert(alerts) == "watch"
