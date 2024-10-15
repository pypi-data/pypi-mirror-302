# This module is not meant for public use and will be removed in SciPy v2.0.0.
from typing_extensions import deprecated

__all__ = [
    "cspline1d",
    "cspline1d_eval",
    "cspline2d",
    "gauss_spline",
    "qspline1d",
    "qspline1d_eval",
    "sepfir2d",
    "spline_filter",
]

@deprecated("will be removed in SciPy v2.0.0")
def cspline1d(signal: object, lamb: object = ...) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def cspline1d_eval(cj: object, newx: object, dx: object = ..., x0: object = ...) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def cspline2d(signal: object, lamb: object = ..., precision: object = ...) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def gauss_spline(x: object, n: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def qspline1d(signal: object, lamb: object = ...) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def qspline1d_eval(cj: object, newx: object, dx: object = ..., x0: object = ...) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def spline_filter(Iin: object, lmbda: object = ...) -> object: ...

# _spline
@deprecated("will be removed in SciPy v2.0.0")
def sepfir2d(input: object, hrow: object, hcol: object) -> object: ...
