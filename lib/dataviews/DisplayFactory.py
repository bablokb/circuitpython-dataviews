# ----------------------------------------------------------------------------
# DisplayFactory: Utility class with static methods to create display-objects
#
# See directory examples for example/test-programs.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-dataviews
#
# ----------------------------------------------------------------------------

import board
import busio
import displayio
import sys
if sys.version_info[0] > 8:
  import fourwire
  from i2cdisplaybus import I2CDisplayBus
else:
  fourwire = displayio
  I2CDisplayBus = displayio.I2CDisplay

# --- helper-function for Inky-displays   -------------------------------------

def get_inky_info(i2c):
  """ try to return tuple (width,height,color) """
  from adafruit_bus_device.i2c_device import I2CDevice
  import struct
  COLOR = [None, 'black', 'red', 'yellow', None, 'acep7']

  EE_ADDR = 0x50
  i2c_device = I2CDevice(i2c,EE_ADDR)
  buffer = bytearray(29)
  with i2c_device as i2c:
    i2c.write(bytes([0x00])+bytes([0x00]))
    i2c.write_then_readinto(bytes([0x00]),buffer)

  data = struct.unpack('<HHBBB22s',buffer)
  return [data[0],data[1],COLOR[data[2]]]

class DisplayFactory:

  # --- return builtin-display   ---------------------------------------------

  @staticmethod
  def builtin():
    return board.DISPLAY

  # --- create SSD1306-based I2C-display   -----------------------------------

  @staticmethod
  def ssd1306(i2c=None,sda=None,scl=None,width=128,height=64,addr=0x3c):
    """ factory-method for SSD1306-based I2C-displays """

    from adafruit_displayio_ssd1306 import SSD1306

    if i2c is None:
      if sda is None:
        sda = board.SDA
      if scl is None:
        scl = board.SCL
      i2c = busio.I2C(sda=sda,scl=scl,frequency=400000)
    display_bus = I2CDisplayBus(i2c, device_address=addr)
    return SSD1306(display_bus,width=width,height=height)

  # --- create ST7789-based SPI-display   ------------------------------------

  @staticmethod
  def st7789(pin_dc,pin_cs,pin_rst=None,spi=None,**kwargs):
    """ factory-method for ST7789-based SPI-displays """

    from adafruit_st7789 import ST7789

    if spi is None:
      spi = board.SPI()

    bus = fourwire.FourWire(spi,command=pin_dc,chip_select=pin_cs,
                             reset=pin_rst)
    return ST7789(bus,**kwargs)

  # --- create ST7789-based display for the Pimoroni Pico-Display-Pack  ------

  @staticmethod
  def display_pack(spi=None):
    """ factory-method for a Display-Pack display """

    if spi is None:
      spi = busio.SPI(clock=board.GP18,MOSI=board.GP19)
    return DisplayFactory.st7789(
      spi=spi,pin_dc=board.GP16,pin_cs=board.GP17,
      height=135,width=240,rotation=270,rowstart=40,colstart=53)

  # --- create ST7735-based SPI-display   ------------------------------------

  @staticmethod
  def st7735(pin_dc,pin_cs,spi=None,pin_rst=None,
             height=128,width=160,rotation=90,bgr=True,**kwargs):
    """ factory-method for ST7735-based SPI-displays """

    from adafruit_st7735r import ST7735R       # SPI-TFT  display

    if spi is None:
      spi = board.SPI()

    bus = fourwire.FourWire(spi,command=pin_dc,chip_select=pin_cs,
                             reset=pin_rst)
    return ST7735R(bus,width=width,height=height,
                   rotation=rotation,bgr=bgr,**kwargs)

  # --- create pygame-based display   ----------------------------------------

  @staticmethod
  def pygame(height=400,width=600,**kwargs):
    """ factory-method for pygame-based displays """

    from blinka_displayio_pygamedisplay import PyGameDisplay
    return PyGameDisplay(width=width,height=height,**kwargs)

  # --- create display for Pimoronis Pico Inky-Pack   -------------------------

  @staticmethod
  def inky_pack(spi=None):
    """ create display for InkyPack """

    import InkyPack

    if spi is None:
      spi = busio.SPI(board.GP18,MOSI=board.GP19)

    display_bus = fourwire.FourWire(
      spi, command=board.GP20, chip_select=board.GP17,
      reset=board.GP21, baudrate=1000000
    )
    return InkyPack.InkyPack(display_bus,busy_pin=board.GP26)

  # --- create display for Pimoronis Inky-pHat   -----------------------------

  @staticmethod
  def inky_phat(spi=None,pin_dc=None,pin_cs=None,
                    pin_rst=None,pin_busy=None):
    """ create display for InkyPack """

    import phat

    if spi is None:
      spi = busio.SPI(board.SCLK,MOSI=board.MOSI)
    if pin_dc is None and hasattr(board,"GPIO22"):    # this is with
      pin_dc   = board.GPIO22                         # pico-*-base boards
      pin_cs   = board.CE0
      pin_rst  = board.GPIO27
      pin_busy = board.GPIO17

    display_bus = fourwire.FourWire(
      spi, command=pin_dc, chip_select=pin_cs,
      reset=pin_rst, baudrate=1000000
    )
    return phat.Inky_pHat(display_bus,busy_pin=pin_busy,rotation=90,
                          border_color='white')

  # --- create display for Adafruits Monochrom 2.13" e-ink   ------------------

  @staticmethod
  def ada_2_13_mono(pin_dc,pin_cs,spi=None,pin_rst=None,pin_busy=None,
                    rotation=270):
    """ create display for 2.13 monochrom display """

    import adafruit_ssd1675

    if spi is None:
      spi = board.SPI()

    display_bus = fourwire.FourWire(
      spi, command=pin_dc, chip_select=pin_cs,
      reset=pin_rst, baudrate=1000000
    )
    return adafruit_ssd1675.SSD1675(display_bus, width=250, height=122,
                                    busy_pin=pin_busy, rotation=rotation)

  # --- create display for Adafruits monochrome 1.54" e-ink   ----------------

  @staticmethod
  def ada_1_54_mono(pin_dc,pin_cs,spi=None,pin_rst=None,pin_busy=None,
                    rotation=0):
    """
    create display for 1.54 monochrome display.
    Note that Adafruit also sells a SSD1681-variant of the display.
    """

    import adafruit_ssd1608

    if spi is None:
      spi = board.SPI()

    display_bus = fourwire.FourWire(
      spi, command=pin_dc, chip_select=pin_cs,
      reset=pin_rst, baudrate=1000000
    )
    return adafruit_ssd1608.SSD1608(display_bus, width=200, height=200,
                                    busy_pin=pin_busy, rotation=rotation)

  # --- create display for Adafruits tri-color 1.5" e-ink   ------------------

  @staticmethod
  def ada_1_5_color(pin_dc,pin_cs,spi=None,pin_rst=None,pin_busy=None,
                    rotation=180):
    """ create display for 1.54 tri-color display """

    import adafruit_il0373

    if spi is None:
      spi = board.SPI()

    display_bus = fourwire.FourWire(
      spi, command=pin_dc, chip_select=pin_cs,
      reset=pin_rst, baudrate=1000000
    )

    return adafruit_il0373.IL0373(display_bus,width=152,height=152,
                                  busy_pin=pin_busy,
                                  highlight_color=0xFF0000,
                                  rotation=roation)

  # --- create display for Pimoroni Inky-displays   --------------------------

  @staticmethod
  def pimoroni_inky(i2c=None,sda=None,scl=None,
                    spi=None,pin_dc=None,pin_cs=None,
                    pin_rst=None,pin_busy=None):
    """ create display for e-inks from Pimoroni """

    if i2c is None:
      if sda is None:
        sda = board.SDA
      if scl is None:
        scl = board.SCL
      i2c = busio.I2C(sda=sda,scl=scl,frequency=400000)
    width,height,color = get_inky_info(i2c)

    if spi is None:
      spi = board.SPI()

    display_bus = fourwire.FourWire(
      spi, command=pin_dc, chip_select=pin_cs,
      reset=pin_rst, baudrate=1000000
    )

    if color == 'acep7': # assume Inky-Impression
      import adafruit_spd1656
      display = adafruit_spd1656.SPD1656(display_bus,busy_pin=pin_busy,
                                         width=width,height=height,
                                         refresh_time=2,
                                         seconds_per_frame=40)
    elif width == 400: # assume Inky-wHat
      import what
      display = what.Inky_wHat(display_bus,busy_pin=pin_busy,
                               color=color,border_color='white',
                               black_bits_inverted=False)

    elif width == 250: # assume Inky-pHat
      import phat
      display = phat.Inky_pHat(display_bus,busy_pin=pin_busy,rotation=90,
                               border_color='white')

    display.auto_refresh = False
    return display
