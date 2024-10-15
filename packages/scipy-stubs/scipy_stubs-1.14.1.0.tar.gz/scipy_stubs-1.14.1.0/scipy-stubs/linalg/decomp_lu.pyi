# This file is not meant for public use and will be removed in SciPy v2.0.0.

from typing_extensions import deprecated

__all__ = ["LinAlgWarning", "get_lapack_funcs", "lu", "lu_factor", "lu_solve"]

@deprecated("will be removed in SciPy v2.0.0")
class LinAlgWarning(RuntimeWarning): ...

@deprecated("will be removed in SciPy v2.0.0")
def get_lapack_funcs(
    names: object,
    arrays: object = ...,
    dtype: object = ...,
    ilp64: object = ...,
) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def lu(
    a: object,
    permute_l: object = ...,
    overwrite_a: object = ...,
    check_finite: object = ...,
    p_indices: object = ...,
) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def lu_factor(
    a: object,
    overwrite_a: object = ...,
    check_finite: object = ...,
) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def lu_solve(
    lu_and_piv: object,
    b: object,
    trans: object = ...,
    overwrite_b: object = ...,
    check_finite: object = ...,
) -> object: ...
