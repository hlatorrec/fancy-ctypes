# -*- coding: utf-8 -*-
"""
Basic types
===========

The basic or main **types provided by the package are mainly those used in 
numerical computation**, such as the types covered by the 
:code:`iso_fortran_env` intrinsic module introduced by the 2003 Fortran 
standard. Other **C types provided by the ctypes module still work with the 
rest of the API**, so they can be imported from there and used if necessary. 
See 
`here <https://docs.python.org/3/library/ctypes.html#fundamental-data-types>`_.

.. admonition:: Available types
    :class: hint
    
    :Integer:
        *Signed* :py:func:`16-bit<FancyShortInteger>` - 
        :py:func:`32-bit<FancyInteger>` - :py:func:`64-bit<FancyLongInteger>` /
        *Unsigned* :py:func:`16-bit<FancyUnsignedShortInteger>` - 
        :py:func:`32-bit<FancyUnsignedInteger>` - 
        :py:func:`64-bit<FancyUnsignedLongInteger>`
    
    :Real/Float:
        :py:func:`32-bit<FancyRealSingle>` - :py:func:`64-bit<FancyRealDouble>`
    
    :Complex:
        :py:func:`64-bit<FancyComplexSingle>` - 
        :py:func:`128-bit<FancyComplexDouble>` (as defined in 
        :code:`complex.h` by the C99 standard)
    
    :Logical/Boolean:
        :py:func:`8-bit<FancyLogical>`
    
    :Character:
        :py:func:`8-bit<FancyCharacter>`
    
    The aliases for these types are listed below, in the :ref:`type classes 
    <classes>` section. All aliases are imported into the namespace of the 
    module.
    
In addition to these, **pointer and array types can be created from basic 
types** using the :py:func:`pointer` function or multipliying them by the 
desired array length, respectively. C-style :ref:`array declaration <array>` 
can be mimicked by indexing type classes, which looks way prettier.

.. autofunction:: pointer

.. _array:

.. admonition:: Array types
    :class: note
    
    To create an array class, simply do:
        
        .. code-block:: python
        
            import fancytypes as ft
            
            my_array = 5 * ft.real64
            print(my_array) # Prints "fancytypes.real64_array_5"
            
            # C-style array declaration is also supported
            my_char_array = ft.character[8]
            print(my_char_array) # Prints "fancytypes.character_array_8"
        
        It is advised to **use NumPy arrays whenever posible instead ctypes 
        arrays**, but the package provides them nonetheless.

The package provides some functions to make interoperability easier:
    
    * :py:func:`strarray` - Create NumPy character arrays from Python strings
    * :py:func:`ptrarray` - Create an array of pointers to NumPy arrays on a 
      list
    * :py:func:`nparray` - Explicitly declare procedure arguments as NumPy 
      arrays


.. autofunction:: strarray
.. autofunction:: ptrarray
.. autofunction:: nparray

*Placeholder text for references to documentation that I will write eventually*

.. _classes:

Type classes
------------

.. autoclass:: FancyInteger()
.. autoclass:: FancyLongInteger()
.. autoclass:: FancyShortInteger()
.. autoclass:: FancyRealSingle()
.. autoclass:: FancyRealDouble()
.. autoclass:: FancyCharacter()
.. autoclass:: FancyLogical()
.. autoclass:: FancyUnsignedInteger()
.. autoclass:: FancyUnsignedLongInteger()
.. autoclass:: FancyUnsignedShortInteger()
.. autoclass:: FancyComplexSingle()
.. autoclass:: FancyComplexDouble()

"""



from ctypes import (c_int, c_longlong, c_short, c_float, c_double, c_char,
                    c_bool, c_uint, c_ulonglong, c_ushort, POINTER)


from numpy import (int32, int64, int16, float32, float64, uint32, uint64,
                   uint16, complex64, complex128, char)
from numpy.ctypeslib import ndpointer


from fancytypes._types import FancyMeta, FancyType, ComplexType
from fancytypes.ctypes import single_complex, double_complex



class FancyInteger(FancyType):
    '''Class for 32-bit integers.
    
    :Aliases:
        * *int32*
        * *integer*
        * *int*
    '''
    
    _ctype_ = c_int
    _numpy_ = int32
    _alias_ = 'int32'



