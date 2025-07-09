# ----------------------------------------------------------------------------
# pygame_dev.py
#
# A simple test for a pygame-display simulating a 7789-display.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import threading
import board
import time
import busio
import displayio

from dataviews.Base import Color, Justify
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView import DataView

WIDTH  = 240
HEIGHT = 135
AUTO_REFRESH = True

# --- various tests (returns seconds to wait after test)   -------------------

view = None
tests = []
def init():
  """ create view """
  global view

  print("creating view")
  view = DataView(
    dim=(3,2),
    width=WIDTH,height=HEIGHT,
    col_width=[0.3,0.7],
    justify=Justify.CENTER,
    color=Color.GREEN,
    fontname="fonts/DejaVuSansMono-Bold-24-subset.bdf",
    formats=["min:","{0:.1f}mV",
             "avg:","{0:.1f}mV",
             "max:","{0:.1f}mV"],
    border=1,
    divider=1,
    padding=5,
  )
  return 3

def test1():
  """ show initial values """
  global view
  print("show initial values")
  view.set_values(
    [None,  7.1,
     None, 22.3,
     None, 30.8]
  )
  return 3
tests.append(test1)

def test2():
  """ invert """
  global view
  print("invert display")
  view.invert()
  return 3
tests.append(test2)
tests.append(test2)

def test3():
  """ justify right """
  global view
  print("justify right")
  view.justify(Justify.RIGHT)
  return 3
tests.append(test3)

def test4():
  """ realign first column """
  global view
  for index in [0,2,4]:
    print(f"realign column {index}")
    view.justify(Justify.LEFT,index)
    view.set_color(Color.BLUE,index)
  return 1
tests.append(test4)

def test5():
  """ set dynamic colors """
  global view
  for index in [1,3,5]:
    print(f"set color for column {index}")
    view.set_color(index=index,
                   color=[(Color.BLUE,15),
                                (Color.WHITE,24),(Color.RED,None)])
  return 0
tests.append(test5)

# --- update values   --------------------------------------------------------

i = 0
def update_values():
  global i, view
  view.set_values([None,i,
                   None,2.0*i/3.0,
                   None,30-i])
  print("updating values")
  i = (i+1)%30
  return 1

# --- main program   --------------------------------------------------------- 

# Make the display context
main_group = displayio.Group()
init()
main_group.append(view)
display = DisplayFactory.pygame(width=WIDTH,height=HEIGHT,
                                native_frames_per_second=10,
                                auto_refresh=AUTO_REFRESH)
display.root_group = main_group

finished = False
while not finished:
  print("------------------")
  for test in tests:
    wait = test()
    if not AUTO_REFRESH:
      display.refresh()
    print("------------------")
    end = time.monotonic() + wait
    while time.monotonic() < end:
      if display.check_quit():
        finished = True
        break
    if finished:
      break

  while not finished:
    wait = update_values()
    if not AUTO_REFRESH:
      display.refresh()
    end = time.monotonic() + wait
    while time.monotonic() < end:
      if display.check_quit():
        finished = True
        break
