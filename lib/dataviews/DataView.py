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
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_bitmap_font import bitmap_font

from dataviews.Base import BaseGroup, Color, Justify

# --- base class for all data-views   ----------------------------------------

class DataView(BaseGroup):

  # --- constructor   --------------------------------------------------------

  def __init__(self,
               dim,                         # dimension of data (rows,cols)
               width,                       # width view
               height,                      # height of view
               col_width=None,              # column width
               bg_color=Color.BLACK,         # background color
               color=Color.WHITE,            # (foreground) color
               border=0,                    # border-size in pixels
               divider=False,               # print divider
               padding=1,                   # padding next to border/divider
               fontname=None,               # font (defaults to terminalio.FONT
               justify=Justify.RIGHT,          # justification of labels
               formats=None,                # format of labels
               x=0,                         # for displayio.Group
               y=0                          # for displayio.Group
               ):
    """ constructor """

    super().__init__(width=width,
                     height=height,
                     bg_color=bg_color,
                     color=color,
                     border=border,
                     padding=padding,
                     x=x,y=y)

    self._dim      = dim
    self._divider  = int(divider)
    self._font     = (terminalio.FONT if fontname is None else
                      bitmap_font.load_font(fontname))

    if isinstance(justify,int):
      self._justify = [justify]*(dim[0]*dim[1])
    else:
      self._justify  = justify

    self._formats  = (formats if formats is not None
                      else ['{0}']*(dim[0]*dim[1]))
    self._values   = None
    self._color_r  = {}
    self._lines    = None
    self._labels   = None

    # some constant values that depend on dim and width/height
    self._rows     = self._dim[0]
    self._cols     = self._dim[1]

    # calculate width and weight for given col_width parameter
    self._cell_wt = None
    if col_width is None:
      # default is same width
      self._cell_w = [int(self.width/self._cols)]*self._cols
      self._auto_width = False
    elif not isinstance(col_width,str):
      # assume list of width or weight
      if col_width[0] < 1:
        # list of weights, i.e. automatic size
        self._auto_width = True
        self._cell_wt = col_width
      else:
        # list of width, fixed size
        self._auto_width = False
        self._cell_w = col_width
    else:
      # assume string 'AUTO' or whatever, fixed weights
      self._auto_width = True
      self._cell_wt = [1/self._cols]*self_cols

    self._cell_h   = self.height/self._rows
    self._y_anchor = 0.5

    # create UI-elements
    self.set_background(bg_color)
    self._create_labels()
    self._create_lines()

  # --- calculate cell-width   -----------------------------------------------

  def _calc_cell_w(self):
    """ calculate cell width for dynamic column-width """

    cell_w = [0]*self._cols
    for row in range(self._rows):
      for col in range(self._cols):
        lbl = self._label[col+row*self._cols]
        cell_w[col] = max(cell_w[col],lbl.width)

    # adjust column widths
    rest_w = self.width - sum(cell_w)
    if rest_w > 0:
      cell_w = [int(w+wt*rest_w) for (w,wt) in zip(cell_w,self._cell_wt)]
    self._cell_w = cell_w

  # --- calculate x-coordinates of column-start   ----------------------------

  def _calc_x_start(self):
    """ calculate column x-start """

    # a column starts on the next pixel right from the border/divider
    self._cell_x = [self.border]
    for w in self._cell_w[:-1]:
      # last column-pos-1 + column-width + divider + 1 (next colum)
      self._cell_x.append(min(self._cell_x[-1]-1+w+self._divider+1,self.width-1))

  # --- create border and dividers   -----------------------------------------

  def _create_lines(self):
    """ create border and dividers """

    if self._lines:
      # remove old lines
      for _ in range(len(self._lines)):
        self._lines.pop(0)
      gc.collect()
    else:
      self._lines = displayio.Group()
      self.append(self._lines)

    if self.border and self._divider:
      # all lines
      rows = range(0,self._rows+1)
      x_cols = [cell_x-1 for cell_x in self._cell_x]
      x_cols.append(min(x_cols[-1]+self._cell_w[-1]+1,self.width-1))
    elif self.border and not self._divider:
      # only outer lines
      rows = [0,self._rows+1]
      x_cols = [0,self.width-1]
    elif self._divider:
      # only inner lines
      rows = range(1,self._rows)
      x_cols = [cell_x-1 for cell_x in self._cell_x[1:]]
    else:
      # no lines at all
      return

    # draw horizontal lines
    x0 = 0
    x1 = self.width-1
    ydelta = float(self.height/self._rows)
    for row in rows:
      y = min(int(row*ydelta),self.height-1)
      line = Line(x0,y,x1,y,color=self.color)
      self._lines.append(line)

    # draw vertical lines
    y0 = 0
    y1 = self.height-1
    for x_col in x_cols:
      line = Line(x_col,y0,x_col,y1,color=self.color)
      self._lines.append(line)

  # --- set position of label   ----------------------------------------------

  def _set_position(self,lbl,row,col):
    """ set label-position for given cell """

    justify = self._justify[col+row*self._cols]

    if justify == Justify.LEFT:
      # start of cell plus padding
      x = self._cell_x[col] + self.padding
    elif justify == Justify.RIGHT:
      # start of cell + cell-width minus padding
      x = min(self._cell_x[col] + self._cell_w[col],self.width-1) - self.padding
    else:
      # start of cell + 0.5*cell-width
      x = self._cell_x[col] + self._cell_w[col]/2

    x_anchor = 0.5*justify
    y        = (2*row+1)*self._cell_h/2

    lbl.anchor_point=(x_anchor,self._y_anchor)
    lbl.anchored_position=(x,y)

  # --- get text for value by index   ----------------------------------------

  def _get_text(self,index):
    """ get formatted text by index """

    if self._values is None or self._values[index] is None:
      return self._formats[index]
    else:
      return self._formats[index].format(self._values[index])

  # --- set color from color_range and value   -------------------------------

  def _value2color(self,index):
    """ get color for given value """

    if not index in self._color_r:
      # no range, so just return the current color
      return self._labels[index].color

    # search for given color
    for color,val in self._color_r[index]:
      if val is None:
        return color
      elif self._values[index] <= val:
        return color

  # --- create labels   ------------------------------------------------------

  def _create_labels(self):
    """ create fields """

    self._labels = displayio.Group()
    self.append(self._labels)

    # create labels
    for row in range(self._rows):
      for col in range(self._cols):
        lbl = label.Label(self._font,text=self._get_text(col+row*self._cols),
                          color=self.color)
        self._labels.append(lbl)

    if self._auto_width:
      self._calc_cell_w()
    self._calc_x_start()
    self._set_positions()

  # --- set positions   ------------------------------------------------------

  def _set_positions(self):
    """ set positions of all labels """

    for row in range(self._rows):
      for col in range(self._cols):
        lbl = self._labels[col+row*self._cols]
        self._set_position(lbl,row,col)

  # --- set foreground-color   -----------------------------------------------

  def set_color(self,color=None,index=None,color_range=None):
    """ set color.
    If color_range = [(color1,value1),...] is supplied, the color argument
    is ignored and the color depends on the value. Note that the
    tuples within range have to be ordered by value. The last value can
    be None.
    """

    if index is None:
      if color is None:
        return
      # set color for all labels and lines
      self.color = color
      for lbl in self._labels:
        lbl.color = color
      for line in self._lines:
        line.color = color
    elif color_range is None:
      if color is None:
        return
      # set color for given label
      self._labels[index].color = color
    else:
      self._color_r[index] = color_range
      self._labels[index].color = self._value2color(index)

  # --- invert view   --------------------------------------------------------

  def invert(self):
    """ invert colors """
    fg_new = self.bg_color
    bg_new = self.color
    self.set_background(bg_new)
    self.set_color(fg_new)
    self.bg_color = bg_new

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

    if self._auto_width:
      self._calc_cell_w()
      self._calc_cell_x()
      self._set_positions()
      self._create_lines()

  # --- set justification of values    ---------------------------------------

  def justify(self,justify,index=None):
    """ set justification within cell """

    if index is None:
      # justify all labels
      if isinstance(justify,int):
        self._justify = [justify]*(self._dim[0]*self._dim[1])
      else:
        self._justify  = justify
      self._set_positions()
    else:
      # justify a specific label
      self._justify[index] = justify
      row,col = divmod(index,self._cols)
      self._set_position(self._labels[index],row,col)

  # --- set formats   --------------------------------------------------------

  def set_format(self,format,index=None):
    """ set formats. One format string for every data-item """
    if index is None:
      self._formats = format
      self.set_values(None)
    else:
      seif._formats[index] = format
      self._labels[index].text  = self._get_text(index)
      self.set_values(None,index=index)

  # --- set values    --------------------------------------------------------

  def set_values(self,values,index=None):
    """ set values (passing None will force recalculation) """
    if index is None:
      if values:
        self._values = values
      for i in range(len(self._values)):
        self._labels[i].text  = self._get_text(i)
        self._labels[i].color = self._value2color(i)
    else:
      self._values[index] = values
      self._labels[index].text  = self._get_text(index)
      self._labels[index].color = self._value2color(index)


    if self._auto_width:
      self._calc_cell_w()
      self._calc_cell_x()
      self._set_positions()
      self._create_lines()
