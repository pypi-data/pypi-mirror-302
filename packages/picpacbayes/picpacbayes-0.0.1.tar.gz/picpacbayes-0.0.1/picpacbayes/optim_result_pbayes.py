import os
from typing import Optional, Sequence

import numpy as np

import apicutils.basic_io as io
from picproba.types import ProbaParam
from picoptim.fun_evals import FunEvals
from picpacbayes.picpacbayes.hist_bayes import HistBayesLog
from picoptim.optim_result import OptimResult, OPTIM_RESULT_INDICATOR


class OptimResultPBayes(OptimResult):
    """
    Inherited from OptimResult.

    Added fields:
        - end_param
        - log_pbayes
        - sample_val
    """

    class_name = "OptimResultPBayes"

    def __init__(
        self,
        opti_param: ProbaParam,
        converged: bool,
        opti_score: float,
        hist_param: Sequence[ProbaParam],
        hist_score: Sequence[float],
        end_param: ProbaParam,
        log_pbayes: HistBayesLog,
        sample_val: FunEvals,
        hyperparams: Optional[dict] = None,
    ):
        super().__init__(
            opti_param=opti_param,
            converged=converged,
            opti_score=opti_score,
            hist_param=hist_param,
            hist_score=hist_score,
            hyperparams=hyperparams,
        )
        self._end_param = end_param
        self._log_pbayes = log_pbayes
        self._sample_val = sample_val

    @property
    def end_param(self):
        return self._end_param

    @property
    def log_pbayes(self):
        return self._log_pbayes

    @property
    def sample_val(self):
        return self._sample_val

    END_PARAM_PATH = "END_PARAM"
    SAMPLE_VAL_PATH ="SAMPLE_VAL"
    log_pbayes_PATH = "log_pbayes"

    def save(self, name: str, path: str = ".", overwrite: bool = True) -> str:
        # Saving 'OptimResult' attributes
        acc_path = super().save(name, path, overwrite=overwrite)

        # Saving additional attributes
        io.rw_arr.save(io.combine_to_path(self.END_PARAM_PATH, io.rw_arr.ext, acc_path), np.asarray(self._end_param))

        (self._sample_val).save(
            self.SAMPLE_VAL_PATH, acc_path, overwrite=overwrite
        )  # mypy: ignore-errors
        (self._log_pbayes).save(self.log_pbayes_PATH, acc_path, overwrite=overwrite)
        return acc_path

    @classmethod
    def _load(cls, name:str, directory:Optional[str]=None):
        # Load basic attributes shared among all subclass
        acc_path = io.combine_to_path(name, "", directory)
        converged = io.rw_bool.load(io.combine_to_path(cls.CONVERGED_PATH, io.rw_bool.ext, acc_path))
        opti_param = io.rw_arr.load(io.combine_to_path(cls.OPTI_PARAM_PATH, io.rw_arr.ext, acc_path))
        opti_score = io.rw_flt.load(io.combine_to_path(cls.OPTI_SCORE_PATH, io.rw_flt.ext, acc_path), optional=True)
        hist_score = io.rw_arr.load(io.combine_to_path(cls.HIST_SCORE_PATH, io.rw_arr.ext, acc_path), optional=True)
        hist_param = io.rw_arr.load(io.combine_to_path(cls.HIST_PARAM_PATH, io.rw_arr.ext, acc_path), optional=True)
        hyperparams = io.rw_dl.load(io.combine_to_path(cls.HYPERPARAMS_PATH, io.rw_dl.ext, acc_path), optional=True)

        sample_val = FunEvals.load(cls.SAMPLE_VAL_PATH, acc_path)
        log_pbayes = HistBayesLog.load(cls.log_pbayes_PATH, acc_path)
        end_param = io.rw_arr.load(io.combine_to_path(cls.END_PARAM_PATH, io.rw_arr.ext, acc_path))

        return cls(
            opti_param=opti_param,
            converged=converged,
            opti_score=opti_score,
            hist_param=hist_param,
            hist_score=hist_score,
            end_param=end_param,
            log_pbayes=log_pbayes,
            sample_val=sample_val,
            hyperparams=hyperparams
        )

OPTIM_RESULT_INDICATOR.add(OptimResultPBayes)