import time
from datetime import datetime
import RPi.GPIO as GPIO

from fsm import STATE_TEMPERATURE, next_state, state_to_bits
from sensors import init_sensors, measure_aht21, measure_distance
from display import init_display, render_mode, show_shutdown
from data_logger import init_csv, log_measurement

# --- Hardware Pin Configuration (BCM Numbering) ---
BUTTON_PIN = 27
TRIG_PIN = 23
ECHO_PIN = 22

# --- Timing Constants ---
SAMPLE_INTERVAL_S = 1.0
LOOP_SLEEP_S = 0.02
DEBOUNCE_DELAY_S = 0.25
CSV_FILE = "sensor_log.csv"


def setup_gpio():
    """Configure GPIO pins for the push button and HC-SR04 sensor."""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)


def main():
    setup_gpio()
    i2c, aht21 = init_sensors()
    oled, image, draw, font = init_display(i2c)
    init_csv(CSV_FILE)

    current_state = STATE_TEMPERATURE
    last_button_state = GPIO.input(BUTTON_PIN)
    last_press_time = 0.0

    start_time = time.monotonic()
    last_sample_time = start_time - SAMPLE_INTERVAL_S  # Trigger immediate first reading

    # Cache latest readings so button presses update the OLED immediately
    latest_temp = None
    latest_humidity = None
    latest_dist = None

    print(f"DAQ System running (Initial State: S0 / {state_to_bits(current_state)}). Press Ctrl+C to stop.")

    try:
        while True:
            now = time.monotonic()

            # 1. Debounced Push-Button Polling (Active-Low with Internal Pull-Up)
            button_state = GPIO.input(BUTTON_PIN)
            if last_button_state == GPIO.HIGH and button_state == GPIO.LOW:
                if (now - last_press_time) >= DEBOUNCE_DELAY_S:
                    current_state = next_state(current_state)
                    last_press_time = now
                    print(f"Mode changed -> {state_to_bits(current_state)}")
                    render_mode(
                        oled, image, draw, font,
                        current_state, latest_temp, latest_humidity, latest_dist
                    )
            last_button_state = button_state

            # 2. Periodic Sensor Acquisition & CSV Logging (1-Second Interval)
            if (now - last_sample_time) >= SAMPLE_INTERVAL_S:
                last_sample_time = now
                elapsed_s = round(now - start_time, 2)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                latest_temp, latest_humidity = measure_aht21(aht21)
                latest_dist = measure_distance(TRIG_PIN, ECHO_PIN)

                log_measurement(
                    CSV_FILE,
                    timestamp,
                    elapsed_s,
                    latest_temp,
                    latest_humidity,
                    latest_dist
                )

                render_mode(
                    oled, image, draw, font,
                    current_state, latest_temp, latest_humidity, latest_dist
                )

            time.sleep(LOOP_SLEEP_S)

    except KeyboardInterrupt:
        print("\nShutting down DAQ system...")
    finally:
        show_shutdown(oled, image, draw, font)
        GPIO.cleanup()
        print("GPIO cleaned up. Exit complete.")


if __name__ == "__main__":
    main()
