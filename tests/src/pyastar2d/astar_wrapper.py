import ctypes
import numpy as np
import pyastar2d.astar
from typing import Optional, Tuple


# Define array types
ndmat_f_type = np.ctypeslib.ndpointer(
    dtype=np.float32, ndim=1, flags="C_CONTIGUOUS")
ndmat_i2_type = np.ctypeslib.ndpointer(
    dtype=np.int32, ndim=2, flags="C_CONTIGUOUS")

# Define input/output types
pyastar2d.astar.restype = ndmat_i2_type  # Nx2 (i, j) coordinates or None
pyastar2d.astar.argtypes = [
    ndmat_f_type,   # weights
    ctypes.c_int,   # height
    ctypes.c_int,   # width
    ctypes.c_int,   # start index in flattened grid
    ctypes.c_int,   # goal index in flattened grid
    ctypes.c_bool,  # allow diagonal
]


def astar_path(
        weights: np.ndarray,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        max_path_length: int = 10000,
        allow_diagonal: bool = False) -> Optional[np.ndarray]:
    assert weights.dtype == np.float32, (
        f"weights must have np.float32 data type, but has {weights.dtype}"
    )
    # For the heuristic to be valid, each move must cost at least 1.
    if weights.min(axis=None) < 1.:
        raise ValueError("Minimum cost to move must be 1, but got %f" % (
            weights.min(axis=None)))
    # Ensure start is within bounds.
    if (start[0] < 0 or start[0] >= weights.shape[0] or
            start[1] < 0 or start[1] >= weights.shape[1]):
        raise ValueError(f"Start of {start} lies outside grid.")
    # Ensure goal is within bounds.
    if (goal[0] < 0 or goal[0] >= weights.shape[0] or
            goal[1] < 0 or goal[1] >= weights.shape[1]):
        raise ValueError(f"Goal of {goal} lies outside grid.")

    height, width = weights.shape
    start_idx = np.ravel_multi_index(start, (height, width))
    goal_idx = np.ravel_multi_index(goal, (height, width))

    path = pyastar2d.astar.astar(
        weights.flatten(), height, width, start_idx, goal_idx, max_path_length
    )
    return path
