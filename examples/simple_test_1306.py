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

dim = (3,2)
display = SSD1306DataDisplay(dim=dim)

view = display.get_view()
view.justify(DataView.CENTER)
view.set_units(["{0:.0f}mV" for i in range(dim[0]*dim[1])])

display.show()

while True:
  time.sleep(10)
