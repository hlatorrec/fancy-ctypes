.. _compiling:

Compiling a shared library
==========================

.. note::

    This brief introduction uses **C as the reference programming language** 
    and GCC (GNU) as the reference compiler.

Compiling code as a shared library may actually be **easier than making a full 
program in C** that requires a :code:`main` function, plus its own procedures 
to handle I/O (input & output). The later is noticeably tedious to do in some 
lower level languages, while Python can make it almost trivial. That means we 
can **write C code that performs the expensive calculations** and write the 
rest of the program in Python.

Even **old programs can be interfaced from Python**, provided that they were 
originally written in a modular way that separates the *"guts"* from the rest 
of the program. We can **keep the parts of the original code that we need** and 
build a new interface from Python.

The following code snippet can be saved into a text file :code:`example.c` and 
compiled into a shared library.

.. code-block:: c
    
    int add_doubled_integers (int a, int b) {
        int c;
        c = 2 * a + 2 * b;
        return c;
    }

On a Unix system, we simply type the following into the terminal:

.. code-block:: console
    
    $ gcc -shared -fPIC example.c -o example.so

* :code:`-shared` tells the compiler to compile it as a shared library
* :code:`-fPIC`  tells the compiler to compile it as `position independent code 
  <https://en.wikipedia.org/wiki/Position-independent_code>`_

The :code:`.so` extension is short for *shared object* and is commonly used in 
shared libraries compiled for Unix systems. For Windows systems, :code:`.dll` 
is the commonly used extension. This is just a convention, but it is worth 
following so other people know what these files are within a project. Please, 
**do not** use *.exe* if you work in Windows.
