# ----------------------------------------------------------------------------
# pyportal-datapanel-pygame.py
#
# A sample application for the DataPanel class. This program simulates a
# Py-Portal.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import board
import time

from dataviews.Base import Color, Justify
from dataviews.DisplayFactory import DisplayFactory
from dataviews.DataView  import DataView
from dataviews.DataPanel import DataPanel, PanelText

# create display
display = DisplayFactory.pygame(width=320,height=240,native_frames_per_second=1)
display.auto_refresh=False

# simulate sensor-object for internal temperature sensor
class ADT7410:
  temperature = 22.8
adt = ADT7410()

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
display.refresh()
time.sleep(3)

# update some title attributes
title.text    = "ADT7410"
title.color   = Color.YELLOW
#display.auto_refresh=True
display.refresh()

def on_time():
  view.set_values([None,adt.temperature])
  display.refresh()

display.event_loop(interval=5,on_time=on_time)
