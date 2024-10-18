import numpy as np

from picproba.types import Samples
from picpacbayes.score_approx.pre_exp_solver import PreExpSABS
from picpacbayes.score_approx.weighing import get_weights_mc_gauss

# from multiprocess import Pool  # pylint: disable=E0611
from apicutils import blab
from picproba import Proba


class GaussianSABS(PreExpSABS):
    """Bayesian Solver using Score approximation routine for Gaussian Family Maps

    Differs from routine for standard PreExpFamily by the weighing technique (covariance matrix
    of the proba used.)
    """

    def weigh(self, proba: Proba, samples: Samples, n_sample_estim: int) -> np.ndarray:
        return get_weights_mc_gauss(
            proba, samples, n_sample_estim, k_neighbors=self.k_neighbors
        )

    def msg_begin_calib(self) -> None:
        blab(
            self.silent,
            " ".join(
                [
                    "Starting Bayesian calibration",
                    "(Score Approximation routine,",
                    "Gaussian variant)",
                ]
            ),
        )
