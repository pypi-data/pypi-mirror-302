# This module is not meant for public use and will be removed in SciPy v2.0.0.
from typing_extensions import deprecated

__all__ = [
    "csr_count_blocks",
    "csr_matrix",
    "csr_tobsr",
    "csr_tocsc",
    "get_csr_submatrix",
    "isspmatrix_csr",
    "spmatrix",
    "upcast",
]

@deprecated("will be removed in SciPy v2.0.0")
class spmatrix:
    @property
    def shape(self) -> tuple[int, ...]: ...
    def __mul__(self, other: object, /) -> object: ...
    def __rmul__(self, other: object, /) -> object: ...
    def __pow__(self, power: object, /) -> object: ...
    def set_shape(self, shape: object) -> None: ...
    def get_shape(self) -> tuple[int, ...]: ...
    def asfptype(self) -> object: ...
    def getmaxprint(self) -> object: ...
    def getformat(self) -> object: ...
    def getnnz(self, axis: object | None = None) -> object: ...
    def getH(self) -> object: ...
    def getcol(self, j: int) -> object: ...
    def getrow(self, i: int) -> object: ...

@deprecated("will be removed in SciPy v2.0.0")
class csr_matrix: ...

@deprecated("will be removed in SciPy v2.0.0")
def isspmatrix_csr(x: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def csr_count_blocks(*args: object, **kwargs: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def csr_tobsr(*args: object, **kwargs: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def csr_tocsc(*args: object, **kwargs: object) -> object: ...
@deprecated("will be removed in SciPy v2.0.0")
def get_csr_submatrix(*args: object, **kwargs: object) -> object: ...

# sputils
@deprecated("will be removed in SciPy v2.0.0")
def upcast(*args: object) -> object: ...
