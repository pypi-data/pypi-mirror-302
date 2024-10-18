""" Inherited class of OptimResultVI for gradient based VI algorithm"""

from typing import Optional, Sequence

from picproba.types import ProbaParam
from picoptim.fun_evals import FunEvals
from picpacbayes.hist_vi import HistVILog
from picpacbayes.optim_result_vi import OptimResultVI


class OptimResultVIGB(OptimResultVI):
    """
    Inherited from OptimResultVI

    Added fields:
        - bin_log_vi
    """

    class_name = "OptimResultVIGB"

    def __init__(
        self,
        opti_param: ProbaParam,
        converged: bool,
        opti_score: float,
        hist_param: Sequence[ProbaParam],
        hist_score: Sequence[float],
        end_param: ProbaParam,
        log_vi: HistVILog,
        bin_log_vi: HistVILog,
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
            log_vi=log_vi,
            sample_val=sample_val,
            hyperparams=hyperparams,
        )
        self._bin_log_vi = bin_log_vi

    @property
    def bin_log_vi(self):
        return self._bin_log_vi

    def save(self, name: str, path: str = ".", overwrite: bool = True) -> str:
        """Save 'OptimResultVIGB' object to folder 'name' in 'path'"""

        # Saving 'OptimResultVI' attributes
        acc_path = super().save(name, path, overwrite=overwrite)

        # Saving additional attributes
        (self._bin_log_vi).save(name="bin_log_vi", path=acc_path, overwrite=overwrite)
        return acc_path
