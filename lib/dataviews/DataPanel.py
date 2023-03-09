# ----------------------------------------------------------------------------
# DataPanel: A utility class for larger displays with a title, a DataView
#            and a footer.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font

from dataviews.Base import BaseGroup, Justify, Color

# --- class PanelText   ------------------------------------------------------

class PanelText:
  """ Attributes for title and footer """

  # --- constructor   --------------------------------------------------------

  def __init__(self,
               text="",
               color=None,
               fontname=None,
               justify=Justify.CENTER):
    self._text    = text
    self._color   = color
    self.font     = (terminalio.FONT if fontname is None else
                    bitmap_font.load_font(fontname))
    self._justify = justify


  # --- get/set text (and update label)   ------------------------------------

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self,text):
    self._text = text
    if hasattr(self,"_label"):
      self._label.text = text

  # --- get/set color (and update label)   -----------------------------------

  @property
  def color(self):
    return self._color

  @color.setter
  def color(self,color):
    self._color = color
    if hasattr(self,"_label"):
      self._label.color = color

  # --- get/set justify (does not update label)   -------------------------------

  @property
  def justify(self):
    return self._justify

  @justify.setter
  def justify(self,justify):
    self._justify = justify

# --- class DataPanel   ------------------------------------------------------

class DataPanel(BaseGroup):
  """ A group with title, DataView and footer """

  # --- constructor   --------------------------------------------------------

  def __init__(self,
               width,                       # width of panel
               height,                      # height of panel
               view,                        # the data-view
               title=None,                  # title (instance of PanelText)
               footer=None,                 # footer (instance of PanelText)
               justify=Justify.CENTER,      # justification of data-view
               bg_color=Color.BLACK,        # background color
               color=Color.WHITE,           # (foreground) color
               border=0,                    # border-size in pixels
               padding=1,                   # padding next to border/divider
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

    self._view    = view
    self._justify = justify

    self._title   = PanelText(color=color,justify=justify) if not title else title
    if not self._title.color:
      self._title.color = color
    if not self._title.justify:
      self._title.justify = justify

    self._footer  = PanelText(color=color,justify=justify) if not footer else footer
    if not self._footer.color:
      self._footer.color = color
    if not self._footer.justify:
      self._footer.justify = justify

    # create UI-elements
    self.set_background(bg_color)
    self._create_labels()
    self._add_view()

  # --- create labels for title and footer   ---------------------------------

  def _create_label(self,panel_text,is_title):
    """ create label """

    if panel_text.justify == Justify.LEFT:
      x = self.border + self.padding
    elif panel_text.justify == Justify.RIGHT:
      x = self.width - self.border - self.padding
    else:
      x = self.width/2
    if is_title:
      y = self.border + self.padding
      y_anchor = 0
    else:
      y = self.height - self.border - self.padding
      y_anchor = 1

    x_anchor = 0.5*panel_text.justify
    panel_text._label = label.Label(panel_text.font,
                                    text=panel_text.text,
                                    color=panel_text.color,
                                    anchor_point=(x_anchor,y_anchor),
                                    anchored_position=(x,y))
    self.append(panel_text._label)

  # --- create labels for title and footer   ---------------------------------

  def _create_labels(self):
    """ create labels for title and footer """

    self._title_label = self._create_label(self._title,True)
    self._footer_label = self._create_label(self._footer,False)

  # --- add view (vertically centered)   -------------------------------------

  def _add_view(self):
    """ add view """

    if self._justify == Justify.LEFT:
      self._view.x = self.border + self.padding
    elif self._justify == Justify.RIGHT:
      self._view.x = self.width - self._view.width - self.border - self.padding - 1
    else:
      self._view.x = int((self.width - self._view.width)/2)
    self._view.y = int((self.height - self._view.height)/2)
    self.append(self._view)
