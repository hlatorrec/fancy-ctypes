.. _whyshared:

Why use shared libraries
========================

Although the Python ecosystem is already very matured, **sometimes the already 
available tools are not enough or not convenient to use**, which forces us to 
write our own beyond simple scripts. When writing our own tools, usually by 
combining already existing tools, **Python by itself might not be the best or 
easier solution**.

.. admonition:: Problems we may have
    :class: hint
    
    * Our Python code is **not fast enough**
    * **Memory consumption** is way too high
    * We **already have non-Python code**

These problems may lead us to **search for solutions outside of Python** to 
achieve the performance boost that we need, or we may **already have a 
non-Python solution** available to us. None of those mean that we have to 
switch languages entirely, since **Python has tools to communicate with those 
solutions**. This package is one of those tools, which mostly wraps an 
`existing module <https://docs.python.org/3/library/ctypes.html>`_ from the 
standard library and provides some extra shortcut functions for convenience.

Although using more than one language simultaneously adds an **extra layer of 
complexity**, sometimes there is no better alternative or no alternative at 
all. The **performance gain can be very significant** when working with large 
amounts of data, both in terms of speed and memory consumption. The later 
cannot be readily dismissed, as many Python tools will fix the first while 
still making large copies of data by default.