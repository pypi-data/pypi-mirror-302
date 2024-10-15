# This module is not meant for public use and will be removed in SciPy v2.0.0.
from typing_extensions import deprecated

__all__ = [
    "abcd_normalize",
    "cont2discrete",
    "normalize",
    "ss2tf",
    "ss2zpk",
    "tf2ss",
    "tf2zpk",
    "zpk2ss",
    "zpk2tf",
]

@deprecated("will be removed in SciPy v2.0.0")
def tf2ss(num: object, den: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def abcd_normalize(A: object = ..., B: object = ..., C: object = ..., D: object = ...) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def ss2tf(A: object, B: object, C: object, D: object, input: object = ...) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def zpk2ss(z: object, p: object, k: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def ss2zpk(A: object, B: object, C: object, D: object, input: object = ...) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def cont2discrete(system: object, dt: object, method: object = ..., alpha: object = ...) -> object: ...

# filter_design
@deprecated("will be removed in SciPy v2.0.0")
def normalize(b: object, a: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def tf2zpk(b: object, a: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def zpk2tf(z: object, p: object, k: object) -> object: ...