class FancyLongInteger(FancyType):
    '''Class for 64-bit integers.
    
    :Aliases:
        * *int64*
        * *long*
    '''
    
    _ctype_ = c_longlong
    _numpy_ = int64
    _alias_ = 'int64'



class FancyShortInteger(FancyType):
    '''Class for 16-bit integers.
    
    :Aliases:
        * *int16*
        * *short*
    '''
    
    _ctype_ = c_short
    _numpy_ = int16
    _alias_ = 'int16'



class FancyRealSingle(FancyType):
    '''Class for 32-bit real numbers, aka floats or singles (like me).
    
    :Aliases:
        * *real32*
        * *float32*
        * *single*
        * *sp*
    '''
    
    _ctype_ = c_float
    _numpy_ = float32
    _alias_ = 'real32'



class FancyRealDouble(FancyType):
    '''Class for 64-bit real numbers, aka floats-64 or doubles.
    
    :Aliases:
        * *real64*
        * *float64*
        * *double*
        * *dp*
    '''
    
    _ctype_ = c_double
    _numpy_ = float64
    _alias_ = 'real64'



class FancyCharacter(FancyType):
    '''Class for 8-bit characters.
    
    :Aliases:
        * *character*
        * *char*
    '''
    
    _ctype_ = c_char
    _numpy_ = '|S'
    _alias_ = 'character'



class FancyLogical(FancyType):
    '''Class for 8-bit logical values, aka booleans or bools.
    
    :Aliases:
        * *logical*
        * *boolean*
        * *bool*
    '''
    
    _ctype_ = c_bool
    _numpy_ = bool
    _alias_ = 'logical'



class FancyUnsignedInteger(FancyType):
    '''Class for 32-bit unsigned integers.
    
    :Aliases:
        * *uint32*
        * *uint*
    '''
    
    _ctype_ = c_uint
    _numpy_ = uint32
    _alias_ = 'uint32'



class FancyUnsignedLongInteger(FancyType):
    '''Class for 64-bit unsigned integers.
    
    :Aliases:
        * *uint64*
        * *ulong*
    '''
    
    _ctype_ = c_ulonglong
    _numpy_ = uint64
    _alias_ = 'uint64'



class FancyUnsignedShortInteger(FancyType):
    '''Class for 16-bit unsigned integers.
    
    :Aliases:
        * *uint16*
        * *ushort*
    '''
    
    _ctype_ = c_ushort
    _numpy_ = uint16
    _alias_ = 'uint16'



class FancyComplexSingle(ComplexType):
    '''Class for 64-bit complex numbers (two single precision real numbers).
    
    :Aliases:
        * *complex64*
    '''
    
    _ctype_ = single_complex
    _numpy_ = complex64
    _alias_ = 'complex64'



class FancyComplexDouble(ComplexType):
    '''Class for 128-bit complex numbers (two double precision real numbers).
    
    :Aliases:
        * *complex128*
    '''
    
    _ctype_ = double_complex
    _numpy_ = complex128
    _alias_ = 'complex128'



def pointer(typ):
    '''Return a pointer class. These **pointer classes are used to declare 
    pointer arguments in procedure interfaces**. For pointers to actual 
    :py:mod:`ctypes` variable instances use :py:func:`cpointer` instead.
    
    :param typ: Type to get a pointer class from
    :return: Pointer class
    
    .. code-block:: python
        
        import fancytypes as ft
        
        my_pointer = ft.pointer(ft.real64)
        print(my_pointer) # Prints "fancytypes.ptr_real64"
        
        # These can be chained
        my_pointer_to_a_pointer = ft.pointer(my_pointer)
        print(my_pointer_to_a_pointer) # Prints "fancytypes.ptr_ptr_real64"
    '''
    
    # Current workaround solution to let struct/union pointers through
    if hasattr(typ, '_fields_'):
        return POINTER(typ)
    
    if not hasattr(typ, '_ctype_'):
        errmsg = 'fancytypes.pointer must receive a fancytypes type'
        raise TypeError(errmsg)
    
    return typ._pointer()


