# ----------------------------------------------------------------------------
# DataLabel: This class wraps label.Label from adafruit_display_text.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
# ----------------------------------------------------------------------------

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

from .DataCell import DataCell

# --- Class implementing Labels as cell-content   ----------------------------

class DataLabel(DataCell):

  # --- constructor   --------------------------------------------------------

  def __init__(self,font=None, color=None, bg_color=None, format=None):
    """ constructor """
    super().__init__(font,color,bg_color,format)
    # note: bg_color ignored for performance reasons
    self.content = label.Label(self.font, color=self.color)

  # --- width and height properties   ----------------------------------------

  @property
  def width(self):
    """ width of label """
    return self.content.width

  @property
  def height(self):
    """ height of label """
    return self.content.height

  # --- set position   -------------------------------------------------------

  def set_position(self,anchor_point,anchor_position):
    """ set position of content """
    self.content.anchor_point = anchor_point
    self.content.anchored_position = anchor_position

  # --- set color   ----------------------------------------------------------

  def set_color(self,color):
    """ set color """
    super().set_color(color)
    self.content.color = self.value2color(self.value)

  # --- set value   -----------------------------------------------------------

  def set_value(self,value):
    """ set value of content """

    super().set_value(value)
    if value is None:
      self.content.text = "" if not self.format else self.format
    elif self.format:
      self.content.text = self.format.format(value)
    else:
      self.content.text = str(value)
    self.content.color = self.value2color(value)

  # --- invert color   -------------------------------------------------------

  def invert(self):
    """ swap color and bg_color """
    super().invert()
    self.content.color = self.value2color(self.value)
