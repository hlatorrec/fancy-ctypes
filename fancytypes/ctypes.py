# -*- coding: utf-8 -*-
"""
Structures and unions
=====================

User defined types are created by **decorating a class that stores the 
corresponding member annotations**. Each of the types, :code:`struct` and 
:code:`union`, has its own decorator function, :py:func:`@cstruct<cstruct>` and 
:py:func:`@cunion<cunion>`, respectively.

.. autodecorator:: cstruct
.. autodecorator:: cunion

Structure and union types have a corresponding :code:`numpy.dtype` and **can be
used as a datatype in NumPy arrays**. Pointer types are first converted to 
:code:`ctypes.c_void_p`, which NumPy interprets as unsigned integers. This 
conversion does not affect the actual structure or union type.
"""



from ctypes import (c_float, c_double, pointer as pointer_, cast as cast_,
                    Structure, Union, c_void_p)
import functools


from numpy import dtype


from fancytypes._types import FancyType



def _build_structured_type(cls, base, alias, wrapped):
    '''Wrap custom structured types. Make them NumPy friendly as well by 
    declaring all pointer types as void pointers, which NumPy interprets as 
    integers of machine address size.
    '''
    
    fields = [(var, typ._ctype_)
                          if hasattr(typ, '_ctype_') else (var, typ)
                                  for var, typ in cls.__annotations__.items()]
    
    ctypes_type = type('struct', (base, *cls.__bases__), {'_fields_' : fields})
    functools.update_wrapper(ctypes_type, cls, updated=())
    
    if not wrapped:
        return ctypes_type
    
    type_name = f'{cls.__name__}_{base.__name__}'
    
    numpy_fields = [(var, c_void_p)
                            if hasattr(typ, 'contents') else (var, typ)
                                        for var, typ in ctypes_type._fields_]
    
    dict_ = {
        '_ctype_' : ctypes_type,
        '_numpy_' : dtype(numpy_fields, align=True),
        '_alias_' : alias if alias else f'{base.__name__}({repr(fields)})',
        }
    
    new_type = type(type_name, (FancyType,), dict_)
    
    return new_type
    


def cstruct(cls=None, /, *, alias=None, wrapped=True):
    '''Class decorator that returns a C struct class that inherits from 
    :py:class:`ctypes.Structure`. The decorated class must **annotate the 
    struct members with valid types**.
    
    .. code-block::
        
        <name> : <type>
    
    The :code:`type` field takes all types from the :ref:`basic types <basic>` 
    section, plus all pointer and array types derived from them. User defined 
    types are also valid, together with `ctypes types 
    <https://docs.python.org/3/library/ctypes.html#fundamental-data-types>`_.
    
    .. code-block:: python
        
        import fancytypes as ft
        
        # 128-bit complex number as defined by the C99 standard
        @ft.cstruct
        class complex128:
            real : ft.real64 # Real part
            imag : ft.real64 # Imaginary part
        
        # Sample struct that can store an N-dimensional array
        @ft.cstruct
        class ndarray:
            data : ft.pointer(ft.real64) # Pointer to the first data array element
            dim : ft.pointer(ft.int32) # Pointer to the first dimension array element
            ndim : ft.int32 # Number of dimensions
    
    :param alias: User defined alias for the type, default is an explicit list 
        with the fields
    :type alias: str, optional
    :param wrapped: Flag to wrap the type or return a :code:`ctypes` class, 
        default is :code:`True`
    :type wrapped: bool, optional
    '''
    
    def build(cls):
        return _build_structured_type(cls, Structure, alias, wrapped)
    
    if cls is None:
        return build
    
    return build(cls)


def cunion(cls=None, /, *, alias=None, wrapped=True):
    '''Class decorator that returns a C union class that inherits from 
    :py:class:`ctypes.Union`. Union members are annotated following the same  
    rules described in :py:func:`@cstruct<cstruct>`.
    
    :param alias: User defined alias for the type, default is an explicit list 
        with the fields
    :type alias: str, optional
    :param wrapped: Flag to wrap the type or return a :code:`ctypes` class, 
        default is :code:`True`
    :type wrapped: bool, optional
    '''
    
    def build(cls):
        return _build_structured_type(cls, Union, alias, wrapped)
    
    if cls is None:
        return build
    
    return build(cls)



@cstruct(wrapped=False)
class single_complex:
    '''Single precision complex number.
    '''
    
    real : c_float
    imag : c_float



@cstruct(wrapped=False)
class double_complex:
    '''Double precision complex number.
    '''
    
    real : c_double
    imag : c_double



def cpointer(var):
    '''Get a pointer to a :py:mod:`ctypes` instance.
    
    :param var: Instance of ctypes type
    :type var: :py:mod:`ctypes` instance
    :return: Pointer to a ctypes instance.
    :rtype: :py:mod:`ctypes` instance of pointer type
    '''
    
    return pointer_(var)


def cast(var, typ):
    '''Cast pointer instance into another pointer type.
    
    :param var: Pointer instance of ctypes type
    :type var: :py:mod:`ctypes` instance
    :param typ: Target pointer class
    :type typ: :py:mod:`fancytypes` type
    :return: Pointer to a ctypes instance
    :rtype: :py:mod:`ctypes` instance of pointer type
    '''
    
    if not hasattr(typ, '_ctype_'):
        errmsg = 'fancytypes.cast must receive a fancytypes type'
        raise TypeError(errmsg)
    
    new_var = cast_(var, typ._ctype_)
    
    return new_var
