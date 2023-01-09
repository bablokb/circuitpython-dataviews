# ----------------------------------------------------------------------------
# pyportal-datapanel.py
#
# A sample application for the DataPanel class.
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

from adafruit_adt7410 import ADT7410

from dataviews.Base import Color, Justify
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView  import DataView
from dataviews.DataPanel import DataPanel, PanelText

# always release displays (unless you use a builtin-display)
if not hasattr(board,'DISPLAY'):
  displayio.release_displays()

# create display
if hasattr(board,'DISPLAY'):
  display = board.DISPLAY
else:
  display = DisplayFactory.st7789(
    pin_dc=board.GP16,
    pin_cs=board.GP17,
    spi=busio.SPI(clock=board.GP18,MOSI=board.GP19)
  )

# create sensor
if hasattr(board,'I2C'):
  i2c = board.I2C()
else:
  i2c = busio.I2C(board.GP27,board.GP26)   # adapt to your needs
adt = ADT7410(i2c, address=0x48)
adt.high_resolution = True

# create view with one row for temperature (label: value)
view = DataView(
  dim=(1,2),
  width=int(0.8*display.width),height=int(display.height/3),
  justify=Justify.RIGHT,
  fontname="fonts/DejaVuSansMono-Bold-32-subset.bdf",
  formats=["Temp:",
           "{0:.1f}°C"],
  border=1,
  divider=0,
  bg_color=Color.BLUE
)
view.justify(Justify.RIGHT,index=0)
view.justify(Justify.LEFT,index=1)
view.set_color(color=Color.SILVER,index=1)
view.set_values([None,adt.temperature])

# create DataPanel
panel = DataPanel(
  width=display.width,
  height=display.height,
  view=view,
  title=PanelText(text="PyPortal",color=Color.FUCHSIA,
                  fontname="fonts/DejaVuSansMono-Bold-52-subset.bdf",
                  justify=Justify.CENTER),
  footer=PanelText(text="https://github.com/bablokb/circuitpython-dataviews",
                   color=Color.SILVER),
  border=1,
  padding=5,
  justify=Justify.CENTER,
  )

display.show(panel)

while True:
  view.set_values([None,adt.temperature])
  time.sleep(5)
