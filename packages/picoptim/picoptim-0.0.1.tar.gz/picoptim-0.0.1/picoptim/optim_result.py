"""
Optimisation result classes
"""

import os
from typing import Callable, Optional, Sequence

import apicutils.basic_io as io
import numpy as np
from apicutils import par_eval


class OptimResult:
    """
    Class for output of optimization routines

    This class functions as an organized storage of optimisation related variables. These include
    - opti_param, the parameter returned by the optimisation routine
    - converged, whether the optimisation routine assumes convergence
    - opti_score, the score achieved by the optimisation routine (Optional)
    - hist_param, the list of parameters in the optimisation route (Optional)
    - hist_score, the scores of the parameters in hist_param (Optional)
    - full_evals, the full evaluations of x_i, S(x_i) generated during optimisation (Optional)
    - hyperparams, the hyperparameters used for the optimisation procedure (Optional)

    Note on saving
    Hyperparams are saved using dill, as non standard python hyperparameters could be provided.
    """

    class_name = "OptimResult"
    # For future
    __load_info = io.LoadInfo(
        [
            io.ClassAttrIO("class_name", "class_name.txt", "STR"),
            io.ClassAttrIO("opti_param", "opti_param.json", "ARRAY"),
            io.ClassAttrIO("converged", "converged.txt", "BOOL"),
            io.ClassAttrIO("opti_score", "opti_score.txt", "FLOAT", mandatory=False),
            io.ClassAttrIO("hist_param", "hist_param.json", "ARRAY", mandatory=False),
            io.ClassAttrIO("hist_score", "hist_score.json", "ARRAY", mandatory=False),
            io.ClassAttrIO("hyperparams", "hyperparams.dl", "DILL", mandatory=False),
        ]
    )

    def __init__(
        self,
        opti_param,
        converged: bool,
        opti_score: Optional[float] = None,
        hist_param: Optional[Sequence] = None,
        hist_score: Optional[Sequence[float]] = None,
        hyperparams: Optional[dict] = None,
    ):
        """Initialize class from attributes values"""
        self._opti_param = opti_param
        self._converged = converged
        self._opti_score = opti_score
        self._hist_param = hist_param
        self._hist_score = hist_score
        self._hyperparams = hyperparams

    @property
    def opti_param(self):
        """Optimal parameter found during the optimisation process"""
        return self._opti_param

    @property
    def converged(self):
        """Whether the optimisation process converged"""
        return self._converged

    @property
    def opti_score(self) -> float:
        """Optimal score found during the optimisation process"""
        return self._opti_score

    @property
    def hist_param(self):
        """Parameter history throughout the optimisation process"""
        return self._hist_param

    @property
    def hist_score(self):
        """Score history throughout the optimisation process"""
        return self._hist_score

    @property
    def hyperparams(self):
        """Hyper parameters of the optimisation process"""
        return self._hyperparams

    def convert(self, fun: Callable, vectorized: bool = False, parallel: bool = False):
        """
        Convert parameters logged in OptimResult object inplace

        If J o fun was optimized in order to optimize J, then converts the optimisation result for
        the optimisation of J (i.e. parameters are converted)
        """

        self._opti_param = fun(self._opti_param)

        if self._hist_param is not None:
            if vectorized:
                self._hist_param = fun(self._hist_param)
            else:
                self._hist_param = par_eval(fun, self._hist_param, parallel)

    def get_best_param(self):
        """Check history for lowest score found"""
        if (self._hist_param is None) or (self._hist_score is None):
            raise ValueError("Empty hist_param or hist_score attributes")
        return self._hist_param[np.argmin(self._hist_score)]

    def save_future(self, name: str, path: str = ".", overwrite: bool = True) -> str:
        """Save 'OptimResult' object to folder 'name' in 'path'."""

        if not os.path.isdir(path):
            raise ValueError(f"{path} should point to a folder")

        acc_path = os.path.join(path, name)
        os.makedirs(acc_path, exist_ok=overwrite)

        # Save information on how this should be written
        self.__load_info.save(os.path.join(acc_path, "opti_load_info.json"))
        self.__load_info.save_obj(self, path=acc_path, write_methods=io.base_io)

    def save(self, name: str, path: str = ".", overwrite: bool = True) -> str:
        """Save 'OptimResult' object to folder 'name' in 'path'."""
        if not os.path.isdir(path):
            raise ValueError(f"{path} should point to a folder")

        def mk_pth(name: str):
            return os.path.join(acc_path, name)

        acc_path = os.path.join(path, name)
        os.makedirs(acc_path, exist_ok=overwrite)

        io.rw_str.save(mk_pth("opti_type.txt"), self.class_name)
        io.rw_arr.save(mk_pth("opti_param.json"), self._opti_param)
        io.rw_bool.save(mk_pth("converged.txt"), self._converged)

        if self._opti_score is not None:
            io.rw_flt.save(mk_pth("opti_score.txt"), self._opti_score)

        if self._hist_score is not None:
            io.rw_arr.save(mk_pth("hist_score.json"), np.asarray(self._hist_score))

        if self._hist_param is not None:
            io.rw_arr.save(mk_pth("hist_param.json"), np.asarray(self._hist_param))

        if self._hyperparams is not None:
            io.rw_dl.save(mk_pth("hyperparams.dl"), self._hyperparams)

        return acc_path

    def __repr__(self):
        if self._converged:
            conv_status = "Converged"
        else:
            conv_status = "Not converged"
        return "\n".join(
            [
                f"{self.class_name} object",
                f"Status: {conv_status}",
                f"Optimal score: {self._opti_score}",
                f"Optimal parameter: {self._opti_param}",
            ]
        )
