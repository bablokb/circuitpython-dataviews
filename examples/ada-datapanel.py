# ----------------------------------------------------------------------------
# inky_pack-datapanel.py
#
# A sample application for the DataPanel class.
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
from dataviews.DataView  import DataView
from dataviews.DataPanel import DataPanel, PanelText
from dataviews.DisplayFactory import DisplayFactory

# always release displays (unless you use a builtin-display)
if not hasattr(board,'DISPLAY'):
  displayio.release_displays()

# create display
if hasattr(board,'DISPLAY'):
  display = board.DISPLAY
else:
  epd_cs    = board.GP9
  epd_dc    = board.GP8
  epd_reset = board.GP7
  epd_busy  = board.GP6
  epd_sck   = board.GP10
  epd_mosi  = board.GP11

  spi = busio.SPI(epd_sck,MOSI=epd_mosi)
  display = DisplayFactory.ada_2_13_mono(
    pin_dc=epd_dc,pin_cs=epd_cs,spi=spi,pin_rst=epd_reset,pin_busy=epd_busy)

FONT_NAME="DejaVuSans-16-subset.bdf"

# create view and panel
_formats = ['Bat', '{0:0.1f}V',
            'T1:', '{0:.1f}°C',
            'Hum:', '{0:.0f}%rH',
            'T2:', '{0:.1f}°C']
dim = (3,4)
_formats.extend(
  ["" for _ in range(dim[0]*dim[1] - len(_formats))])
_view = DataView(
  dim=dim,
  width=display.width-2-(dim[1]-1),height=int(0.6*display.height),
  fontname=f"fonts/{FONT_NAME}",
  formats=_formats,
  border=1,
  divider=1,
  color=Color.BLACK,
  bg_color=Color.WHITE
  )

for i in range(0,dim[0]*dim[1],2):
  _view.justify(Justify.LEFT,index=i)
  _view.justify(Justify.RIGHT,index=i+1)

_title = PanelText(text=f"Logger: 001",
                  fontname=f"fonts/{FONT_NAME}",
                  justify=Justify.CENTER)

_footer = PanelText(text=f"at 2023-06-28 11:22:06 SD",
                      fontname=f"fonts/{FONT_NAME}",
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
display.root_group = _panel
#display.show(_panel)
print("starting refresh()")
display.refresh()
print("finished")

while True:
  time.sleep(10)
