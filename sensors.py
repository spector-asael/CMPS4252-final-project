import time
import board
import busio
import adafruit_ahtx0


def init_sensors():
    """Initialize the shared I2C bus and AHT21 sensor with retries."""
    i2c = busio.I2C(board.SCL, board.SDA)
    time.sleep(0.5)

    aht21 = None
    for attempt in range(3):
        try:
            aht21 = adafruit_ahtx0.AHTx0(i2c)
            print("AHT21 sensor initialized successfully.")
            break
        except Exception as error:
            print(f"AHT21 init attempt {attempt + 1} failed: {error}")
            time.sleep(0.5)

    if not aht21:
        print("Warning: AHT21 unavailable; temperature/humidity will log as empty.")

    return i2c, aht21


def measure_aht21(aht21):
    """Read temperature (°C) and relative humidity (%) from AHT21, or return (None, None)."""
    if not aht21:
        return None, None

    try:
        temp_c = round(float(aht21.temperature), 2)
        humidity = round(float(aht21.relative_humidity), 2)
        return temp_c, humidity
    except Exception as error:
        print(f"AHT21 read error: {error}")
        return None, None


def measure_distance(trig_pin, echo_pin, timeout_s=0.04):
    """Trigger HC-SR04 and return distance in cm, or None on timeout/out-of-range."""
    import RPi.GPIO as GPIO

    GPIO.output(trig_pin, True)
    time.sleep(0.00001)  # 10 us trigger pulse
    GPIO.output(trig_pin, False)

    deadline = time.monotonic() + timeout_s
    pulse_start = time.monotonic()

    while GPIO.input(echo_pin) == 0:
        pulse_start = time.monotonic()
        if pulse_start > deadline:
            return None

    pulse_end = pulse_start
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.monotonic()
        if pulse_end > deadline:
            return None

    pulse_duration = pulse_end - pulse_start
    distance_cm = (pulse_duration * 34300.0) / 2.0

    # HC-SR04 reliable physical range is 2 cm to 400 cm
    if 2.0 <= distance_cm <= 400.0:
        return round(distance_cm, 2)
    return None
