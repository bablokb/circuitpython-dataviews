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

import gc
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

  def __init__(self,
               dim,                         # dimension of data (rows,cols)
               width,                       # width view
               height,                      # height of view
               bg_color=BLACK,              # background color
               color=WHITE,                 # (foreground) color
               fontname=None,               # font (defaults to terminalio.FONT
               justify=RIGHT,               # justification of labels
               formats=None                 # format of labels
               ):
    """ constructor """

    self._dim      = dim
    self._width    = width
    self._height   = height
    self._bg_color = None
    self._color    = color
    self._font     = (terminalio.FONT if fontname is None else
                      bitmap_font.load_font(fontname))
    self._justify  = justify
    self._formats  = (formats if formats is not None
                      else ['{0}' for i in range(dim[0]*dim[1])])
    self._values   = None
    self._labels   = []

    # some constant values that depend on dim and width/height
    self._rows     = self._dim[0]
    self._cols     = self._dim[1]
    self._w_cell   = self._width/self._cols
    self._h_cell   = self._height/self._rows
    self._y_anchor = 0.5

    # create UI-elements
    self._group = displayio.Group()
    self.set_background(bg_color)
    self._create_fields()

  # --- create label at given location   -------------------------------------

  def _create_label(self,row,col,justify):
    """ create text at given location """

    x_off    = justify*self._w_cell/2
    x_anchor = 0.5*justify
    x        = x_off + col*self._w_cell
    y        = (2*row+1)*self._h_cell/2

    t = label.Label(self._font,text=self._text(col+row*self._cols),
                    color=self._color,
                    anchor_point=(x_anchor,self._y_anchor),
                    anchored_position=(x,y))
    return t

  # --- get text for value by index   ----------------------------------------

  def _text(self,index):
    """ get formatted text by index """

    if self._values is None or self._values[index] is None:
      return self._formats[index]
    else:
      return self._formats[index].format(self._values[index])

  # --- create fields   ------------------------------------------------------

  def _create_fields(self):
    """ create fields """

    for row in range(self._rows):
      for col in range(self._cols):
        lbl = self._create_label(row,col,self._justify)
        self._labels.append(lbl)
        self._group.append(lbl)
        
  # --- set background   -----------------------------------------------------

  def set_background(self,bg_color):
    """ monochrome background """

    if bg_color == self._bg_color:
      return

    self._bg_color = bg_color
    palette        = displayio.Palette(1)
    palette[0]     = self._bg_color
    rect           = vectorio.Rectangle(pixel_shader=palette,
                                        width=self._width+1,
                                        height=self._height, x=0, y=0)
    if len(self._group):
      # background is always the first layer, exchange it
      self._group[0] = rect
    else:
      self._group.append(rect)

  # --- set foreground-color   -----------------------------------------------

  def set_color(self,color,index=None):
    """ set color """

    if index is None:
      # set color for all labels
      self._color = color
      for lbl in self._labels:
        lbl.color = color
    else:
      # set color for given label
      self._labels[index].color = color

  # --- invert view   --------------------------------------------------------

  def invert(self):
    """ invert colors """
    color_new = self._bg_color
    self.set_background(self._color)
    self.set_color(color_new)

  # --- set font   -----------------------------------------------------------

  def set_font(self,fontname,index=None):
    """ set font """

    if index is None:
      # set font for all labels
      self._font = bitmap_font.load_font(fontname)
      for lbl in self._labels:
        lbl.font = self._font
    else:
      # set font for given label
      font = bitmap_font.load_font(fontname)
      self._labels[index].font = font

  # --- set justification of values    ---------------------------------------

  def justify(self,justify,index=None):
    """ set justification within cell """

    # the code assumes that group[0] is the background and
    # group[1...rows*cols] are the labels
    if index is None:
      # justify all labels
      self._justify = justify
      for row in range(self._rows):
        for col in range(self._cols):
          lbl = self._create_label(row,col,self._justify)
          self._labels[col+row*self._cols] = lbl
          self._group[1+col+row*self._cols] = lbl
    else:
      row,col = divmod(index,self._cols)
      self._labels[index]  = self._create_label(row,col,justify)
      self._group[1+index] = self._labels[index]

    # remove unused labels
    gc.collect()

  # --- set formats   --------------------------------------------------------

  def set_formats(self,formats):
    """ set formats. One format string for every data-item """
    self._formats = formats

  # --- set values    --------------------------------------------------------

  def set_values(self,values):
    """ set values """
    self._values = values
    for i in range(len(values)):
      self._labels[i].text = self._text(i)

  # --- get group   ----------------------------------------------------------

  def get_group(self):
    """ return group """

    return self._group
