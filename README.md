# FancyTypes

Syntax sugar for [ctypes](https://docs.python.org/3/library/ctypes.html) that provides a more **confortable way to load and setup shared libraries** for your projects. The goal of this simple package is to **reduce boilerplate and replace tedious syntax with something more intuitive** and fancier.

### Features

- Load shared libraries and only interface the desired procedures.
- Parse argument and result types together through a dedicated parser function.
- Multiple type aliases available (e.g. *real64* / *float64* for 64-bit floating point numbers)
- Improved syntax to define C struct and union types
- Tools to work with NumPy arrays

All ctypes types are compatible even if FancyTypes does not provide its own specific class for them. For example, char support is limited since the main focus of the package is numerical computing, so syntax improvements to pass strings around are limited to turning them into NumPy arrays and not much else. Typically, strings and I/O can be handled on the Python side.

### Dependency free

The only dependency is NumPy for array handling. The NumPy package is pretty much part of the standard library amongst the Python numerical computing ecosystem, so any project that could potentially use this will most likely already depend on NumPy on its own.

### Documentation

Read the [documentation](https://hlatorrec.github.io/fancy-ctypes/) and find out if this package could be useful to you.

### Installation and importing

The package can be installed from PyPI

```bash
pip install fancy-ctypes
```

Alternatively, download this repository and run

```bash
pip install .
```

The package is imported as

```python
import fancytypes

# For confort
import fancytypes as ft
```

### Platform

The package is intended to be platform agnostic, although shared libraries are not. This is a tool that interfaces those libraries with Python, but users still need to build them first however they want.
