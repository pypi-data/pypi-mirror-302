from abc import ABC, abstractmethod
from typing import Callable, Iterable, Optional

import numpy as np
from picoptim.exhaustive.brute_force import BruteForceOptimizer


def gridify(*values: np.ndarray) -> np.ndarray:
    """From tuple of list [a_11, ..., a_1n], ..., [a_k1, ..., akm],
    returns array
        [[a_11, ..., ak1], ... [a11, ..., akm],
        ...,
        [a1n, ..., ak1], ..., [a1n, ..., akm]]
    """
    n_dim = len(values)
    n_per_dim = tuple(len(v) for v in values)

    gshape = (1,) + n_per_dim + (n_dim,)
    grid = np.zeros(gshape)

    for dim, v in enumerate(values):
        for j, x in enumerate(v):
            grid[:, j, ..., dim] = x
        grid.shape = (grid.shape[0] * grid.shape[1],) + grid.shape[2:]

    return grid


class GridSearchOptimizer(BruteForceOptimizer):
    """Grid Search optimisation routine"""

    def __init__(
        self,
        fun: Callable[[np.ndarray], float],
        vals_per_dim: tuple[np.ndarray],
        kwargs: Optional[dict] = None,
        parallel: bool = False,
        vectorized: bool = False,
        silent=False,
    ):
        super().__init__(
            fun=fun,
            pars_to_eval=gridify(*vals_per_dim),
            kwargs=kwargs,
            parallel=parallel,
            vectorized=vectorized,
            silent=silent,
        )


class RegularGridSearchOptimizer(GridSearchOptimizer, ABC):
    def __init__(
        self,
        fun: Callable[[np.ndarray], float],
        grid_data: Iterable[tuple[float, float, int]],
        kwargs: Optional[dict] = None,
        parallel: bool = False,
        vectorized: bool = False,
        silent=False,
    ):
        vals_per_dim = self.mk_grid(grid_data)
        super().__init__(
            fun=fun,
            vals_per_dim=vals_per_dim,
            kwargs=kwargs,
            parallel=parallel,
            vectorized=vectorized,
            silent=silent,
        )

    @abstractmethod
    def mk_grid(self, grid_data) -> tuple[np.ndarray]:
        pass


class LinearGridSearchOptimizer(RegularGridSearchOptimizer):
    """Grid Search optimisation routine with a linear grid

    Args:
        grid_data: Iterable of tuple containing mimimal value,
            maximum value and number of values
    """

    def mk_grid(
        self,
        grid_data: Iterable[tuple[float, float, int]],
    ):
        # Check grid_data
        for xmin, xmax, n in grid_data:
            assert xmin <= xmax
            assert isinstance(n, int)

        # If xmin = xmax, change n to 1 to avoid recomputation
        _grid_data = [
            (xmin, xmax, n) if xmin < xmax else (xmin, xmax, 1)
            for xmin, xmax, n in grid_data
        ]
        return tuple(
            np.linspace(xmin, xmax, n, endpoint=True) for xmin, xmax, n in _grid_data
        )


class GeometricGridSearchOptimizer(RegularGridSearchOptimizer):
    """Grid Search optimisation routine with a geometric grid

    Args:
        grid_data: Iterable of tuple containing mimimal value,
            maximum value and number of values
    """

    def mk_grid(
        self,
        grid_data: Iterable[tuple[float, float, int]],
    ):

        # Check grid_data
        for xmin, xmax, n in grid_data:
            assert xmin <= xmax
            assert xmin * xmax > 0
            assert isinstance(n, int)

        # If xmin = xmax, change n to 1 to avoid recomputation
        _grid_data = [
            (xmin, xmax, n) if xmin < xmax else (xmin, xmax, 1)
            for xmin, xmax, n in grid_data
        ]

        return tuple(
            np.geomspace(xmin, xmax, n, endpoint=True) for xmin, xmax, n in _grid_data
        )
