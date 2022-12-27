# ----------------------------------------------------------------------------
# DataView: base class for data-views.
#
# A DataView displays data in a (row,col)-grid. Technically, it is a
# displayio.Group, so the view can be added to the view-hierarchy.
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
from adafruit_display_shapes.line import Line
from adafruit_bitmap_font import bitmap_font

# --- base class for all data-views   ----------------------------------------

class DataView(displayio.Group):

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
               border=0,                    # border-size in pixels
               divider=0,                   # divider-size in pixels
               padding=1,                   # padding next to border/divider
               fontname=None,               # font (defaults to terminalio.FONT
               justify=RIGHT,               # justification of labels
               formats=None,                # format of labels
               x=0,                         # for displayio.Group
               y=0                          # for displayio.Group
               ):
    """ constructor """

    super().__init__(x=x,y=y)

    self._dim      = dim
    self._width    = width
    self._height   = height
    self._bg_color = None
    self._color    = color
    self._border   = border
    self._divider  = divider
    self._padding  = padding
    self._font     = (terminalio.FONT if fontname is None else
                      bitmap_font.load_font(fontname))
    self._justify  = justify
    self._formats  = (formats if formats is not None
                      else ['{0}' for i in range(dim[0]*dim[1])])
    self._values   = None

    # some constant values that depend on dim and width/height
    self._rows     = self._dim[0]
    self._cols     = self._dim[1]
    self._w_cell   = self._width/self._cols
    self._h_cell   = self._height/self._rows
    self._y_anchor = 0.5

    # create UI-elements
    self.set_background(bg_color)
    self._create_lines()
    self._create_labels()

  # --- create border and dividers   -----------------------------------------

  def _create_lines(self):
    """ create border and dividers """

    self._lines = displayio.Group()
    self.append(self._lines)
    if self._border and self._divider:
      # all lines
      rows = range(0,self._rows+1)
      cols = range(0,self._cols+1)
    elif self._border and not self._divider:
      # only outer lines
      rows = [0,self._rows+1]
      cols = [0,self._cols+1]
    elif self._divider:
      # only inner lines
      rows = range(1,self._rows)
      cols = range(1,self._cols)
    else:
      # no lines at all
      return

    # draw horizontal lines
    x0 = 0
    x1 = self._width-1
    ydelta = float(self._height/self._rows)
    for row in rows:
      y = min(int(row*ydelta),self._height-1)
      line = Line(x0,y,x1,y,color=self._color)
      self._lines.append(line)

    # draw vertical lines
    y0 = 0
    y1 = self._height-1
    xdelta = float(self._width/self._cols)
    for col in cols:
      x = min(int(col*xdelta),self._width-1)
      line = Line(x,y0,x,y1,color=self._color)
      self._lines.append(line)

  # --- create label at given location   -------------------------------------

  def _create_label(self,row,col,justify):
    """ create text at given location """

    x_off = justify*self._w_cell/2
    if justify == DataView.LEFT and col == 0:
      x_off += self._border + self._padding
    elif justify == DataView.LEFT:
      x_off += self._divider + self._padding
    if justify == DataView.RIGHT and col == self._cols-1:
      x_off -= self._border + self._padding
    elif justify == DataView.RIGHT:
      x_off -= self._divider + self._padding

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

  # --- create labels   ------------------------------------------------------

  def _create_labels(self):
    """ create fields """

    self._labels = displayio.Group()
    for row in range(self._rows):
      for col in range(self._cols):
        lbl = self._create_label(row,col,self._justify)
        self._labels.append(lbl)

    # append labels as sub-group to ourselves
    self.append(self._labels)

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
    if len(self):
      # background is always the first layer, exchange it
      self[0] = rect
    else:
      self.append(rect)

  # --- set foreground-color   -----------------------------------------------

  def set_color(self,color,index=None):
    """ set color """

    if index is None:
      # set color for all labels and lines
      self._color = color
      for lbl in self._labels:
        lbl.color = color
      for line in self._lines:
        line.color = color
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

    if index is None:
      # justify all labels
      self._justify = justify
      for row in range(self._rows):
        for col in range(self._cols):
          lbl = self._create_label(row,col,self._justify)
          self._labels[col+row*self._cols] = lbl
    else:
      row,col = divmod(index,self._cols)
      self._labels[index] = self._create_label(row,col,justify)

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
