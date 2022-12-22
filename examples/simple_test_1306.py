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
from dataviews.SSD1306DataDisplay import SSD1306DataDisplay
from dataviews.DataView import DataView

display = SSD1306DataDisplay(dim=(3,2))

view = display.get_view()
view.justify(DataView.CENTER)
view.set_units(
  ["min:","{0:.1f}mV",
   "avg:","{0:.1f}mV",
   "max:","{0:.1f}mV"]
)

view.set_values(
  [None,  7.1,
   None, 22.3,
   None, 30.8]
)

display.show()

while True:
  time.sleep(10)
