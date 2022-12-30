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
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView import DataView

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

# create view
view = DataView(
  dim=(3,2),
  width=display.width,height=display.height,
  justify=DataView.CENTER,
  color=DataView.GREEN,
  fontname="fonts/DejaVuSansMono-Bold-24-subset.bdf",
  formats=["min:","{0:.1f}mV",
           "avg:","{0:.1f}mV",
           "max:","{0:.1f}mV"],
  border=1,
  divider=1,
  padding=10,
)

# show without values
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
view.justify(DataView.RIGHT)
time.sleep(3)

# realign only fields in first column
for index in [0,2,4]:
  view.justify(DataView.LEFT,index)
  view.set_color(DataView.BLUE,index)
  time.sleep(1)

while True:
  time.sleep(10)
