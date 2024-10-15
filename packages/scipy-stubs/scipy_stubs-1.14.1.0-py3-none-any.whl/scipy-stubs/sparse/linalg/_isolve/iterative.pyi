from scipy._typing import Untyped

__all__ = ["bicg", "bicgstab", "cg", "cgs", "gmres", "qmr"]

def bicg(
    A,
    b,
    x0: Untyped | None = None,
    *,
    rtol: float = 1e-05,
    atol: float = 0.0,
    maxiter: Untyped | None = None,
    M: Untyped | None = None,
    callback: Untyped | None = None,
) -> Untyped: ...
def bicgstab(
    A,
    b,
    x0: Untyped | None = None,
    *,
    rtol: float = 1e-05,
    atol: float = 0.0,
    maxiter: Untyped | None = None,
    M: Untyped | None = None,
    callback: Untyped | None = None,
) -> Untyped: ...
def cg(
    A,
    b,
    x0: Untyped | None = None,
    *,
    rtol: float = 1e-05,
    atol: float = 0.0,
    maxiter: Untyped | None = None,
    M: Untyped | None = None,
    callback: Untyped | None = None,
) -> Untyped: ...
def cgs(
    A,
    b,
    x0: Untyped | None = None,
    *,
    rtol: float = 1e-05,
    atol: float = 0.0,
    maxiter: Untyped | None = None,
    M: Untyped | None = None,
    callback: Untyped | None = None,
) -> Untyped: ...
def gmres(
    A,
    b,
    x0: Untyped | None = None,
    *,
    rtol: float = 1e-05,
    atol: float = 0.0,
    restart: Untyped | None = None,
    maxiter: Untyped | None = None,
    M: Untyped | None = None,
    callback: Untyped | None = None,
    callback_type: Untyped | None = None,
) -> Untyped: ...
def qmr(
    A,
    b,
    x0: Untyped | None = None,
    *,
    rtol: float = 1e-05,
    atol: float = 0.0,
    maxiter: Untyped | None = None,
    M1: Untyped | None = None,
    M2: Untyped | None = None,
    callback: Untyped | None = None,
) -> Untyped: ...
