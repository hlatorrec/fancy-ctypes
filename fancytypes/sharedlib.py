# -*- coding: utf-8 -*-
"""
Library interfaces
==================

After loading a shared library, its **procedures must be interfaced to make 
them available from the Python side**. Shared libraries are loaded using the 
:py:func:`load` function, which returns a :py:class:`SharedLibrary` instance. 
Procedures can be interfaced using the :py:func:`interface` function.

Now follows a minimal example of C code that we can interface from Python, with  
arguments chosen to cover typical cases. Function and class documentation 
:ref:`just below <docu>`.

.. code-block:: c
    
    // Sample structure that stores seismic station information
    typedef struct {
        double longitude;
        double latitude;
        double elevation;
        char network[2];
        char station[5];
        _Bool operational; // OCD safety (it would get padded anyways)
    } t_Station;
    
    // Sample function prototype that will be interfaced
    int do_something (t_Station *station, double *data, unsigned int nsamp);

When building an interface, we will assume that :code:`data` is a NumPy array.

.. code-block:: python
    
    import fancytypes as ft
    
    # This ctypes struct is equivalent to the one above
    @ft.cstruct
    class Station:
        longitude : ft.real64
        latitude : ft.real64
        elevation : ft.real64
        network : ft.character[2]
        station : ft.character[5]
        operational : ft.logical
    
    # We load the library first
    library = ft.load(<path_to_library>)
    
    # Now we can interface any procedure we need
    library.do_something = ft.interface(ft.pointer(Station), 
                                        ft.pointer(ft.real64),
                                        ft.uint32,
                                        returns=ft.int32)
    
    # Create some empty dummy variables
    import numpy as np
    nsamp = 100
    data = np.zeros(100, dtype=np.double)
    station = Station()    
    
    # Call the procedure
    res = library.do_something(station, ft.real64.array(data), nsamp)
    
    # If "data" is always a NumPy array, we can rely on their API instead
    library.do_something = ft.interface(ft.pointer(Station), 
                                        ft.nparray(ft.real64), # nparray instead of pointer
                                        ft.uint32,
                                        returns=ft.int32)
    
    # The call will now look cleaner but less explicit
    res = library.do_something(station, data, nsamp)

It is important to note that **ctypes will always try to make any necessary 
type conversions**, such as passing a pointer even if we make the call using 
the variable. This happens in the example above when we pass :code:`station` 
instead of :code:`ft.cpointer(station)`. NumPy arrays require us to go through 
the :code:`array` method of the corresponding type class unless we rely on the 
:py:mod:`numpy.ctypeslib` API.

.. _docu:

.. autoclass:: SharedLibrary()
.. autofunction:: load
.. autofunction:: interface
.. autoclass:: LibraryError
    :no-index:
"""



from ctypes import CDLL
from pathlib import Path
from os import name as windows_check



