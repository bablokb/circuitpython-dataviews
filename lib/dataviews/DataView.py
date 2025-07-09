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
from dataviews.DataLabel import DataLabel

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
               objects=None,                # list (row,col,DataCell)
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
    self._divider  = divider
    font           = (terminalio.FONT if fontname is None else
                      bitmap_font.load_font(fontname))

    if isinstance(justify,int):
      self._justify = [justify]*(dim[0]*dim[1])
    else:
      self._justify  = justify

    if formats is None:
      formats = '{0}'
    if isinstance(formats,str):
      formats = [formats]*(dim[0]*dim[1])
    else:
      formats  = formats

    self._lines    = None
    self._cells   = None

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
      self._cell_wt = [1/self._cols]*self._cols

    self._cell_h   = self.height/self._rows
    self._y_anchor = 0.5

    # create UI-elements
    self._create_cells(objects,font,formats)
    self._create_lines()

  # --- calculate cell-width   -----------------------------------------------

  def _calc_cell_w(self):
    """ calculate cell width for dynamic column-width """

    # calculate necessary width per column, iterating over all rows
    cell_w = [0]*self._cols
    for row in range(self._rows):
      for col in range(self._cols):
        cell = self._cells[col+row*self._cols]
        cell_w[col] = max(cell_w[col],cell.width+2*self.padding)

    # adjust column widths (distribute rest according to weights)
    rest_w = self.width - sum(cell_w)
    if rest_w > 0:
      cell_w = [int(w+wt*rest_w) for (w,wt) in zip(cell_w,self._cell_wt)]
    self._cell_w = cell_w

  # --- calculate x-coordinates of column-start   ----------------------------

  def _calc_cell_x(self):
    """ calculate column x-start """

    # a column starts on the next pixel right from the border/divider
    self._cell_x = [self.border]
    for w in self._cell_w[:-1]:
      # last column-pos-1 + column-width + 1 (divider) + 1 (next colum)
      self._cell_x.append(min(self._cell_x[-1]-1+w+1+1,self.width-1))

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

  def _set_position(self,cell,row,col):
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
    cell.set_position((x_anchor,self._y_anchor),(x,y))

  # --- set positions   ------------------------------------------------------

  def _set_positions(self):
    """ set positions of all cells """

    for row in range(self._rows):
      for col in range(self._cols):
        cell = self._cells[col+row*self._cols]
        self._set_position(cell,row,col)

  # --- create cells   -------------------------------------------------------

  def _create_cells(self,objects,font,formats):
    """ create cells """

    group = displayio.Group()
    self.append(group)

    self._cells = [None]*self._rows*self._cols
    if objects:
      for row,col,obj in objects:
        self._cells[col+row*self._cols] = obj

    # append cell-content to group
    for row in range(self._rows):
      for col in range(self._cols):
        if not self._cells[col+row*self._cols]:
          # create default cell objects (DataLabel)
          self._cells[col+row*self._cols] = DataLabel(
            font=font,
            color=self.color,
            bg_color=self.bg_color,
            format=formats[col+row*self._cols])
        group.append(self._cells[col+row*self._cols].content)

    if self._auto_width:
      self._calc_cell_w()
    self._calc_cell_x()
    self._set_positions()

  # --- set foreground-color   -----------------------------------------------

  def set_color(self,color=None,index=None):
    """ set color. """

    if color is None:
      return

    if index is None:
      # set color for all labels and lines
      for cell in self._cells:
        cell.set_color(color)
    else:
      # set color for given label
      self._cells[index].set_color(color)

  # --- color property of DataView   -----------------------------------------

  @BaseGroup.color.setter
  def color(self,value):
    self._color = value
    for line in self._lines:
      line.color = value

  # --- invert view   --------------------------------------------------------

  def invert(self):
    """ invert colors """
    fg_new = self.bg_color
    bg_new = self.color
    self.set_background(bg_new)
    self.color = fg_new
    self.bg_color = bg_new
    for cell in self._cells:
      cell.invert()

  # --- set font   -----------------------------------------------------------

  def set_font(self,fontname,index=None):
    """ set font """

    font = bitmap_font.load_font(fontname)
    if index is None:
      # set font for all cells
      for cell in self._cells:
        cell.font = font
    else:
      # set font for given cell
      self._cells[index].font = font

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
      self._set_position(self._cells[index],row,col)

  # --- set formats   --------------------------------------------------------

  def set_format(self,format,index=None):
    """ set formats. format without an index must be a list """
    if index is None:
      for i in range(len(format)):
        self._cells[i].set_format(format[i])
    else:
        self._cells[index].set_format(format)

  # --- set values    --------------------------------------------------------

  def set_values(self,values,index=None):
    """ set values (passing None will force recalculation) """
    if index is None:
      for i in range(len(values)):
        self._cells[i].set_value(values[i])
    else:
      self._cells[index].set_value(values)

    if self._auto_width:
      self._calc_cell_w()
      self._calc_cell_x()
      self._set_positions()
      self._create_lines()
