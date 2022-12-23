Fonts
=====

This directory contain a number of font-files in BDF-format:

  - DejaVuSansMono-Bold-18-subset.bdf
  - DejaVuSansMono-Bold-32-subset.bdf
  - DejaVuSansMono-Bold-52-subset.bdf

All these files only contain a subset of available glyphs, mainly
numbers, characters a-z, A-Z, some basic punction-chars and some special
characters.

You can query the available characters by running

    grep STARTCHAR fonts/DejaVuSansMono-Bold-18-subset.bdf

If you need additional characters, you should follow the tutorial from
<https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display>.
