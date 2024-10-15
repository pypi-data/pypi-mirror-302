import io
from collections.abc import Iterable, Mapping
from typing import IO, Any, Final, Literal, TypeAlias, TypedDict, final, type_check_only

import numpy as np
import numpy.typing as npt
from scipy._typing import AnyShape, ByteOrder
from scipy.sparse import sparray, spmatrix
from ._miobase import MatFileReader

_GenericArray: TypeAlias = np.ndarray[tuple[int, ...], np.dtype[np.generic]]
_OnedAs: TypeAlias = Literal["row", "column"]

@type_check_only
class _MatFile5Header(TypedDict):
    __header__: str
    __version__: str

NDT_FILE_HDR: Final[np.dtype[np.generic]]
NDT_TAG_FULL: Final[np.dtype[np.generic]]
NDT_TAG_SMALL: Final[np.dtype[np.generic]]
NDT_ARRAY_FLAGS: Final[np.dtype[np.generic]]

@final
class EmptyStructMarker: ...

class MatFile5Reader(MatFileReader):
    uint16_codec: Final[str]

    def __init__(
        self,
        /,
        mat_stream: IO[bytes],
        byte_order: ByteOrder | None = None,
        mat_dtype: bool = False,
        squeeze_me: bool = False,
        chars_as_strings: bool = True,
        matlab_compatible: bool = False,
        struct_as_record: bool = True,
        verify_compressed_data_integrity: bool = True,
        uint16_codec: str | None = None,
        simplify_cells: bool = False,
    ) -> None: ...
    def read_file_header(self, /) -> _MatFile5Header: ...
    def initialize_read(self, /) -> None: ...
    def read_var_header(self, /) -> tuple[object, int]: ...
    def read_var_array(self, /, header: Mapping[str, object], process: bool = True) -> _GenericArray: ...
    def get_variables(
        self,
        /,
        variable_names: Iterable[str] | None = None,
    ) -> dict[str, str | list[str] | _GenericArray]: ...
    def list_variables(self, /) -> list[tuple[str, tuple[int, ...], str]]: ...

class VarWriter5:
    mat_tag: _GenericArray
    file_stream: IO[bytes]
    unicode_strings: bool
    long_field_names: bool
    oned_as: _OnedAs
    def __init__(self, /, file_writer: MatFile5Writer) -> None: ...
    def write_bytes(self, /, arr: _GenericArray) -> None: ...
    def write_string(self, /, s: str) -> None: ...
    def write_element(self, /, arr: _GenericArray, mdtype: int | None = None) -> None: ...
    def write_smalldata_element(self, /, arr: _GenericArray, mdtype: int, byte_count: int) -> None: ...
    def write_regular_element(self, /, arr: _GenericArray, mdtype: int, byte_count: int) -> None: ...
    def write_header(
        self,
        /,
        shape: AnyShape,
        mclass: int,
        is_complex: bool = False,
        is_logical: bool = False,
        nzmax: int = 0,
    ) -> None: ...
    def update_matrix_tag(self, /, start_pos: int) -> None: ...
    def write_top(self, /, arr: npt.ArrayLike, name: str, is_global: bool) -> None: ...
    def write(self, /, arr: npt.ArrayLike) -> None: ...
    def write_numeric(self, /, arr: npt.NDArray[np.bool_ | np.number[Any]]) -> None: ...
    def write_char(self, /, arr: npt.NDArray[np.str_], codec: str = "ascii") -> None: ...
    def write_sparse(self, /, arr: spmatrix | sparray) -> None: ...
    def write_cells(self, /, arr: _GenericArray) -> None: ...
    def write_empty_struct(self, /) -> None: ...
    def write_struct(self, /, arr: npt.NDArray[np.void]) -> None: ...
    def write_object(self, /, arr: npt.NDArray[np.object_]) -> None: ...

class MatFile5Writer:
    file_stream: IO[bytes]
    do_compression: bool
    unicode_strings: bool
    global_vars: list[str] | tuple[str, ...]
    long_field_names: bool
    oned_as: _OnedAs
    def __init__(
        self,
        /,
        file_stream: IO[bytes],
        do_compression: bool = False,
        unicode_strings: bool = False,
        global_vars: list[str] | tuple[str, ...] | None = None,
        long_field_names: bool = False,
        oned_as: _OnedAs = "row",
    ) -> None: ...
    def write_file_header(self, /) -> None: ...
    def put_variables(self, /, mdict: Mapping[str, _GenericArray], write_header: bool | None = None) -> None: ...

def varmats_from_mat(file_obj: IO[bytes]) -> list[tuple[str, io.BytesIO]]: ...
def to_writeable(source: object) -> _GenericArray | type[EmptyStructMarker] | None: ...
