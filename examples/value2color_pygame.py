# ----------------------------------------------------------------------------
# value2color-pygame.py
#
# A sample application for the DataPanel class. This program simulates a
# Inky-Pack.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import board
import time
import sys

from dataviews.Base import Color, Justify
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView  import DataView
from dataviews.DataPanel import DataPanel, PanelText


# color callback
def value2color(index,value):
  # print all labels in AQUA
  if index in [0,2,4,6]:
    return Color.AQUA
  elif value is not None and value > 30:
    return Color.RED
  else:
    return Color.BLACK

# create display
display = DisplayFactory.pygame(width=296,height=128,native_frames_per_second=1)
display.auto_refresh=False

# create view and panel
_formats = ['Bat:', '{0:0.1f}V',
            'T1:', '{0:.1f}°C',
            'Hum:', '{0:.0f}%rH',
            'T2:', '{0:.1f}°C']
dim = (3,4)

width = 280
#col_width = [int(width/4) for _ in range(4)]
#col_width = [50,90,35,90]
#col_width = None
#col_width = 'AUTO'
col_width = [0,0.5,0,0.5]

_formats.extend(
  ["" for _ in range(dim[0]*dim[1] - len(_formats))])
_view = DataView(
  dim=dim,
  width=width,height=int(0.6*display.height),
  col_width=col_width,
  fontname="fonts/DejaVuSansMono-Bold-18-subset.bdf",
  formats=_formats,
  border=1,
  divider=1,
  padding=1,
  color=Color.BLACK,
  bg_color=Color.WHITE,
  value2color=value2color
  )

for i in range(0,dim[0]*dim[1],2):
  _view.justify(Justify.LEFT,index=i)
  _view.justify(Justify.RIGHT,index=i+1)

_title = PanelText(text=f"Logger: 001",
                  fontname="fonts/DejaVuSansMono-Bold-18-subset.bdf",
                  justify=Justify.CENTER)

_footer = PanelText(text=f"at 2023-06-28 11:22:06 SD",
                      fontname="fonts/DejaVuSansMono-Bold-18-subset.bdf",
                      justify=Justify.RIGHT)
_panel = DataPanel(
  width=display.width,
  height=display.height,
  view=_view,
  title=_title,
  footer=_footer,
  border=1,
  padding=5,
  justify=Justify.CENTER,
  color=Color.BLACK,
  bg_color=Color.WHITE
)

values = [None,2.9,
          None,23.2,
          None,44,
          None,23.1]

# fill in unused cells
values.extend([None for _ in range(len(_formats)-len(values))])

_view.set_values(values)
print("starting show()")
display.show(_panel)
print("starting refresh()")
display.refresh()
print("finished")

while True:
  if display.check_quit():
    sys.exit(0)
  time.sleep(0.1)
