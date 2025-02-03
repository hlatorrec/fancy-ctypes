# -*- coding: utf-8 -*-
"""
fancytypes - Shared libraries in a fancy way
============================================

The `fancytypes <https://github.com/hlatorrec/fancytypes>`_ package is a 
`ctypes <https://docs.python.org/3/library/ctypes.html>`_ wrapper. It provides 
**syntax sugar that makes it easier to include C and Fortran code in your 
Python projects** through the use of shared libraries.

.. admonition:: What is a shared library
    :class: hint
    
    Shared libraries, also called binaries, are **executable code that can be 
    used by another program**. The `Wikipedia 
    <https://en.wikipedia.org/wiki/Shared_library>`_ article covers them in 
    more detail.

FancyTypes makes your interfaces to shared libraries simpler and clearer. 
**Calling functions becomes very straightforward and working with arrays is now 
very easy**.

This package assumes that **the user already knows some Python and has some 
basic programming experience in lower level languages** so that they can more 
easily dive into the world of language interoperability. This is likely the 
case for anyone who has already compiled and run some small program written in 
C or even Fortran (2003+ standard, not 77 or any similar abominations, though 
the later can be salvaged, sometimes).

.. note::

    Users who already have some experience with language interoperability may 
    skip directly to the documentation section, which describes the API.

Beginner tools
--------------

* :ref:`Why use shared libraries <whyshared>` - *Do you need them?*
* :ref:`Compiling a shared library <compiling>` - *It's not that hard*

API description
---------------

* :ref:`Basic types <basic>` - *Available types*
* :ref:`Structures and unions <structure>` - *User defined types*
* :ref:`Library interfaces <interface>` - *Building interfaces*
"""



from fancytypes.types import (FancyInteger, FancyLongInteger, FancyRealSingle,
                              FancyRealDouble, FancyCharacter, FancyLogical,
                              FancyUnsignedInteger, FancyUnsignedLongInteger,
                              FancyComplexSingle, FancyComplexDouble,
                              FancyShortInteger, FancyUnsignedShortInteger)
from fancytypes.types import pointer, strarray, ptrarray, nparray
from fancytypes.ctypes import cstruct, cunion, cpointer, cast
from fancytypes.sharedlib import load, interface



__version__ = '0.2.0'


__all__ = ['int32', 'int64', 'int16', 'real32', 'real64', 'uint32', 'uint64',
           'uint16', 'complex64', 'complex128', 'character', 'logical',
           'pointer', 'strarray', 'ptrarray', 'nparray', 'cstruct', 'cunion',
           'cpointer', 'load', 'interface', 'cast']



# Type & function aliases
int32 = integer = int = FancyInteger
int64 = long = FancyLongInteger
int16 = short = FancyShortInteger
real32 = float32 = single = sp = FancyRealSingle
real64 = float64 = double = dp = FancyRealDouble
uint32 = uint = FancyUnsignedInteger
uint64 = ulong = FancyUnsignedLongInteger
uint16 = ushort = FancyUnsignedShortInteger
complex64 = FancyComplexSingle
complex128 = FancyComplexDouble
character = char = FancyCharacter
logical = boolean = bool = FancyLogical
ptr = pointer
cptr = cpointer
