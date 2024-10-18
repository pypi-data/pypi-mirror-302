""" Bayesian inspired algorithm for joint calibration and uncertainty quantification
Main functions:
- iter_prior, inspired by A. Leurent and R. Moscoviz (https://doi.org/10.1002/bit.28156)
- iter_prior_vi, adaptation of iter_prior to the context of Variational inference for gaussians
- variational_inference, based on Catoni's bound (see https://doi.org/10.48550/arXiv.2110.11216)
"""

from picpacbayes.gradient_based import (
    FunEvalsDens,
    GradientBasedBayesSolver,
    OptimResultVIGB,
)
from picpacbayes.hist_vi import HistVILog, load_hist_vi
from picpacbayes.iter_prior import (
    OptimResultPriorIter,
    iter_prior,
    iter_prior_vi,
)
from picpacbayes.optim_result_vi import OptimResultVI
from picpacbayes.score_approx import (
    FunEvalsExp,
    GaussianSABS,
    PreExpSABS,
    ScoreApproxBayesSolver,
)
from picpacbayes.variational_inference import (
    infer_VI_routine,
    variational_inference,
)
