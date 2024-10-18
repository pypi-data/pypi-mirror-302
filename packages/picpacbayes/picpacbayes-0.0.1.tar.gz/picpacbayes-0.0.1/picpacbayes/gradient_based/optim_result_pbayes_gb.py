""" Inherited class of OptimResultPBayes for gradient based VI algorithm"""

from typing import Optional, Sequence

import apicutils.basic_io as io
from picproba.types import ProbaParam
from picoptim.fun_evals import FunEvals
from picpacbayes.picpacbayes.hist_bayes import HistBayesLog
from picoptim.optim_result import OPTIM_RESULT_INDICATOR
from picpacbayes.picpacbayes.optim_result_pbayes import OptimResultPBayes


class OptimResultPBayesGB(OptimResultPBayes):
    """
    Inherited from OptimResultPBayes

    Added fields:
        - bin_log_pbayes
    """

    class_name = "OptimResultPBayesGB"

    def __init__(
        self,
        opti_param: ProbaParam,
        converged: bool,
        opti_score: float,
        hist_param: Sequence[ProbaParam],
        hist_score: Sequence[float],
        end_param: ProbaParam,
        log_pbayes: HistBayesLog,
        bin_log_pbayes: HistBayesLog,
        sample_val: FunEvals,
        hyperparams: Optional[dict] = None,
    ):
        super().__init__(
            opti_param=opti_param,
            converged=converged,
            opti_score=opti_score,
            hist_param=hist_param,
            hist_score=hist_score,
            end_param=end_param,
            log_pbayes=log_pbayes,
            sample_val=sample_val,
            hyperparams=hyperparams,
        )
        self._bin_log_pbayes = bin_log_pbayes

    @property
    def bin_log_pbayes(self):
        return self._bin_log_pbayes

    BIN_LOG_PBAYES_PATH = "BIN_LOG_PBAYES"

    def save(self, name: str, path: str = ".", overwrite: bool = True) -> str:
        """Save 'OptimResultPBayesGB' object to folder 'name' in 'path'"""

        # Saving 'OptimResultPBayes' attributes
        acc_path = super().save(name, path, overwrite=overwrite)

        # Saving additional attributes
        (self._bin_log_pbayes).save(self.BIN_LOG_PBAYES_PATH, acc_path, overwrite=overwrite)
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
        bin_log_pbayes = HistBayesLog.load(cls.BIN_LOG_PBAYES_PATH, acc_path)
        end_param = io.rw_arr.load(io.combine_to_path(cls.END_PARAM_PATH, io.rw_arr.ext, acc_path))

        return cls(
            opti_param=opti_param,
            converged=converged,
            opti_score=opti_score,
            hist_param=hist_param,
            hist_score=hist_score,
            end_param=end_param,
            log_pbayes=log_pbayes,
            bin_log_pbayes=bin_log_pbayes,
            sample_val=sample_val,
            hyperparams=hyperparams
        )    

OPTIM_RESULT_INDICATOR.add(OptimResultPBayesGB)