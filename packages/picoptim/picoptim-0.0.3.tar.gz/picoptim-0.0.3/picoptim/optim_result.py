"""
Optimisation result classes
"""

import os
from typing import Callable, Optional, Sequence, Type

import apicutils.basic_io as io
import numpy as np
from apicutils import par_eval
from picoptim._helper import ProtectedDict


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

    CONVERGED_PATH = "CONVERGED"
    HYPERPARAMS_PATH = "HYPERPARAMS"
    HIST_PARAM_PATH = "HIST_PARAM"
    HIST_SCORE_PATH = "HIST_SCORE"
    OPTI_SCORE_PATH = "OPTI_SCORE"
    OPTI_PARAM_PATH = "OPTI_PARAM"
    CLASS_NAME_PATH = "OPTIM_RESULT_TYPE"

    # For future
    _load_info = io.LoadInfo(
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
        """Save 'OptimResult' object to folder 'name' in 'path'.
        WORK IN PROGRESS, DO NOT USE!
        """

        if not os.path.isdir(path):
            raise ValueError(f"{path} should point to a folder")

        acc_path = os.path.join(path, name)
        os.makedirs(acc_path, exist_ok=overwrite)

        # Save information on how this should be written
        self._load_info.save(os.path.join(acc_path, "opti_load_info.json"))
        self._load_info.save_obj(self, path=acc_path, write_methods=io.base_io)

    def save(self, name: str, path: str = ".", overwrite: bool = True) -> str:
        """Save 'OptimResult' object to folder 'name' in 'path'."""
        if not os.path.isdir(path):
            raise ValueError(f"{path} should point to a folder")

        def mk_pth(name: str):
            return os.path.join(acc_path, name)

        acc_path = io.combine_to_path(name, "", path)
        os.makedirs(acc_path, exist_ok=overwrite)

        io.rw_str.save(
            io.combine_to_path(self.CLASS_NAME_PATH, io.rw_str.ext, acc_path),
            self.class_name,
        )
        io.rw_arr.save(
            io.combine_to_path(self.OPTI_PARAM_PATH, io.rw_arr.ext, acc_path),
            self._opti_param,
        )
        io.rw_bool.save(
            io.combine_to_path(self.CONVERGED_PATH, io.rw_bool.ext, acc_path),
            self._converged,
        )

        if self._opti_score is not None:
            io.rw_flt.save(
                io.combine_to_path(self.OPTI_SCORE_PATH, io.rw_flt.ext, acc_path),
                self._opti_score,
            )

        if self._hist_score is not None:
            io.rw_arr.save(
                io.combine_to_path(self.HIST_SCORE_PATH, io.rw_arr.ext, acc_path),
                self._hist_score,
            )

        if self._hist_param is not None:
            io.rw_arr.save(
                io.combine_to_path(self.HIST_PARAM_PATH, io.rw_arr.ext, acc_path),
                np.asarray(self._hist_param),
            )

        if self._hyperparams is not None:
            io.rw_dl.save(
                io.combine_to_path(self.HYPERPARAMS_PATH, io.rw_dl.ext, acc_path),
                self._hyperparams,
            )

        return acc_path

    @classmethod
    def _load(cls, name: str, directory: Optional[str] = None):
        # Load basic attributes shared among all subclass
        acc_path = io.combine_to_path(name, "", directory)
        converged = io.rw_bool.load(
            io.combine_to_path(cls.CONVERGED_PATH, io.rw_bool.ext, acc_path)
        )
        opti_param = io.rw_arr.load(
            io.combine_to_path(cls.OPTI_PARAM_PATH, io.rw_arr.ext, acc_path)
        )
        opti_score = io.rw_flt.load(
            io.combine_to_path(cls.OPTI_SCORE_PATH, io.rw_flt.ext, acc_path),
            optional=True,
        )
        hist_score = io.rw_arr.load(
            io.combine_to_path(cls.HIST_SCORE_PATH, io.rw_arr.ext, acc_path),
            optional=True,
        )
        hist_param = io.rw_arr.load(
            io.combine_to_path(cls.HIST_PARAM_PATH, io.rw_arr.ext, acc_path),
            optional=True,
        )
        hyperparams = io.rw_dl.load(
            io.combine_to_path(cls.HYPERPARAMS_PATH, io.rw_dl.ext, acc_path),
            optional=True,
        )

        return cls(
            opti_param=opti_param,
            converged=converged,
            opti_score=opti_score,
            hist_param=hist_param,
            hist_score=hist_score,
            hyperparams=hyperparams,
        )

    @classmethod
    def load(
        cls,
        name: str,
        directory: Optional[str] = None,
    ):
        full_path = io.combine_to_path(name, "", directory)
        load_type = io.rw_str.load(
            io.combine_to_path(cls.class_name, io.rw_str.ext, full_path)
        )
        return OPTIM_RESULT_INDICATOR[load_type]._load(name, directory)

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


class OptimResultIndicator(ProtectedDict):
    def add(self, optim_res_class: Type[OptimResult]):
        self.__setitem__(optim_res_class.class_name, optim_res_class)


OPTIM_RESULT_INDICATOR = OptimResultIndicator()
OPTIM_RESULT_INDICATOR.add(OptimResult)
