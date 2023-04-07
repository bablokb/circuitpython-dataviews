# ----------------------------------------------------------------------------
# listview_pygame.py
#
# ListView example using a pygame-display.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

ITEMS = 10

import board
import time
import busio
import displayio

from dataviews.Base import Color, Justify
from dataviews.DisplayFactory import DisplayFactory
from dataviews.ListView import ListView
from dataviews.LabelItem import LabelItem

# always release displays (unless you use a builtin-display)
if not hasattr(board,'DISPLAY'):
  displayio.release_displays()

# create display
if hasattr(board,'DISPLAY'):
  display = board.DISPLAY
else:
  display = DisplayFactory.pygame(width=600,height=400,native_frames_per_second=2)

# create view
view = ListView(
  width=display.width,
  height=display.height,
  #item_width=int(0.7*display.width),
  justify=Justify.CENTER,
  bg_color=Color.GREEN,
  border=1,
)
display.show(view)

item_factory = LabelItem(
  color=Color.BLUE,
  bg_color = Color.WHITE,
  border = 2,
  padding = 5,
  justify = Justify.LEFT,
  fontname="fonts/DejaVuSansMono-Bold-24-subset.bdf",
)

items = []
for i in range(ITEMS):
  if i%2 == 0:
    items.append(item_factory.create(text=f"item: {i}"))
  else:
    items.append(item_factory.create(text=f"long item: {i}"))
view.add_items(items)
view.layout()

def test_focus(nr):
  view.set_focus(nr)

def test_select(nr):
  view.set_selection(nr)
  
tests = [test_select]
i = 0
tnr = 0
tst = tests[tnr]

def on_time():
  global i, tnr, tst
  print(f"test: {tnr}, item: {i}")
  tst(i)
  view.layout()
  i = (i+1)%ITEMS
  if i == 0:
    tnr = (tnr+1)%len(tests)
    tst = tests[tnr]

display.event_loop(interval=1,on_time=on_time)
