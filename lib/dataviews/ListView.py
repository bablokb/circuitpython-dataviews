# ----------------------------------------------------------------------------
# ListView: A collection of ListItems
#
# Currently this is a vertically list of items. Eventually it will support
# selections and scrolling.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import displayio
from dataviews.Base import BaseGroup, Color, Justify
from dataviews.ListItem import ListItem

# --- Collection of list-items   ---------------------------------------------

class ListView(BaseGroup):

  # --- constructor   --------------------------------------------------------

  def __init__(self,
               width,                       # width view
               height,                      # height of view
               bg_color=Color.BLACK,        # background color
               color=Color.WHITE,           # (foreground) color
               border=0,                    # border-size in pixels
               padding=2,                   # padding between items
               justify=Justify.CENTER,      # justification of items
               item_width=None,             # width of items (None: automatic)
               item_height=None,            # height of items (None: automatic)
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

    self._justify     = justify
    self._item_width  = item_width
    self._item_height = item_height
    self._items       = displayio.Group()
    self._redraw      = True
    self.append(self._items)

  # --- add items   --------------------------------------------------------

  def add_items(self,items):
    """ add items to the view """

    for item in items:
      self._items.append(item)
    self._redraw = True

  # --- set focus for given item   -------------------------------------------

  def set_focus(self,nr,focus=True):
    """ set/clear focus for given item """

    for i,item in enumerate(self._items):
      if i == nr:
        item.focus = focus
      elif focus:
        # clear focus on other items
        item.focus = False
    self._redraw = True

  # --- set selection for given item   -----------------------------------------

  def set_selection(self,nr,select=True):
    """ set selection for given item """

    self._items[nr].selected = select
    self._redraw = True

  # --- perform layout   -----------------------------------------------------

  def layout(self):
    """ perform layout """

    if not self._redraw:
      return

    width  = -1
    y = 0
    for item in self._items:
      item.layout(self._item_width,self._item_height)
      if not self.width:
        x = 0
      elif self._justify == Justify.LEFT:
        x = 0
      elif self._justify == Justify.CENTER:
        x = int((self.width - item.width)/2)
      else:
        x = self.width - item.width
      item.x = x
      item.y = y
      y     += item.height + self.padding
      width = max(width,item.width)
      if self.height and y > self.height-item.height:
        # no space for an additional item
        break

    # update width/height
    if not self.width:
      self.width = width
    if not self.height:
      self.height = y - self.padding

    # update background and border
    self.set_background()
    self._redraw = False
