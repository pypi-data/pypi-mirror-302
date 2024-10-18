"""
FunEvals class.

FunEvals is used to store (x, f(x)) evaluations where f outputs float.
'x' is called a parameter, 'fun(x)' the value.

New evaluations can be added using the add method. Data suppression is performed lazily.

The generation at which each data was added is also stored.
Data can be saved to .csv files using the save method.

Loading FunEvals object is done using the 'load' method of the class. The name of the class is
stored as 'FUN_EVALS_TYPE.txt'. This is meant to be used to distinguish the class from its subclasses.
Finding a way to automate FunEvals subclass loading is still ongoing work.
"""

import os
import warnings
from typing import Callable, Optional, Type

import apicutils.basic_io as io
import numpy as np
from apicutils import check_shape, par_eval

from picoptim.types import Param, Params
from picoptim._helper import ProtectedDict


class NonEmptyAccuLoading(Exception):
    """Exception when trying to load data on an non empty accu"""


class FunEvals:
    """Store evaluations of a function.

    Data can be accessed through methods
        params (all Params generated),
        vals (the evaluations of each Params),
        gen_tracker (when was each Param generated)
    which take as input a number of data (optional, if None returns all data)

    params is a list of points x,
    vals the list of evaluations of the scoring function at x,
    gen_tracker the information pointing from which distribution x was generated (latest generation
    is 0, -1 indicates that the parameter memory is not yet filled)

    Data is stored in np.ndarray of fixed sized defined at initialisation. These should never be
    accessed by the users as they can be misleading (data suppression is lazy, i.e. only a count of
    stored data is changed).

    Memory size can be extended through extend_memory method.
    """

    # For saving/loading purpose
    load_type = "FunEvals"

    # Paths when saving. No extensions (added at save time)
    LOAD_TYPE_PATH = "FUN_EVALS_TYPE"
    VALS_PATH = "VALS"
    PARAMS_PATH = "PARAMS"
    GEN_PATH = "GEN"
    N_TOT_PATH = "N_TOT"

    def __init__(self, param_shape: tuple[int, ...], n_tot: int):
        self.param_shape = param_shape

        self._params = np.zeros((n_tot,) + param_shape)
        self._vals = np.zeros(n_tot)
        self._gen_tracker = np.full(n_tot, -1)

        self._n_gen: int = 0

        self._n_filled: int = 0
        self._n_tot: int = n_tot

    @property
    def n_gen(self) -> int:
        """Number of storing operations"""
        return self._n_gen

    @property
    def n_filled(self) -> int:
        """Number of filled evaluations"""
        return self._n_filled

    @property
    def n_tot(self) -> int:
        """Total number of evaluations prepared in memory"""
        return self._n_tot

    def extend_memory(self, n_add: int) -> None:
        """Add n_add memory slot to the FunEvals object"""
        n_tot = self._n_tot + n_add
        n_filled = self._n_filled

        params = np.zeros((n_tot,) + self.param_shape)
        vals = np.zeros(n_tot)
        gen_tracker = np.full(n_tot, -1)

        params[:n_filled] = self.params()
        vals[:n_filled] = self.vals()
        gen_tracker[:n_filled] = self.gen_tracker()

        self._params = params
        self._vals = vals
        self._gen_tracker = gen_tracker

        self._n_tot = n_tot

    def n_remain(self) -> int:
        """Return number of remaining slots in the memory"""
        return self._n_tot - self._n_filled

    def add(self, params: Params, vals: np.ndarray) -> None:
        """Add a new generation to memory."""
        params = np.asarray(params)
        m = len(params)

        check_shape(params, (m,) + self.param_shape)

        n = self._n_filled

        if (n + m) > self._n_tot:
            warnings.warn("Maximum number of data reached")
            m = self._n_tot - n

        self._params[n : (n + m)] = params[:m]
        self._vals[n : (n + m)] = vals[:m]

        self._gen_tracker[: (n + m)] += 1

        self._n_gen += 1
        self._n_filled = n + m

    def add1(self, param: Param, val: float) -> None:
        """
        Add a new point to memory
        """
        param = np.asarray(param)

        check_shape(param, shape_exp=self.param_shape)

        n = self._n_filled

        if n < self._n_tot:
            self._params[n] = param
            self._vals[n] = val

            self._gen_tracker[: (n + 1)] += 1

            self._n_gen += 1
            self._n_filled = n + 1
        else:
            warnings.warn("Maximum number of data reached")

    def suppr(self, k: int):
        """Deletes the last k entries in the memory (lazy delete)"""
        self._n_filled = max(0, self._n_filled - k)

    def suppr_gen(self, K: int):
        """Deletes the last K generations in the memory (lazy delete)"""
        gen_tracker = self._gen_tracker.copy()
        gen_tracker = np.clip(gen_tracker - K, a_min=-1, a_max=None)

        self._n_gen = max(0, self._n_gen - K)
        self._n_filled = np.sum(gen_tracker >= 0, dtype=int)
        self._gen_tracker = gen_tracker

    def params(self, k: Optional[int] = None):
        """
        Clean look at the parameters

        By default, outputs all parameters logged.
        If 'k' is provided, the last 'k' parameters logged are returned.
        """
        if k is None:
            init = 0
        else:
            init = max(0, self._n_filled - k)

        return self._params[init : self._n_filled]

    def vals(self, k: Optional[int] = None):
        """
        Clean look at the parameter evaluations

        By default, outputs all vals logged.
        If 'k' is provided, the last 'k' vals logged are returned.
        """

        if k is None:
            init = 0
        else:
            init = max(0, self._n_filled - k)

        return self._vals[init : self._n_filled]

    def gen_tracker(self, k: Optional[int] = None):
        """
        Clean look at the parameter generations

        By default, outputs all parameter generations logged.
        If 'k' is provided, the last 'k' parameter generations logged are returned.
        """

        if k is None:
            init = 0
        else:
            init = max(0, self._n_filled - k)

        return self._gen_tracker[init : self._n_filled]

    def __repr__(self):
        return f"{self.load_type} object with {self._n_filled} / {self._n_tot} evaluations filled"

    def convert(
        self, fun: Callable, vectorized: bool = False, parallel: bool = False
    ) -> None:
        """
        Convert inplace the parameters of a FunEvals object.

        Both the '_params' and 'param_shape' attributes are modified.

        Args:
            fun: the conversion function
            vectorized: states if fun is vectorized
            parallel: states if calls to fun should be parallelized
        """

        if self._n_filled == 0:
            raise ValueError("Can not convert empty FunEvals")
        if vectorized:
            converted_params = fun(self.params())
        else:
            converted_params = np.array(par_eval(fun, self.params(), parallel))

        new_shape = converted_params.shape[1:]

        self._params = np.concatenate(
            [converted_params, np.zeros((self._n_tot - self._n_filled,) + new_shape)], 0
        )
        self.param_shape = new_shape

    def save(
        self, name: str, directory: Optional[str] = None, overwrite: bool = False
    ) -> str:
        """
        Save FunEvals object to folder 'name' situated in 'directory' (default to working folder)
        """

        full_path = io.combine_to_path(name, "", directory)
        os.makedirs(full_path, exist_ok=overwrite)

        # Save type information (for easy loading)
        io.rw_str.save(
            io.combine_to_path(self.LOAD_TYPE_PATH, io.rw_str.ext, full_path),
            self.load_type,
        )

        # Save data
        io.rw_int.save(
            io.combine_to_path(self.N_TOT_PATH, io.rw_int.ext, directory=full_path),
            self.n_tot,
        )
        io.rw_arr.save(
            io.combine_to_path(self.VALS_PATH, io.rw_arr.ext, directory=full_path),
            self.vals(),
        )
        io.rw_arr.save(
            io.combine_to_path(self.PARAMS_PATH, io.rw_arr.ext, directory=full_path),
            self.params(),
        )
        io.rw_arr.save(
            io.combine_to_path(self.GEN_PATH, io.rw_arr.ext, directory=full_path),
            self.gen_tracker(),
        )

        return full_path

    @classmethod
    def _load(cls, name: str, directory: Optional[str] = None):
        """Actual loading method"""
        full_path = io.combine_to_path(name, "", directory)

        n_tot = io.rw_int.load(
            io.combine_to_path(cls.N_TOT_PATH, io.rw_int.ext, full_path)
        )
        vals = io.rw_arr.load(
            io.combine_to_path(cls.VALS_PATH, io.rw_arr.ext, full_path)
        )
        params = io.rw_arr.load(
            io.combine_to_path(cls.PARAMS_PATH, io.rw_arr.ext, full_path)
        )
        gen = io.rw_arr.load(
            io.combine_to_path(cls.GEN_PATH, io.rw_arr.ext, directory=full_path)
        )

        n = len(vals)
        if n > n_tot:
            raise ValueError(f"More values than slots! n values:{n}, n_tot: {n_tot}")
        if not len(gen) == n:
            raise ValueError(
                f"Number of generations is not equal to number of values passed ({len(gen)}, {n})"
            )
        if not len(params) == n:
            raise ValueError(
                f"Number of params is not equal to number of values passed ({len(params)}, {n})"
            )
        params_shape = params.shape[1:]
        data = cls(params_shape, n_tot)
        data.add(params, vals)
        data._gen_tracker[:n] = gen

        return data

    @classmethod
    def load(cls, name: str, directory: Optional[str] = None):
        """Load a FunEvals or subclass instance.

        FunEvals.load will automatically detect the proper subclass if this subclass
        is adequately coded, i.e.:
        - it has a specific FunEvals.load_type,
        - the _load method and save method have been adequately overwritten
        - the dictionnary FUN_EVALS_INDICATOR has been updated

        For developpers, that means doing:
        </> file where subclass is defined </>

        from picoptim import FunEvals, FUN_EVALS_INDICATOR

        class MyFunEvals(FunEvals):
            load_type = "MyFunEvals"

            def _load(self, name:str, directory:Optionale[str] = None) -> None:
                ...

            def save(self, name:str, directory:Optionale[str] = None, overwrite: bool = False) -> str:
                ...

        FUN_EVALS_INDICATOR.add(MyFunEvals) # This is a shortcut to:
        # FUN_EVALS_INDICATOR[MyFunEvals.load_type] = MyFunEvals

        </> End of file </>

        Now in a console:

        >> accu = MyFunEvals(...) # Create a MyFunEvals
        >> accu.add(...) # Add some data
        >> accu.save('my_fun_eval') # Save it to the disk

        >> same_accu = FunEvals.load('my_fun_eval')
        >> assert isinstance(same_accu, MyFunEvals)
        True

        """
        full_path = io.combine_to_path(name, "", directory)
        load_type = io.rw_str.load(
            io.combine_to_path(cls.LOAD_TYPE_PATH, io.rw_str.ext, full_path)
        )
        return FUN_EVALS_INDICATOR[load_type]._load(name, directory)

    def downgrade(self):
        """Downgrade a subclass of FunEvals back to FunEvals"""
        accu = FunEvals(self.param_shape, self._n_tot)
        accu.add(self.params(), self.vals())
        accu._gen_tracker = self._gen_tracker

        return accu


class FunEvalsIndicator(ProtectedDict):
    def add(self, fun_eval_class: Type[FunEvals]):
        self.__setitem__(fun_eval_class.load_type, fun_eval_class)


FUN_EVALS_INDICATOR = FunEvalsIndicator()
FUN_EVALS_INDICATOR.add(FunEvals)
