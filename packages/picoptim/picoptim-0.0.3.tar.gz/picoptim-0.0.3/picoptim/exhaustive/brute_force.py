from typing import Callable, Optional

import numpy as np

from picoptim.optim_result import OptimResult
from picoptim.optimizer import Optimizer


class BruteForceOptimizer(Optimizer):
    """Brute Force optimisation routine evaluating a sequence
    of possible parameters"""

    def __init__(
        self,
        fun: Callable[[np.ndarray], float],
        pars_to_eval: np.ndarray,
        kwargs: Optional[dict] = None,
        parallel: bool = False,
        vectorized: bool = False,
        silent: bool = False,
    ):
        super().__init__(
            fun=fun,
            kwargs=kwargs,
            parallel=parallel,
            vectorized=vectorized,
            silent=silent,
        )

        self.opti_score = np.inf
        self.pars_to_eval = pars_to_eval
        self.opti_param = self.pars_to_eval[0]  # Just to initialize
        self.pars_results = np.zeros(len(self.pars_to_eval))

    def _optimize(self) -> None:
        """Brute force evaluation of all parameters,
        then selection of minimal value"""
        self.pars_results = self.mfun(self.pars_to_eval)
        best_index = self.pars_results.argmin()
        self.opti_param = self.pars_to_eval[best_index]
        self.opti_score = self.pars_results[best_index]
        self.converged = True

    def process_result(self) -> OptimResult:
        return OptimResult(
            opti_param=self.opti_param,
            converged=self.converged,
            opti_score=self.opti_score,
            hist_param=self.pars_to_eval,
            hist_score=self.pars_results,
        )
