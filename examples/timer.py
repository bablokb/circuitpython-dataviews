# ----------------------------------------------------------------------------
# timer.py: display a running timer on a 1306-display.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import time
import displayio
from dataviews.SSD1306DataDisplay import SSD1306DataDisplay
from dataviews.DataView import DataView

# always release displays!
displayio.release_displays()

# create new display with integrated view
display = SSD1306DataDisplay(
  dim=(1,1),
  justify=DataView.CENTER,
  bg_color=DataView.WHITE,
  color=DataView.BLACK,
  fontname="fonts/DejaVuSansMono-Bold-32-subset.bdf",
  formats=["{0}"]
)
view = display.get_view()

# for other displays, e.g. builtin displays use
#import board
#display = board.DISPLAY
#view = DataView(
#  dim=(1,1),
#  width=display.width,
#  height=display.height,
#  justify=DataView.CENTER,
#  bg_color=DataView.WHITE,
#  color=DataView.BLACK,
#  fontname="fonts/DejaVuSansMono-Bold-32-subset.bdf",
#  formats=["{0}"]
#)

# --- format timer   ---------------------------------------------------------

def pp_timer(seconds):
  """ pretty-print timer """
  m, s = divmod(seconds,60)
  h, m = divmod(m,60)
  if h > 0:
    return "{0:02d}:{1:02d}:{2:02d}".format(h,m,s)
  else:
    return "{0:02d}:{1:02d}".format(m,s)

# --- main   -----------------------------------------------------------------

timer    = 0
values   = ["00:00"]

start = time.monotonic()
view.set_values(values)
display.show(view)    # SSD1306DataDisplay also implements: display.show_view()

while True:
  overhead = time.monotonic() - start
  time.sleep(max(0,1-overhead))

  start = time.monotonic()
  timer += 1
  values[0] = pp_timer(timer)
  view.set_values(values)
