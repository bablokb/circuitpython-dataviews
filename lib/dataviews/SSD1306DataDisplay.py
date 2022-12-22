# ----------------------------------------------------------------------------
# SSD1306DataDisplay: Display with SSD1306-driver and DataView
#
# See examples/simple_test_1306.py for a usage-template
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
import adafruit_displayio_ssd1306

from dataviews.DataView import DataView

class SSD1306DataDisplay:

  # --- constructor   --------------------------------------------------------

  def __init__(self,sda=None,scl=None,
               width=128,height=64,addr=0x3c,
               dim=(3,1),**kwargs):
    """ constructor """

    if sda is None:
      sda = board.SDA
    if scl is None:
      scl = board.SCL
    displayio.release_displays()
    i2c = busio.I2C(sda=sda,scl=scl,frequency=400000)
    display_bus = displayio.I2CDisplay(i2c, device_address=addr)
    self._display = adafruit_displayio_ssd1306.SSD1306(display_bus,
                                                       width=width,
                                                       height=height)
    self._view = DataView(dim,width,height,**kwargs)

  # --- return view   --------------------------------------------------------

  def get_view(self):
    """ return view """
    return self._view

  # --- return display   -----------------------------------------------------

  def get_display(self):
    """ return display """
    return self._display

  # --- show   ---------------------------------------------------------------

  def show(self):
    """ show view inside the display """
    self._display.show(self._view.get_group())
