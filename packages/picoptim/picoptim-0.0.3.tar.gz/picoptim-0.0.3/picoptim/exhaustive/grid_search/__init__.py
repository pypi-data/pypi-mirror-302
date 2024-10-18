"""Optimisation solver evaluating points on regular grids of form
(X_{1,j_1}, X_{2,j_2}, ... X_{d, j_d})

for all 0 <= j_i <= n_i and pre determined values X_{i,j}
"""

from picoptim.exhaustive.grid_search.grid_search import (
    GeometricGridSearchOptimizer,
    GridSearchOptimizer,
    LinearGridSearchOptimizer,
    RegularGridSearchOptimizer,
)