def strarray(items, *, strlen=None):
    '''Return a NumPy character array from a Python string or a list of 
    strings. For the later, the longest string sets the length of the array 
    "rows" that store the individual strings, padding the shorter strings.
    
    .. admonition:: Character encoding
        :class: note
        
        Unicode outputs are explicitly disabled to ensure 8-bit elements. This 
        function was originally meant for paths, so it will not fit all  
        usecases. ASCII outside of the minimal 8-bit is not supported.
    
    :param items: String or list/tuple of strings
    :type items: :py:class:`str`, :py:class:`list` or :py:class:`tuple`
    :param strlen: Specify a string length, default is the longest required
    :type strlen: :py:class:`int`, *optional*
    :return: NumPy character array of 8-bit characters
    :rtype: :py:class:`numpy.ndarray`
    
    .. code-block:: python
        
        import fancytypes as ft
        
        my_strings = ['data.dat', 'some_text.txt', 'user.cfg']
        my_array = ft.strarray(my_strings)
        print(my_array) # Prints "[b'data.dat', b'some_text.txt', b'user.cfg']"
    '''
    
    if isinstance(items, str):
        items = (items,)
    
    if not isinstance(items, (list, tuple)):
        errmsg = 'items must be a list or tuple of strings'
        raise TypeError(errmsg)
    
    asarray = char.asarray(items, itemsize=strlen, unicode=False)
    
    return asarray



def ptrarray(arrays, typ):
    '''Return an array of pointers to NumPy arrays on a list. This can be used 
    to pass an arbitrary number of arrays to a procedure. These arrays do not 
    have to be contiguous in memory, which forces us to pass them like this.
    
    :param arrays: List/tuple of arrays
    :type arrays: :py:class:`list` or :py:class:`tuple`
    :param typ: Type to make the pointers to
    :return: :py:mod:`ctypes` array instance
    
    .. code-block:: python
        
        import numpy as np
        import fancytypes as ft
        
        my_array_1 = np.array([1, 2, 3, 4, 5], dtype=np.int32)
        my_array_2 = np.array([6, 7, 8, 9, 10], dtype=np.int32)
        my_array_3 = np.array([11, 12, 13, 14, 15], dtype=np.int32)
        my_arrays = [my_array_1, my_array_2, my_array_3]
        
        my_pointer_array = ft.ptrarray(my_arrays, ft.int32)
        print(my_pointer_array[0][:5]) # Prints [1, 2, 3, 4, 5]
        print(my_pointer_array[1][:5]) # Prints [6, 7, 8, 9, 10]
        print(my_pointer_array[2][:5]) # Prints [11, 12, 13, 14, 15]
    '''
    
    if not isinstance(arrays, (list, tuple)):
        errmsg = 'arrays must be a list or tuple of NumPy arrays'
        raise TypeError(errmsg)
    
    if not type(typ) is FancyMeta:
        this_class = typ.__name__
        errmsg = f'dtype must be a fancytypes type, got {this_class} instead'
        raise TypeError(errmsg)
    
    array_type = pointer(typ) * len(arrays)
    ptr_array = array_type(*(typ.array(array) for array in arrays))
    
    return ptr_array


def nparray(typ, *, ndim=None, shape=None, flags=None):
    '''Return a :py:class:`~numpy.ctypeslib.ndpointer` object from 
    :py:mod:`numpy.ctypeslib`. These can be used in procedure interfaces to 
    explicitly declare NumPy arrays as arguments. This function is a wrapper 
    around `ndpointer 
    <https://numpy.org/doc/stable/reference/routines.ctypeslib.html#numpy.ctypeslib.ndpointer>`_,
    and its optional keyword arguments are described there.
    
    :param typ: Type of the array
    :return: NumPy ndpointer object
    :rtype: :py:class:`~numpy.ctypeslib.ndpointer`
    
    .. code-block:: python
        
        import fancytypes as ft
        
        my_ndpointer = ft.nparray(ft.real64)
        print(my_ndpointer) # Prints "numpy.ctypeslib.ndpointer_<f8"
    '''
    
    if not type(typ) is FancyMeta:
        this_class = typ.__name__
        errmsg = f'dtype must be a fancytypes type, got {this_class} instead'
        raise TypeError(errmsg)
    
    ctype = typ._ctype_
    
    if hasattr(ctype, '_type_') and not isinstance(ctype._type_, str):
        errmsg = 'NumPy array arguments can only be of basic types'
        raise TypeError(errmsg)
    
    return ndpointer(typ._numpy_, ndim=ndim, shape=shape, flags=flags)
