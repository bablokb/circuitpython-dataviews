# ----------------------------------------------------------------------------
# simple_test_7789.py
#
# A simple test for the 7789-display.
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
  # Pimoroni Display-Pack
  #display = DisplayFactory.display_pack()

  # Adafruit 240x320
  display = DisplayFactory.st7789(
    spi=busio.SPI(clock=board.GP14,MOSI=board.GP15),
    pin_dc=board.GP9,
    pin_cs=board.GP13,
    pin_rst=board.GP11,
    width=320, height=240, rotation=270,
    backlight_pin=board.GP10,
    brightness=0.6,
  )

# create view
view = DataView(
  dim=(3,2),
  width=display.width,height=display.height,
  justify=Justify.CENTER,
  color=Color.GREEN,
  fontname="fonts/DejaVuSansMono-Bold-24-subset.bdf",
  formats=["min:","{0:.1f}mV",
           "avg:","{0:.1f}mV",
           "max:","{0:.1f}mV"],
  border=1,
  divider=1,
  padding=10,
)

# show without values
if hasattr(display,"root_group"):
  display.root_group = view
else:
  display.show(view)
time.sleep(3)

# now set values
view.set_values(
  [None,  7.1,
   None, 22.3,
   None, 30.8]
)
time.sleep(3)

# flip background/forground
view.invert()
time.sleep(3)
view.invert()
time.sleep(3)

# realign all fields
view.justify(Justify.RIGHT)
time.sleep(3)

# realign only fields in first column
for index in [0,2,4]:
  view.justify(Justify.LEFT,index)
  view.set_color(Color.BLUE,index)
  time.sleep(1)

# set dynamic colors
for index in [1,3,5]:
  view.set_color(index=index,
                 color_range=[(Color.BLUE,15),
                              (Color.WHITE,24),(Color.RED,None)])
time.sleep(3)

while True:
  for i in range(30):
    view.set_values([None,i,
                     None,2.0*i/3.0,
                     None,30-i])
    time.sleep(1)
