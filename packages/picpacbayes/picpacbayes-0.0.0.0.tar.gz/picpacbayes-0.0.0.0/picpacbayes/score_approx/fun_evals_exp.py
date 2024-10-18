""" In the case of exponential family, add a T field to accu_sample.

Increase strain on memory but avoids recomputing T values at each iteration.
"""

import os
from typing import Optional, Union

import numpy as np
from numpy.typing import ArrayLike

import apicutils.basic_io as io
from picoptim.types import Params
from picoptim.fun_evals import FunEvals, FUN_EVALS_INDICATOR
from picproba import ExponentialFamily, PreExpFamily


class FunEvalsExp(FunEvals):
    """
    Manages the low level history of a PAC Bayesian optimisation problem.

    Data can be accessed through methods
        sample (all SamplePoints generated),
        vals (the score of each  SamplePoint),
        gen_tracker (when was each  SamplePoint generated)
    which take as input a number of data (optional, if None returns all data)

    sample is a list of points x,
    vals the list of evaluations of the scoring function at x,
    half_ldens the half log densities for x wrt to the distribution from which x was generated,
    gen_tracker the information pointing from which distribution x was generated (latest generation is 0,
        -1 indicates that the sample point is not yet generated)

    Data is stored in np.ndarray of fixed sized defined at initialisation. These should never be
    accessed by the users as they can be misleading (data suppression is lazy, i.e. only a count of
    stored data is changed).

    It is possible to increase memory size through extend_memory method.
    """

    # For saving/loading purpose
    load_type = "FunEvalsExp"
    TS_PATH = "TS"

    def __init__(
        self, param_shape: tuple[int, ...], t_shape: tuple[int, ...], n_tot: int
    ):
        super().__init__(param_shape, n_tot)
        self._ts = np.zeros((n_tot,) + t_shape)
        self.t_shape = t_shape

    def extend_memory(self, n_add: int) -> None:
        n_filled = self.n_filled
        super().extend_memory(n_add)

        ts = np.zeros((self.n_tot,) + self.t_shape)
        ts[:n_filled] = self.ts()
        self._ts = ts

    def add(  # type: ignore# pylint: disable=W0221
        self, params: Params, vals: ArrayLike, ts: ArrayLike
    ) -> None:
        """
        Add a new generation to memory.
        """

        n = self.n_filled
        super().add(params, vals)  # type: ignore
        n_end = self.n_filled
        self._ts[n : n_end] = ts[:(n_end-n)]

    def ts(self, k: Optional[int] = None) -> np.ndarray:
        """Clean look at the sample evaluations"""

        if k is None:
            init = 0
        else:
            init = max(0, self.n_filled - k)

        return self._ts[init : self.n_filled]

    def save(self, name: str, directory: Optional[str]=None, overwrite: bool = False) -> str:
        """
        Save FunEvalsExp object to folder 'name' situated in 'directory' (default to working folder)
        """

        full_path = super().save(name, directory, overwrite)
        io.rw_arr.save(io.combine_to_path(self.TS_PATH, io.rw_arr.ext, full_path), self.ts())
        return full_path

    @classmethod
    def _load(cls, name:str, directory:Optional[str] = None):
        """Actual loading method"""
        # Check that path exists
        full_path = io.combine_to_path(name, "", directory)

        n_tot = io.rw_int.load(io.combine_to_path(cls.N_TOT_PATH, io.rw_int.ext, full_path))
        vals = io.rw_arr.load(io.combine_to_path(cls.VALS_PATH, io.rw_arr.ext, full_path))
        params = io.rw_arr.load(io.combine_to_path(cls.PARAMS_PATH, io.rw_arr.ext, full_path))
        ts = io.rw_arr.load(io.combine_to_path(cls.TS_PATH, io.rw_arr.ext, full_path))
        gen = io.rw_arr.load(io.combine_to_path(cls.GEN_PATH, io.rw_arr.ext, directory=full_path))

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
        if not len(ts) == n:
           raise ValueError(
                f"Number of ts is not equal to number of values passed ({len(ts)}, {n})"
            )
        t_shape = ts.shape[1:]
        params_shape = params.shape[1:]
        data = cls(params_shape, t_shape, n_tot)
        data.add(params, vals, ts)
        data._gen_tracker[:n] = gen

        return data
    
FUN_EVALS_INDICATOR.add(FunEvalsExp)


def _add_T_data(
    accu_sample: FunEvals, proba_map: Union[PreExpFamily, ExponentialFamily]
) -> FunEvalsExp:
    accu_exp = FunEvalsExp(
        param_shape=accu_sample.param_shape,
        t_shape=proba_map.t_shape,
        n_tot=accu_sample.n_tot,
    )
    params = accu_sample.params()
    accu_exp.add(params, vals=accu_sample.vals(), ts=proba_map.T(params))
    accu_exp._gen_tracker = accu_sample._gen_tracker  # pylint:disable=W0212
    return accu_exp
