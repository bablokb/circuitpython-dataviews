# ----------------------------------------------------------------------------
# st7789_aht20.py
#
# Display sensor-values on a ST7789-display. The code assumes a 240x135 display,
# like Pimoroni's Pico Display Pack or Adafruit's 240x135-display with this
# chip.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import board
import time
import busio
import displayio

import adafruit_ahtx0          # AHT20

from dataviews.Base import Color, Justify
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView import DataView

# always release displays (unless you use a builtin-display)
if not hasattr(board,'DISPLAY'):
  displayio.release_displays()

# create display
if hasattr(board,'DISPLAY'):
  display = board.DISPLAY
else:
  display = DisplayFactory.display_pack()

# create sensor
if hasattr(board,'I2C'):
  i2c = board.I2C()
else:
  i2c = busio.I2C(board.GP27,board.GP26)   # adapt to your needs
sensor = adafruit_ahtx0.AHTx0(i2c)

# create view with two rows for temperature and relative humidity
view = DataView(
  dim=(2,1),
  width=display.width,height=display.height,
  justify=Justify.RIGHT,
  fontname="fonts/DejaVuSansMono-Bold-32-subset.bdf",
  formats=["{0:.1f}°C",
           "{0:.0f}%"],
  border=1,
  divider=0,
  padding=10,
)
display.show(view)

while True:
  view.set_values([sensor.temperature,sensor.relative_humidity])
  time.sleep(5)
