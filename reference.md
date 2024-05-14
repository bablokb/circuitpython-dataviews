Reference
=========

Class Justify
-------------

Constants for justification of fields:
  * `Justify.LEFT`
  * `Justify.CENTER`
  * `Justify.RIGHT`

Import:

    from dataviews.Base import Justify


Class Color
-----------

Color constants for sixteen HTML 4.01 basic web colors
(see: <https://en.wikipedia.org/wiki/Web_colors>).

Import:

    from dataviews.Base import Color


Class DataView
--------------

This is a subclass of `displayio.Group` and can be used like any other
group, but you will typically use it as the root-group, i.e.

    view = DataView(...)
    display.root_group = view

A DataView is a grid of rows x cols fields. The number of rows and
colums that fit on a display varies with display-size. Although it is
possible to put 3x3 fields on a 128x64 I2C-oled-display, it does not
really make sense.

Besides rows and columns a view also has a width and a height. You
typically set this to `display.width` and `display.height` unless you
have a larger display and don't want to use the complete display-size
for the DataView.

Some attributes can only be set using the constructor, other attributes
can be changed dynamically.

  - Fixed attributes
    * `dim = (rows,cols)`: dimension
    * `width`: width of the view in pixels
    * `col_width=None`: column width (see below)
    * `height`: height of the view in pixels
    * `border`: border-size in pixels
    * `divider`: add divider between row and columns (True|False)
    * `padding`: added space between content and border and dividers
    * `value2color=None`: callback to dynamically set the color of
      a cell. Signature is `func(index,value)`. If `None`, use the colors
      as defined by `set_color()` or `color`. 
    * `x=0`    : x-origin within parent group
    * `y=0`    : y-origin within parent group

  - Variable attributes (see methods below):
    * `bg_color = Color.BLACK`: background color
    * `color = Color.WHITE`: color of lines and values
    * `fontname = None`: name of the font to load. If unset, uses 
       `terminalio.Font`, a very small font
    * `justify=Justify.RIGHT`: justification of all fields. Can also be
      a list with rows x cols elements
    * `formats=None`: formats of fields. Must be a list with rows x cols elements.

  - Methods:
    * `set_background(self,bg_color)`: set background color.
    * `set_color(self,color=None,index=None,color_range=None)`:  
       set global foreground color or color of the field with the given index.
       The index is mapped to fields in row-column order.  
       You can also supply a color-range as a list `[(color,value),...]`,e.g.
       `[(Color.BLUE,0),(Color.GREEN,20),(Color.RED,None)]`. With
       this example values below zero will be in blue, below 20 in green and all
       values above will be in red color.
    * `invert(self)`: flip forground and background colors.
    * `set_font(self,fontname,index=None)`: set global font or font of the
      field with the given index.
    * `justify(self,justify,index=None)`: set global justification or
      justification of the field with the given index.
    * `set_format(self,format,index=None)`: set list of formats.
       Must be a list with rows x cols elements if index is not set.
    * `set_values(self,values,index=None)`: set values of fields.
       Must be a list with rows x cols elements if index is not set.

The attribute `col_width` allows control over the column-width. Possible
values:

  - `None`: the default, this will generate equally sized columns
  - `[width1,width2,...]`: use columns of the given sizes in pixels
  - `'AUTO'`: optimize column-width so that the content will fit
  - `[weight1,weight2,...]`: same as `'AUTO'`, but distribute remaining space
    according to the given weights. Weights must be between 0 and 1.

The first two options might clip their content. If the sum of the width
given in the second option is smaller than the width of the DataView, you
will have an empty additional column on the right.

Automatically sized columns are clipped on the right if the total
of the column widths is larger than the given view width (as defined by
the `width`-attribute). Passing weights will not change this. Weights are
only used to distribute unused space.


Class DataPanel
---------------

A `DataPanel` is a `displayio.Group` with three elements: a title, a footer
and a `DataView`. It is useful for larger displays, e.g. the Py-Portal. The
title is always on the top edge of the display, the `DataView` is
vertically centered and the footer is at the bottom edge.

  - Fixed attributes
    * `width`: width of the panel in pixels
    * `height`: height of the panel in pixels
    * `border`: border-size in pixels
    * `padding`: added space between content and border
    * `x=0`    : x-origin within parent group
    * `y=0`    : y-origin within parent group
    * `bg_color = Color.BLACK`: background color
    * `color = Color.WHITE`: color of border and default title/footer color

Title and footer are passed as instances of `PanelText`:

    title = PanelText(text="PyPortal",color=Color.FUCHSIA,
                      fontname="fonts/DejaVuSansMono-Bold-52-subset.bdf",
                      justify=Justify.CENTER)

For an usage example, see `examples/pyportal-datapanel.py`.


Class PanelText
---------------

Container for title and footer texts within a `DataPanel`.
All properties execpt the fontname can be changed after creation.

  - Fixed attributes
    * `fontname=None` (defaults to `terminalio.Font`)

  - Properties (with getter/setter):
    * `text`: text
    * `color`: color of text (defaults to color of `DataPanel`)
    * `justify`: justification of text (defaults to justification of `DataPanel`)


Class DisplayFactory
--------------------

This is a small utility class with static methods to create display-objects for
some common small displays like I2C-OLED with SSD1306, ST7735, ST7789.
