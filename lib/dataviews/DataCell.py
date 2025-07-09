# ----------------------------------------------------------------------------
# DataCell: base class for cells within a DataView.
#
# A DataCell wraps objects that can be added to a displayio.Group. It
# has methods for positioning and setting values.
#
# The default class for DataViews is the DataLabel, which is a subclass
# of DataCell that wraps label.Label from adafruit_display_text.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
# ----------------------------------------------------------------------------

# --- base class for all data-cells   ----------------------------------------

class DataCell:

  # --- constructor   --------------------------------------------------------

  def __init__(self, font=None, color=None, bg_color=None, format=None):
    """ constructor """
    self.font = font
    self.color = color
    self.bg_color = bg_color
    self.format = format
    self.content = None
    self.value = None

  # --- set position   -------------------------------------------------------

  def set_position(self,anchor_point,anchor_position):
    """ set position of content """
    raise NotImplementedError("set_position must be implemented by a subclass")

  # --- set format   ---------------------------------------------------------

  def set_format(self,format):
    """ set format and clear value """
    self.format = format
    self.set_value(None)

  # --- set color   ----------------------------------------------------------

  def set_color(self,color):
    """ set color """
    self.color = color

  # --- set value   ----------------------------------------------------------

  def set_value(self,value):
    """ set value of content """
    self.value = value

  # --- set color from color_range and value   -------------------------------

  def value2color(self,value):
    """ get color for given value """

    if not isinstance(self.color,(list,tuple)):
      # no range, so just return the color
      return self.color

    # search for given color
    for color,val in self.color:
      if val is None or value is None:
        return color
      elif value <= val:
        return color

  # --- invert color   -------------------------------------------------------

  def invert(self):
    """ swap color and bg_color.
    Does not work with value-color mappings.
    """
    if isinstance(self.color,(list,tuple)):
      raise ValueError("list/tuple for self.color not supported")
    fg_new = self.bg_color
    bg_new = self.color
    self.color    = fg_new
    self.bg_color = bg_new
