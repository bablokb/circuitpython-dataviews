# ----------------------------------------------------------------------------
# simple_test_1306.py
#
# A simple test for the 1306-display.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import time
import board
import displayio
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView import DataView

# always release displays (unless you use a builtin-display)
if not hasattr(board,'DISPLAY'):
  displayio.release_displays()

# create display (choose your type!)
if hasattr(board,'DISPLAY'):
  display = board.DISPLAY
else:
  display = DisplayFactory.ssd1306()

# create view
view = DataView(
  dim=(3,2),
  width=display.width,height=display.height,
  justify=DataView.CENTER,
  formats=["min:","{0:.1f}mV",
           "avg:","{0:.1f}mV",
           "max:","{0:.1f}mV"],
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
  time.sleep(1)

while True:
  time.sleep(10)
