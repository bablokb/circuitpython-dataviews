# ----------------------------------------------------------------------------
# pyportal-datapanel.py
#
# A sample application for the DataPanel class. This program expects to
# run on a Py-Portal.
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

from adafruit_adt7410 import ADT7410

from dataviews.Base import Color, Justify
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView  import DataView
from dataviews.DataPanel import DataPanel, PanelText

# create display
display = board.DISPLAY

# create sensor-object for internal temperature sensor
i2c = board.I2C()
adt = ADT7410(i2c, address=0x48)
adt.high_resolution = True

# create view with one row for temperature (label: value)
view = DataView(
  dim=(1,2),
  width=int(0.8*display.width),height=int(display.height/3),
  justify=Justify.RIGHT,
  fontname="fonts/DejaVuSansMono-Bold-32-subset.bdf",
  formats=["Temp:",
           "{0:.1f}°C"],
  border=1,
  divider=0,
  bg_color=Color.BLUE
)
view.justify(Justify.RIGHT,index=0)
view.justify(Justify.LEFT,index=1)
view.set_color(color=Color.SILVER,index=1)
view.set_values([None,adt.temperature])

# create DataPanel
title = PanelText(text="PyPortal",color=Color.FUCHSIA,
                  fontname="fonts/DejaVuSansMono-Bold-52-subset.bdf",
                  justify=Justify.CENTER)

panel = DataPanel(
  width=display.width,
  height=display.height,
  view=view,
  title=title,
  footer=PanelText(text="https://github.com/bablokb/circuitpython-dataviews",
                   color=Color.SILVER),
  border=1,
  padding=5,
  justify=Justify.CENTER,
  )

display.show(panel)
time.sleep(3)

# update some title attributes
display.auto_refresh = False
title.text    = "ADT7410"
title.color   = Color.YELLOW
display.refresh()
display.auto_refresh = True

while True:
  view.set_values([None,adt.temperature])
  time.sleep(5)
