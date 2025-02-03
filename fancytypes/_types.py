# -*- coding: utf-8 -*-
"""
Base class.
"""



from ctypes import POINTER, byref


from numpy import ndarray



class FancyMeta(type):
    '''Metaclass for :py:mod:`fancytypes` type classes.
    
    Attributes:
        :_ctype_: Underlying :py:mod:`ctypes` type
        :_numpy_: Matching NumPy type for :py:meth:`array` checks
        :_alias_: Fancy name for :py:meth:`__repr__`
    '''
    
    _ctype_ = None
    _numpy_ = None
    _alias_ = None
    
    def __repr__(cls):
        '''Repr method for :py:mod:`fancytypes` type classes.
        '''
        
        return f'fancytypes.{cls._alias_}'
    
    def __setattr__(cls, name, value):
        '''Raise exception.
        '''
        
        errmsg = 'cannot set attributes to FancyTypes type'
        raise TypeError(errmsg)
    
    def __getattr__(cls, name):
        '''Monkeypatch.
        '''
        
        if name != 'dtype':
            this_class = cls.__name__
            errmsg = f'no attribute "{name}" in type class {this_class}'
            raise AttributeError(errmsg)
        
        return cls._numpy_
    
    def __mul__(cls, other):
        '''Array generation method.
        '''
        
        if not isinstance(other, int):
            received = other.__class__.__name__
            errmsg = f'array length must be of type int, not {received}'
            raise TypeError(errmsg)
            
        if other < 0:
            errmsg = 'array length must be positive'
            raise ValueError(errmsg)
        
        type_name = f'{cls.__name__}_Array_{other}'
        
        dict_ = {
            '_ctype_' : cls._ctype_*other,
            '_numpy_' : cls._numpy_,
            '_alias_' : f'{cls._alias_}_array_{other}',
            }
        
        new_type = type(type_name, (cls.__base__,), dict_)
        
        return new_type
    
    def __rmul__(cls, other):
        '''Array generation method.
        '''
        
        return cls.__mul__(other)
    
    def __getitem__(cls, size):
        '''Mimic C-style array declaration.
        '''
        
        return size * cls
    
    def _pointer(cls):
        '''Get a pointer class.
        '''
        
        type_name = f'Ptr_{cls.__name__}'
        
        dict_ = {
            '_ctype_' : POINTER(cls._ctype_),
            '_numpy_' : cls._numpy_,
            '_alias_' : f'ptr_{cls._alias_}',
            }
        
        new_type = type(type_name, (cls.__base__,), dict_)
        
        return new_type
    
    def from_param(cls, param):
        '''Support for :py:mod:`ctypes`.
        '''
        
        return cls._ctype_.from_param(param)
    
    def array(cls, array):
        '''Get pointer to array, necessary to pass arrays into binaries.
        
        :param array: NumPy array
        :type array: :py:class:`numpy.ndarray`
        '''
        
        if not isinstance(array, ndarray):
            errmsg = 'array must be a NumPy array'
            raise TypeError(errmsg)
        
        # Skip check for string or byte arrays, not too clean but w/e
        if not isinstance(array[0], (str, bytes)) \
            and array.dtype != cls._numpy_:
                errmsg = 'array dtype does not match fancytypes type'
                raise TypeError(errmsg)
        
        return array.ctypes.data_as(POINTER(cls._ctype_))
    
    def byref(cls, value):
        '''Get reference to :py:mod:`ctypes` instance, pass by reference with 
        no pointer instance created. Not really useful unless explicitly 
        working with :py:mod:`ctypes` type instances.
        '''
        
        if not isinstance(value, cls._ctype_):
            value = cls._ctype_(value)
        
        return byref(value)



class FancyType(metaclass=FancyMeta):
    '''Base class for :py:mod:`fancytypes` type classes that implements common 
    functionality. It acts as a bridge between :py:class:`FancyMeta` and basic 
    type classes.
    '''
    
    _ctype_ = None
    _numpy_ = None
    _alias_ = 'type'
    
    def __new__(cls, *values):
        '''Return a :py:mod:`ctypes` instance that matches the type.
        '''
        
        return cls._ctype_(*values)



class ComplexType(metaclass=FancyMeta):
    '''Base class for complex types that adjusts some methods to fit these 
    types.
    '''
    
    _ctype_ = None
    _numpy_ = None
    _alias_ = 'complextype'
    
    def __new__(cls, *values):
        '''This makes the underlying struct work with pointer and array types, 
        which is convoluted because of how :py:mod:`ctypes` works.
        '''
        
        ctype = cls._ctype_
        
        if not hasattr(ctype, '_type_'): # It is a single complex number
            value, = values
            return cls._ctype_(value.real, value.imag)
            
        elif not hasattr(ctype._type_, 'contents') and \
            not hasattr(ctype, 'contents'): # It is a complex number array
            iter_complex = (cls._ctype_._type_(value.real, value.imag)
                                                        for value in values)
            return cls._ctype_(*iter_complex)
            
        else: # It has to be a pointer type
            return cls._ctype_(*values)
    
    @classmethod
    def byref(cls, value):
        '''Pass complex type by reference.
        '''
        
        return byref(cls._ctype_(value.real, value.imag))
    
    @classmethod
    def from_param(cls, param):
        '''Support for :py:mod:`ctypes`. This might not work with arrays, but 
        that is fine since arrays must be passed with :py:meth:`array`
        '''
        
        return cls._ctype_(param.real, param.imag)
