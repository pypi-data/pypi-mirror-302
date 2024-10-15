from typing import Final, Literal, TypeAlias, overload
from typing_extensions import LiteralString

import numpy as np

# TODO: stub `pooch` (this should be a `pooch.code.Pooch`)
_DataFetcher: TypeAlias = object
data_fetcher: Final[_DataFetcher]

def fetch_data(dataset_name: LiteralString, data_fetcher: _DataFetcher = ...) -> LiteralString: ...
def ascent() -> np.ndarray[tuple[Literal[512], Literal[512]], np.dtype[np.uint8]]: ...
def electrocardiogram() -> np.ndarray[tuple[Literal[108_000]], np.dtype[np.float64]]: ...
@overload
def face(gray: Literal[False] = False) -> np.ndarray[tuple[Literal[768], Literal[1_024], Literal[3]], np.dtype[np.uint8]]: ...
@overload
def face(gray: Literal[True]) -> np.ndarray[tuple[Literal[768], Literal[1_024]], np.dtype[np.uint8]]: ...
