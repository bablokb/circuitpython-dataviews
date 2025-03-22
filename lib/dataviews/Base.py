# ----------------------------------------------------------------------------
# Base: base class for DataView and DataPanel.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import gc
import displayio
from vectorio import Rectangle

class Color:
  """some basic colors (see: https://en.wikipedia.org/wiki/Web_colors) """

  WHITE   = 0xFFFFFF
  BLACK   = 0x000000

  RED     = 0xFF0000
  LIME    = 0x00FF00
  BLUE    = 0x0000FF

  YELLOW  = 0xFFFF00
  FUCHSIA = 0xFF00FF
  AQUA    = 0x00FFFF

  MAROON  = 0x800000
  GREEN   = 0x008000
  NAVY    = 0x000080

  GRAY    = 0x808080
  OLIVE   = 0x808000
  TEAL    = 0x008080
  PURPLE  = 0x800080

  SILVER  = 0xC0C0C0

class Justify:
  """ justification constants """
  LEFT   = 0
  CENTER = 1
  RIGHT  = 2

class BaseGroup(displayio.Group):

  # --- constructor   --------------------------------------------------------

  def __init__(self,
               width,                       # width view
               height,                      # height of view
               bg_color=Color.BLACK,        # background color
               color=Color.WHITE,           # (foreground) color
               border=0,                    # border-size in pixels
               padding=1,                   # padding next to border/divider
               x=0,                         # for displayio.Group
               y=0                          # for displayio.Group
               ):
    """ constructor """

    super().__init__(x=x,y=y)

    self.width     = width
    self.height    = height
    self.bg_color  = bg_color
    self.color     = color
    self.border    = border
    self.padding   = padding

    self._background = displayio.Group()
    self.append(self._background)
    self.set_background()

  # --- set background   -----------------------------------------------------

  def set_background(self,bg_color=-1,color=-1,border=-1):
    """ monochrome background and border.
    Arguments override object-attributes. """

    if not self.width and not self.height:
      return

    if self.bg_color is None:
      return
    shader = displayio.Palette(2)
    if bg_color != -1:
      shader[0] = bg_color
    else:
      shader[0] = self.bg_color

    if color != -1:
      shader[1] = color
    else:
      shader[1] = self.color

    if border == -1:
      border = self.border

    for _ in range(len(self._background)):
      self._background.pop()
    gc.collect()

    if border > 0:
      # needs two rectangles
      b1 = Rectangle(pixel_shader=shader,x=0,y=0,
                     width=self.width,
                     height=self.height,
                     color_index=1)
      self._background.append(b1)
    b2 = Rectangle(pixel_shader=shader,x=border,y=border,
                   width=self.width-2*border,
                   height=self.height-2*border,
                   color_index=0)
    self._background.append(b2)
