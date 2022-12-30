Reference
=========


Class DataView
--------------

This is a subclass of `displayio.Group` and can be used like any other
group, but you will typically use it as the root-group, i.e.

    view = DataView(...)
    display.show(view)

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

  - Constants:
    * `LEFT, CENTER, RIGHT`: justification of fields
    * `WHITE, BLACK, RED, GREEN, BLUE`: some basic colors


  - Fixed attributes
    * `dim = (rows,cols)`: dimension
    * `width`: width of the view in pixels
    * `height`: height of the view in pixels
    * `border`: border-size in pixels
    * `divider`: divider-size in pixels (lines betweeen fields)
    * `padding`: added space between content and border and dividers
    * `x=0`    : x-origin within parent group
    * `y=0`    : y-origin within parent group

  - Variable attributes (see methods below):
    * `bg_color = BLACK`: background color
    * `color = WHITE`: color of lines and values
    * `fontname = None`: name of the font to load. If unset, uses 
       `terminalio.Font`, a very small font
    * `justify=RIGHT`: justification of all fields
    * `formats=None`: formats of fields. Must be a list with rows x cols elements.

  - Methods:
    * `set_background(self,bg_color)`: set background color.
    * `set_color(self,color,index=None)`: set global foreground color or color
      of the field with the given index. The index is mapped to fields
      in row-column order.
    * `invert(self)`: flip forground and background colors.
    * `set_font(self,fontname,index=None)`: set global font or font of the
      field with the given index.
    * `justify(self,justify,index=None)`: set global justification or
      justification of the field with the given index.
    * `set_formats(self,formats)`: set list of formats. Must be a list with
      rows x cols elements.
    * `set_values(self,values)`: set values of fields. Must be a list with
       rows x cols elements.


Class DisplayFactory
--------------------

This is a small utility class with static methods to create display-objects for
some common small displays like I2C-OLED with SSD1306, ST7735, ST7789.
