# ----------------------------------------------------------------------------
# LabelItem: A ListItem wrapping a Label as content
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import gc
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

from dataviews.Base import Justify, Color
from dataviews.ListItem import ListItem

# --- class LabelItem   ------------------------------------------------------

class LabelItem(ListItem):
  """ A LabelItem is a styled Label with behavior """

  # --- constructor   --------------------------------------------------------

  def __init__(self,
               width=None,
               height=None,
               text="",
               color=Color.WHITE,
               bg_color=Color.BLACK,
               border=0,
               padding=2,
               justify=Justify.CENTER,      # justification of labels
               fontname=None,
               x=0,
               y=0):

    super().__init__(width=width,
                     height=height,
                     color=color,
                     bg_color=bg_color,
                     border=border,
                     padding=padding,
                     x=x,y=y)

    self._text     = text
    if fontname is None:
      self.font = terminalio.FONT
    elif isinstance(fontname,str):
      self.font = bitmap_font.load_font(fontname)
    else:
      # assume font
      self.font = fontname

  # --- create label at given location   -------------------------------------

  def get_content(self):
    """ create Label object """

    return label.Label(self.font,text=self._text,
                    color=self.color,
                    anchor_point=(0,0),
                    anchored_position=(0,0))

  # --- create new item with identical settings   -------------------------------

  def create(self,text=""):
    """ create new item with identical settings """

    return LabelItem(
      text=text,
      color=self.color,
      bg_color=self.bg_color,
      border=self.border,
      padding=self.padding,
      justify=self._justify,
      fontname=self.font
      )
