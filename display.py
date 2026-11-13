import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from fsm import STATE_TEMPERATURE, STATE_HUMIDITY, STATE_DISTANCE, state_to_bits

OLED_WIDTH = 128
OLED_HEIGHT = 64


def init_display(i2c, addr=0x3C):
    """Initialize the 128x64 SSD1306 OLED display."""
    try:
        oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=addr)
        image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        return oled, image, draw, font
    except Exception as error:
        print(f"Warning: OLED initialization failed: {error}")
        return None, None, None, None


def render_mode(oled, image, draw, font, state, temp_c, humidity, dist_cm):
    """Render the currently selected FSM state reading onto the OLED."""
    if oled is None:
        return

    try:
        draw.rectangle((0, 0, OLED_WIDTH, OLED_HEIGHT), outline=0, fill=0)
        draw.text((0, 0), f"DAQ MONITOR [{state_to_bits(state)}]", font=font, fill=255)

        if state == STATE_TEMPERATURE:
            draw.text((0, 20), "MODE: Temperature", font=font, fill=255)
            val_text = f"Temp: {temp_c:.1f} C" if temp_c is not None else "Temp: Sensor Error"
            draw.text((0, 42), val_text, font=font, fill=255)

        elif state == STATE_HUMIDITY:
            draw.text((0, 20), "MODE: Humidity", font=font, fill=255)
            val_text = f"Humidity: {humidity:.1f} %" if humidity is not None else "Hum: Sensor Error"
            draw.text((0, 42), val_text, font=font, fill=255)

        elif state == STATE_DISTANCE:
            draw.text((0, 20), "MODE: Distance", font=font, fill=255)
            val_text = f"Dist: {dist_cm:.1f} cm" if dist_cm is not None else "Dist: Out of Range"
            draw.text((0, 42), val_text, font=font, fill=255)

        oled.image(image)
        oled.show()
    except Exception as error:
        print(f"OLED render error: {error}")


def show_shutdown(oled, image, draw, font):
    """Display an offline status message on the OLED prior to exit."""
    if oled is None:
        return

    try:
        draw.rectangle((0, 0, OLED_WIDTH, OLED_HEIGHT), outline=0, fill=0)
        draw.text((0, 25), "System Offline", font=font, fill=255)
        oled.image(image)
        oled.show()
    except Exception:
        pass
