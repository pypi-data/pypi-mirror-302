from abc import ABC, abstractmethod
from functools import partial
from typing import Callable, Optional, Protocol

import numpy as np
from apicutils import blab
from multiprocess import Pool

from picoptim.fun_evals import FunEvals
from picoptim.optim_result import OptimResult


class OptimProtocol(Protocol):
    """Protocol for Optimizer.

    Inheriting from 'Optimizer' (which implements this protocol) is the
    recommanded option for those wishing to implement there own optimisation
    routine from scratch. If this is not practicable, the class should still
    implement the protocol if it is to be used in conjonction with the 'optim'
    module.
    """

    def __init__(
        self,
        fun: Callable[[np.ndarray], float],
        kwargs: Optional[dict] = None,
        # Function evaluation
        parallel: bool = False,
        vectorized: bool = False,
    ):
        ...

    def optimize(self) -> None:
        """Inplace optimisation routine"""

    def process_result(self) -> OptimResult:
        """Process outputs of the optimisation routine and return them as an OptimResult"""


class Optimizer(ABC):
    """Optimizer class.

    Args:
        fun: function to be minimized.
            Should take np.ndarray as input and return float.
        kwargs: further keyword arguments passed to fun
        parallel: indicates if function calls should be parallelized.
            Default is False. Disregarded is vectorized is True
        vectorized: indicates if the function is vectorized.
            Default is False.
        silent: indicates if there should be prints.
    """

    def __init__(
        self,
        fun: Callable[[np.ndarray], float],
        kwargs: Optional[dict] = None,
        # Function evaluation
        parallel: bool = False,
        vectorized: bool = False,
        # Printing
        silent=False,
    ):
        self.fun = fun

        if kwargs is None:
            kwargs = {}

        if vectorized:
            self.parallel = False
        else:
            self.parallel = parallel
        self.vectorized = vectorized

        if self.parallel:
            self.pool = Pool()
        else:
            self.pool = None

        self.converged = False

        self.silent = silent

        self.kwargs = kwargs

        self.loc_fun = partial(fun, **kwargs)

    def msg_begin_calib(self) -> None:
        """Optional print at the beginning of the calibration routine"""
        blab(self.silent, "Beginning optimisation routine")

    def msg_end_calib(self) -> None:
        """Optional print at the end of the calibration routine"""
        blab(self.silent, "Optimisation procedure completed")
        if self.converged:
            blab(self.silent, f"Converged")
        else:
            blab(self.silent, "Did not converge")

    def mfun(self, xs: np.ndarray) -> np.ndarray:
        """Multiple calls to 'fun' with automatic parallelisation/vectorisation handling"""
        if self.parallel:
            return np.array(self.pool.map(self.loc_fun, xs))
        elif self.vectorized:
            return self.loc_fun(xs)  # type: ignore
        else:
            return np.array([self.loc_fun(x) for x in xs])

    @abstractmethod
    def _optimize(self):
        pass

    def optimize(self):
        self.msg_begin_calib()

        try:
            self._optimize()
            err = {"failed": False, "err": None}
        except Exception as exc:
            err = {"failed": True, "err": exc}
        # Close pool of worker if required
        if self.parallel:
            self.pool.terminate()
        if err["failed"]:
            raise err["err"]

        self.msg_end_calib()

    def process_result(self) -> OptimResult:
        """Process Optimizer result to OptimResult"""
        return OptimResult(
            opti_param=None,
            converged=self.converged,
        )


class IterOptimizer(Optimizer, ABC):
    """
    Abstract class for Optimizer using an iterative strategy (i.e. looping
    on an update step).

    The 'update' method must be reimplemented.
    """

    def __init__(
        self,
        fun: Callable[[np.ndarray], float],
        param_ini: np.ndarray,
        # Termination criteria
        chain_length: int,
        xtol: float = 10 ** (-8),
        ftol: float = 10 ** (-8),
        delta_conv_check: int = 1,
        # Function evaluation
        kwargs: Optional[dict] = None,
        parallel: bool = False,
        vectorized: bool = False,
        # Printing
        silent: bool = False,
        print_rec: int = 5,
    ):
        super().__init__(
            fun, parallel=parallel, vectorized=vectorized, silent=silent, kwargs=kwargs
        )
        self.chain_length = chain_length

        self.xtol = xtol
        self.ftol = ftol
        self.delta_conv_check = delta_conv_check

        self.count = 0

        self.print_rec = print_rec

        self.kwargs = kwargs

        self.param = np.array(param_ini)  # Force copy to avoid side effects
        self.score: float = self.loc_fun(self.param)

        self.hist_log = FunEvals(self.param.shape, n_tot=2 + chain_length)
        self.add_log()

    def add_log(self):
        """Logs the result of the update to the history of the optimisation routine"""
        self.hist_log.add1(self.param, self.score)

    @abstractmethod
    def update(self):
        """Dummy update rule for optimizer
        This method should be reimplemented by specific optimizer routine
        """
        self.count += 1
        self.add_log()
        # No convergence check here

    def _optimize(self):
        """Main optimisation calls. Loops on update method until convergence or exceeds max evaluations"""
        try:
            while (self.count < self.chain_length) and (not self.converged):
                self.update()
            if self.parallel:
                self.pool.close()
        except Exception as exc:
            # Terminate pool of worker if parallel
            if self.parallel:
                self.pool.terminate()
            raise exc

    def msg_begin_step(self) -> None:
        silent_loc = self.silent or (self.count % self.print_rec != 0)
        blab(silent_loc, f"Score at step {self.count}: {self.score}")

    def msg_end_step(self) -> None:
        return None

    def check_convergence(self):
        """Default convergence check for optimisation routine
        Stops if either score evolution or parameter evolution are
        less than ftol (xtol for parameter evolution, for all parameters)
        """
        if self.count > self.delta_conv_check:
            xs = self.hist_log.params(self.delta_conv_check)
            delta_x = (xs[0] - xs[-1]) / self.delta_conv_check
            converged_x = np.all(np.abs(delta_x)) < self.xtol

            fs = self.hist_log.vals(self.delta_conv_check)
            delta_f = (fs[0] - fs[-1]) / self.delta_conv_check
            converged_f = delta_f < self.ftol

            self.converged = converged_x or converged_f
        else:
            self.converged = False

    def mfun(self, xs):
        """Multiple calls to 'fun' with automatic parallelisation/vectorisation handling"""
        if self.parallel:
            return np.array(self.pool.map(self.loc_fun, xs))
        elif self.vectorized:
            return self.loc_fun(xs)
        else:
            return np.array([self.loc_fun(x) for x in xs])

    def get_hyperparams(self) -> dict:
        return {
            "xtol": self.xtol,
            "ftol": self.ftol,
            "chain_length": self.chain_length,
        }

    def process_result(self) -> OptimResult:
        return OptimResult(
            opti_param=self.param,
            converged=self.converged,
            opti_score=self.score,
            hist_param=self.hist_log.params(),
            hist_score=self.hist_log.vals(),
            hyperparams=self.get_hyperparams(),
        )
