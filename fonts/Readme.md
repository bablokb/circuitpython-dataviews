Fonts
=====

This directory contain a number of font-files in BDF-format:

  - DejaVuSansMono-Bold-18-subset.bdf
  - DejaVuSansMono-Bold-24-subset.bdf
  - DejaVuSansMono-Bold-32-subset.bdf
  - DejaVuSansMono-Bold-52-subset.bdf
  - DejaVuSans-16-subset.bdf

All these files only contain a subset of available glyphs, mainly
numbers, characters a-z, A-Z, some basic punctuation-chars and some special
chars.

You can query the available characters by running

    grep STARTCHAR fonts/DejaVuSansMono-Bold-18-subset.bdf

If you need additional glyphs or fonts, you should follow the tutorial from
<https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display>.
