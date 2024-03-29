# ----------------------------------------------------------------------------
# timer-pygame.py: display a running timer on a pygame-display,
#                  simulating a 1306-display.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import board
import time
import displayio

from dataviews.Base import Color, Justify
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView import DataView

display = DisplayFactory.pygame(width=128,height=64)

# create view
view = DataView(
  dim=(1,1),
  width=display.width,height=display.height,
  justify=Justify.CENTER,
  bg_color=Color.WHITE,
  color=Color.BLACK,
  fontname="fonts/DejaVuSansMono-Bold-32-subset.bdf",
  formats=["{0}"],
)

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

view.set_values(values)
display.show(view)

def on_time():
  global timer
  timer += 1
  values[0] = pp_timer(timer)
  view.set_values(values)

display.event_loop(interval=1,on_time=on_time)
