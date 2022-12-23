# ----------------------------------------------------------------------------
# ST7789DataDisplay: Display with ST7789-driver and DataView
#
# See examples/st7789_aht20.py for a usage-template
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import board
import busio
import displayio
from adafruit_st7789 import ST7789

from dataviews.DataView import DataView

class ST7789DataDisplay(ST7789):

  # --- constructor   --------------------------------------------------------

  def __init__(self,pin_dc,pin_cs,spi=None,pin_rst=None,
               height=135,width=240,rotation=270,rowstart=40,colstart=53,
               dim=(3,2),**kwargs):
    """ constructor """

    if spi is None:
      spi = board.SPI()

    bus = displayio.FourWire(spi,command=pin_dc,chip_select=pin_cs,
                             reset=pin_rst)
    super().__init__(bus,width=width,height=height,rotation=rotation,
                     rowstart=rowstart,colstart=colstart)
    self._view = DataView(dim,width,height,**kwargs)

  # --- return view   --------------------------------------------------------

  def get_view(self):
    """ return view """
    return self._view

  # --- show   ---------------------------------------------------------------

  def show_view(self):
    """ show view inside the display """
    self.show(self._view)
