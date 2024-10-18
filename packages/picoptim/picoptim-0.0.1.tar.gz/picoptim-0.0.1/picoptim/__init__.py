"""
Optimisation module

Main classes:
- Optimizer, dummy class for optimisation algorithms. Optimizer loops on
    "update" method until convergence or maximum number of iteration reached.
    "update" should be reimplemented for each specific routine.
- CMAOptimizer, class for CMA-ES optimisation routine
- MHOptimizer, class for a Metropolis-Hastings inspired optimisation routine
- OptimResult, main class for output of optimisation algorithm

Optimisation can be performed using "optim" function, with optimisation method
specified by "optimizer" argument.

Other:
A dichotomy solver for f(x) = y is also provided by "dichoto" function
"""

from picoptim.fun_evals import FunEvals
from picoptim.generative_optim import (CMAOptimizer, GenOptimizer, MHOptimizer,
                                       OptimResultCMA)
from picoptim.optim import optim
from picoptim.optim_result import OptimResult
from picoptim.optimizer import Optimizer
from picoptim.search.dichoto import dichoto
