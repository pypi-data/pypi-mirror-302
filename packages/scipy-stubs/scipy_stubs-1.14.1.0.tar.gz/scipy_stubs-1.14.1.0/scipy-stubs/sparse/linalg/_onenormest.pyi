from scipy._typing import Untyped

__all__ = ["onenormest"]

def onenormest(A, t: int = 2, itmax: int = 5, compute_v: bool = False, compute_w: bool = False) -> Untyped: ...
def sign_round_up(x) -> Untyped: ...
def elementary_vector(n, i) -> Untyped: ...
def vectors_are_parallel(v, w) -> Untyped: ...
def every_col_of_X_is_parallel_to_a_col_of_Y(X, Y) -> Untyped: ...
def column_needs_resampling(i, X, Y: Untyped | None = None) -> Untyped: ...
def resample_column(i, X): ...
def less_than_or_close(a, b) -> Untyped: ...
