r"""
Optimise Catoni's bound through an approximated gradient descent procedure.

Contrary to the algorithm in the 'score_approx' module, the routines implemented here can be used
to optimise Catoni's bound for any 'ProbaMap.'

Warning:
- The algorithm seems to have stability issues, which prevent it from converging to the correct
distribution when the temperature is small (i.e. high learning rate).
"""

from picpacbayes.gradient_based.fun_evals_dens import FunEvalsDens
from picpacbayes.gradient_based.gradient_based_solver import (
    GradientBasedBayesSolver,
)
from picpacbayes.gradient_based.optim_result_vi_gb import OptimResultVIGB
