# ----------------------------------------------------------------------------
# simple_test_pygame.py
#
# A simple test for a pygame-display simulating a 7789-display.
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
  display = DisplayFactory.pygame(width=240,height=135,native_frames_per_second=1)

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

i = 0
def on_time():
  global i
  view.set_values([None,i,
                   None,2.0*i/3.0,
                   None,30-i])
  i = (i+1)%30

display.event_loop(interval=1,on_time=on_time)
