import numpy as np
from typing import TypeVar
from numpy.typing import DTypeLike, NDArray
from .dogma_rust import concatenate_numpy as concatenate_arrays
from contextlib import contextmanager
from time import time

_T = TypeVar("_T", bound=np.generic, covariant=True)


def concatenate_numpy(
    arrays: list[NDArray[_T]],
) -> tuple[NDArray[_T], NDArray[np.int64]]:
    arr, cu = concatenate_arrays(arrays)
    dtype: DTypeLike = arrays[0].dtype
    arr = arr.view(dtype)
    cu //= dtype.itemsize
    return arr, cu


@contextmanager
def timer(name):
    print(f"{name}...")
    start = time()
    yield
    print(f"{name} took {time() - start} seconds")
