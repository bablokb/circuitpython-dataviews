Dataviews - Simple Views for Data-Display
=========================================

This project provides the CircuitPython module `dataviews` with a number
of classes that simplify the presentation of data.

Goal is not to provide fancy output, but simple to use wrapper-classes
for standard displayio-classes. You typically use the classes of this
module with small I2C or SPI displays to display sensor-readings or
similar data.

The data is arranged in a grid with rows x cols fields. Every field
has an associated format. Normally you create the view with suitable
attributes (colors, border, justification, formats and so on)
and then use the method `set_values()` to update the data within a loop.


Installation
------------

Just copy the `lib`-directory to your device. The repository also provides
a number font-subsets, see <fonts/Readme.md> for details. In case you want
to use these fonts you should also copy the `fonts`-directory.


Usage
-----

There are a number of programs in the `examples`-directory that can serve
as a blueprint. See <reference.md> for a quick cheat-sheet of classes and
methods. The ultimate reference is of course the source-code.