class SharedLibrary:
    '''Class to store loaded shared libraries and their interfaces. Use the 
    :py:func:`load` function to load them. Any **procedures from the library 
    must first be explicitly interfaced to make them callable** from Python. 
    Interfaces can be built by **assigning a two-tuple containing argument and 
    return types to an attribute with the same name as the procedure**.
    
    .. code-block::
        
        <library>.<procedure> = ((<arg_type_1>, ..., <arg_type_n>), <res_type>)
    
    Use the :py:func:`interface` function to make the right side more readable. 
    These **assigned attributes are callable** and will run the procedure after 
    :py:mod:`ctypes` does the corresponding checks and attempts to make any 
    necessary conversions.
    
    .. code-block::
        
        <res> = <library>.<procedure>(<arg_1>, ..., <arg_n>)
    
    Procedures can have :code:`void` returns if :py:obj:`None` is assigned as 
    return type on the interface.
    
    .. warning::
        
        Procedure interfaces are not guaranteed to match on both sides, and 
        there is no way to check for it. Users are responsible of ensuring the 
        arguments declared are correct for proper functionality. Wrong 
        interfaces will result in unintended behaviour at best and are likely 
        to crash the Python interpreter.
    '''
    
    def __init__(self, path):
        
        if not isinstance(path, (str, Path)):
            errmsg = 'path must be a pathlike object'
            raise TypeError(errmsg)
        
        path = Path(path).resolve()
        
        self.__dict__['_path_'] = path
        self.__dict__['_name_'] = path.name
        
        try:
            
            if windows_check == 'nt': 
                from _ctypes import LoadLibrary
                self.__dict__['_lib_'] = CDLL(name=str(path),
                                            handle=LoadLibrary(str(path)))
            else:
                self.__dict__['_lib_'] = CDLL(str(path))
            
        except FileNotFoundError:
            errmsg = f'could not load any shared library at "{self._path_}",' \
                      ' make sure the path is correct'
            raise LibraryError(errmsg) from None
    
    def __repr__(self):
        '''Repr method.
        '''
            
        return '<fancytypes.SharedLibrary object for shared library ' \
              f'"{self._name_}" at "{self._path_}">'
    
    def __setattr__(self, name, value):
        '''Setter method that loads a procedure if it exists and throws an 
        exception if it does not.
        '''
        
        try:
            symbol = getattr(self._lib_, name) # self._lib_.__getattr__(name)
        except AttributeError:
            errmsg = f'procedure {name} not found in {self._name_}'
            raise LibraryError(errmsg) from None
            
        args, res = value
        
        res = res._ctype_ if hasattr(res, '_ctype_') else res
        
        symbol.argtypes = args
        symbol.restype = res
        
        procedure = FancyProcedure(symbol, args, res, self._path_, name)
        
        self.__dict__[name] = procedure



class FancyProcedure:
    '''Class to interface shared object procedures and trivialize invocations. 
    These instances are not meant to be created "by hand", the shared object 
    loading class :py:class:`SharedLibrary` will manage that instead.
    
    :param symbol_ptr: Symbol exposed by a :py:class:`ctypes.CDLL` object
    :type symbol: :py:class:`ctypes.CDLL._FuncPtr`
    :param arguments: Argument types of the procedure
    :type arguments: list or tuple
    :param result: Result type of the procedure
    :type result: :py:mod:`fancytypes` or :py:mod:`ctypes` valid types
    :param lib_path: Path to shared library
    :type lib_path: str or :py:class:`pathlib.Path`
    :param symbol_name: Procedure name
    :type symbol_name: str
    '''
    
    def __init__(self, symbol_ptr, arguments=(), result=None,
                 lib_path=None, symbol_name=None):
        
        self._arguments_ = tuple(arguments)
        self._result_ = result
        self._path_ = lib_path
        self._name_ = symbol_name
        
        self._nargs_ = len(self._arguments_)
        
        self.__procedure__ = symbol_ptr
    
    def __repr__(self):
        '''Repr method.
        '''
        
        return f'<fancytypes.FancyProcedure object for symbol ' \
               f'"{self._name_}" at "{self._path_}">'
    
    def __call__(self, *args):
        '''Calls the procedure with the arguments provided.
        '''
        
        if len(args) != self._nargs_:
            errmsg = f'procedure {self._name_} expects {self._nargs_} ' \
                     f'arguments, got {len(args)} instead'
            raise LibraryError(errmsg)
        
        return self.__procedure__(*args)



def interface(*args, returns=None):
    '''Helper function to declare procedure interfaces on instances of 
    :py:class:`SharedLibrary` in a more readable way.
    
    .. code-block::
        
                ((<arg_type_1>, ..., <arg_type_n>), <res_type>)
                                       |
                                       V
        interface(<arg_type_1>, ..., <arg_type_2>, returns=<res_type>)
    
    :param args: Argument types
    :param returns: Return type, default is :py:obj:`None`
    '''
    
    return args, returns


def load(path):
    '''Return a :py:class:`SharedLibrary` instance that stores a loaded shared 
    library.
    
    :param path: Path to shared library
    :type path: :py:class:`str` or :py:class:`pathlib.Path`
    :return: Loaded shared library
    :rtype: :py:class:`SharedLibrary`
    '''
    
    return SharedLibrary(path)



class LibraryError(Exception):
    '''Exception raised by the package for issues related to shared libraries.
    '''
    
    pass
