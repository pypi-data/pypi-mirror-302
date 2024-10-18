""" Bayesian inspired algorithm for joint calibration and uncertainty quantification
Main functions:
- pacbayes_minimize, based on Catoni's bound (see https://doi.org/10.48550/arXiv.2110.11216)
"""

from picpacbayes.gradient_based import (
    FunEvalsDens,
    GradientBasedPBayesSolver,
    OptimResultPBayesGB,
)
from picpacbayes.picpacbayes.hist_bayes import HistBayesLog
from picpacbayes.picpacbayes.optim_result_pbayes import OptimResultPBayes
from picpacbayes.score_approx import (
    FunEvalsExp,
    GaussianSABS,
    PreExpSABS,
    ScoreApproxPBayesSolver,
)
from picpacbayes.picpacbayes.pacbayes_minimize import (
    infer_pb_routine,
    pacbayes_minimize,
)
