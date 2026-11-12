import math
import unicodedata

# Characters that render as blank space but are not treated as whitespace by
# str.strip() or float(): Hangul/halfwidth fillers and the braille blank.
_BLANK_FILLERS = {chr(0x115F), chr(0x1160), chr(0x2800), chr(0x3164), chr(0xFFA0)}


def _clean(value):
    """Remove invisible characters (zero-width spaces, BOM, soft hyphen, ...)
    that often sneak in via copy-paste, then strip surrounding whitespace."""
    return ''.join(
        c for c in value
        if unicodedata.category(c) != 'Cf' and c not in _BLANK_FILLERS
    ).strip()


def _require_text(value, name):
    """Return value cleaned of invisible characters and surrounding
    whitespace, or raise ValueError."""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string, got {type(value).__name__}")
    value = _clean(value)
    if not value:
        raise ValueError(f"{name} must not be empty")
    return value


def parse_reading(text):
    text = _require_text(text, "reading")
    parts = text.split('/')
    if len(parts) != 2:
        raise ValueError(f"reading must be 'temperature/humidity', got {text!r}")

    temp_text, humidity_text = (_clean(p) for p in parts)
    if not temp_text or not humidity_text:
        raise ValueError(f"temperature and humidity must not be empty: {text!r}")

    temp = float(temp_text)
    if not math.isfinite(temp):
        raise ValueError(f"temperature must be a finite number, got {temp_text!r}")

    humidity = int(humidity_text)
    if not 0 <= humidity <= 100:
        raise ValueError(f"humidity must be between 0 and 100, got {humidity}")

    return temp, humidity


def wind_category(speed_text):
    speed_text = _require_text(speed_text, "wind speed")
    speed = int(speed_text)
    if speed < 0:
        raise ValueError(f"wind speed must not be negative, got {speed}")
    if speed >= 89:
        return 'warning'
    if speed >= 39:
        return 'advisory'
    return 'none'


def rainfall_spread(readings_csv):
    readings_csv = _require_text(readings_csv, "rainfall readings")
    readings = []
    for field in readings_csv.split(','):
        field = _clean(field)
        if not field:
            raise ValueError(f"empty rainfall reading in {readings_csv!r}")
        value = float(field)
        if not math.isfinite(value):
            raise ValueError(f"rainfall reading must be finite, got {field!r}")
        if value < 0:
            raise ValueError(f"rainfall reading must not be negative, got {field!r}")
        readings.append(value)
    return max(readings) - min(readings)


def main():
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    print("Temperature and Humidity:", result)

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    print("Wind Category:", result)

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    print("Rainfall Spread:", result)

if __name__ == "__main__":
    main()
