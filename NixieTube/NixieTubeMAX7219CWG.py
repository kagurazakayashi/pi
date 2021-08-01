# https://luma-led-matrix.readthedocs.io/en/latest/python-usage.html#segment-led-displays
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
import time

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)
seg.text = "12345678"
time.sleep(1)