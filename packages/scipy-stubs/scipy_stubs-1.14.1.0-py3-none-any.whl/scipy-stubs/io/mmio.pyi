# This module is not meant for public use and will be removed in SciPy v2.0.0.
from typing_extensions import deprecated

__all__ = ["mminfo", "mmread", "mmwrite"]

@deprecated("will be removed in SciPy v2.0.0")
def mminfo(source: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def mmread(source: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def mmwrite(
    target: object,
    a: object,
    comment: object = ...,
    field: object = ...,
    precision: object = ...,
    symmetry: object = ...,
) -> None: ...
