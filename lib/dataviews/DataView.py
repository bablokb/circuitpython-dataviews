# ----------------------------------------------------------------------------
# DataView: base class for data-views.
#
# A DataView displays data in a (row,col)-grid.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import displayio
import vectorio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# --- base class for all data-views   ----------------------------------------

class DataView:

  # some basic colors
  WHITE = 0xFFFFFF
  BLACK = 0x000000
  RED   = 0xFF0000
  GREEN = 0x00FF00
  BLUE  = 0x0000FF

  # justification
  LEFT   = 0
  CENTER = 1
  RIGHT  = 2

  # --- constructor   --------------------------------------------------------

  def __init__(self,dim,width,height):
    """ constructor: pass dimensions of data-grid and width/height"""

    self._dim      = dim
    self._width    = width
    self._height   = height
    self._bg_color = DataView.BLACK
    self._fg_color = DataView.WHITE
    self._font     = terminalio.FONT
    self._justify  = DataView.RIGHT
    self._group    = None
    self._units    = ['{0}' for i in range(dim[0]*dim[1])]
    self._values   = [i  for i in range(dim[0]*dim[1])]
    self._labels   = []

  # --- create background   --------------------------------------------------

  def _set_background(self):
    """ monochrome background """

    palette    = displayio.Palette(1)
    palette[0] = self._bg_color
    background = vectorio.Rectangle(pixel_shader=palette,
                                    width=self._width+1,
                                    height=self._height, x=0, y=0)
    self._group.append(background)

  # --- create label at given location   -------------------------------------

  def _create_label(self,text,pos,anchor):
    """ create text at given location """

    t = label.Label(self._font,text=text,
                    color=self._fg_color,anchor_point=anchor)
    t.anchored_position = pos
    self._group.append(t)
    return t

  # --- get text for value by index   ----------------------------------------

  def _text(self,index):
    """ get formatted text by index """

    return self._units[index].format(self._values[index])

  # --- create fields   ------------------------------------------------------

  def _create_fields(self):
    """ create fields """

    rows     = self._dim[0]
    cols     = self._dim[1]
    w_cell   = self._width/cols
    h_cell   = self._height/rows
    x_off    = self._justify*w_cell/2
    x_anchor = 0.5*self._justify
    y_anchor = 0.5

    for row in range(rows):
      y = (2*row+1)*h_cell/2                 # fixed, vertical center of label
      for col in range(cols):
        x = x_off + col*w_cell
        lbl = self._create_label(self._text(col+row*cols),
                                 (x,y),(x_anchor,y_anchor))
        self._labels.append(lbl)
        
  # --- create view   --------------------------------------------------------

  def create(self):
    """ create view """

    if not self._group:
      self._group = displayio.Group()
      self._set_background()
      self._create_fields()

  # --- set foreground-color   -----------------------------------------------

  def set_fg_color(self,color):
    """ set foreground color """
    self._fg_color = color

  # --- set background-color   -----------------------------------------------

  def set_bg_color(self,color):
    """ set background color """
    self._bg_color = color

  # --- set font   -----------------------------------------------------------

  def set_font(self,fontname):
    """ set font """
    self._font = bitmap_font.load_font(fontname)

  # --- set justification of values    ---------------------------------------

  def justify(self,just):
    """ set justification within cell """
    self._justify = just

  # --- set units   ----------------------------------------------------------

  def set_units(self,units):
    """ set units. One format string for every data-item """
    self._units = units

  # --- set values    --------------------------------------------------------

  def set_values(self,values):
    self._values = values
    for i in range(values):
      self._labels[i].text = self._text(i)

  # --- get group   ----------------------------------------------------------

  def get_group(self):
    """ return group (create if necessary) """

    self.create()
    return self._group
