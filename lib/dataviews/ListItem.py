# ----------------------------------------------------------------------------
# ListItem: an item of a ListView
#
# Subclasses must implement
#   - get_content()
#   - width, height
#   - anchor_position, anchor_point
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

from dataviews.Base import BaseGroup, Justify, Color

# --- class ListItem   ------------------------------------------------------

class ListItem(BaseGroup):
  """ A ListItem is the base-class of styled items with behavior """

  # --- constructor   --------------------------------------------------------

  def __init__(self,
               width=None,
               height=None,
               color=Color.WHITE,
               bg_color=Color.BLACK,
               border=0,
               padding=2,
               justify=Justify.CENTER,      # justification of labels
               x=0,
               y=0):

    super().__init__(width=width,
                     height=height,
                     color=color,
                     bg_color=bg_color,
                     border=border,
                     padding=padding,
                     x=x,y=y)

    self.bg_color  = bg_color
    self._justify  = justify
    self._focus    = False
    self._selected = False
    self._redraw   = True

    self._content  = displayio.Group()
    self.append(self._content)

  # --- create content at given location   -----------------------------------

  def _create_content(self):
    """ create content object """

    content = self.get_content()
    if len(self._content):                # content already filled
      self._content[0] = content          # replace with new content
      gc.collect()                        # garbage collect
    else:
      self._content.append(content)       # first-time, so just append

  # --- perform layout   -----------------------------------------------------

  def layout(self,width=None,height=None):
    """ layout object, draw border and fill """

    if not self._redraw:
      return
    
    self._create_content()

    # item dimensions
    if width is None:
      """ use width of item """
      width = self._content[0].width + 2*self.padding + 2*self.border
      if self._focus:
        width += 2*self.border
    if height is None:
      """ use height of item """
      height = self._content[0].height + 2*self.padding + 2*self.border
      if self._focus:
        height += 2*self.border

    # align label within item
    x_off = 0.5*self._justify*width
    if self._justify == Justify.LEFT:
      x_off += self.border + self.padding
    elif self._justify == Justify.RIGHT:
      x_off -= self.border + self.padding

    self._content[0].anchor_point=(0.5*self._justify,0.5)
    self._content[0].anchored_position=(x_off,height/2)

    # update size
    self.width  = width
    self.height = height

    # fill background and create border
    if self._focus:
      self.set_background(border=2*self.border)
    else:
      self.set_background()

    self._redraw = False

  # --- get/set focus   -------------------------------------------------------

  @property
  def focus(self):
    return self._focus

  @focus.setter
  def focus(self,focus):
    if focus != self._focus:
      self._focus  = focus
      self._redraw = True

  # --- get/set selection   -------------------------------------------------------

  @property
  def selected(self):
    """ get/set selection status """
    return self._selected

  @selected.setter
  def selected(self,select):
    """ select/deselect item """
    if self._selected and not select:
      self._redraw   = True
      self._selected = False
      self.bg_color,self.color = (self.color,self.bg_color)
    elif not self._selected and select:
      self._redraw   = True
      self._selected = True
      self.bg_color,self.color = (self.color,self.bg_color)

  def toggle_selection(self):
    """ flip selection status """
    self.selected(not self._selected)
