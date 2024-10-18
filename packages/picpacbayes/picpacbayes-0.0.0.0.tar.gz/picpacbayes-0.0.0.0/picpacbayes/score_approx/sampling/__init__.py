"""
Submodule generating new points to improve score approximation.

Two routines are considered:
- Draw i.i.d. samples from distribution
- Partial Stein Variational Gradient Descent

The SVGD approach could be bring a boost to situations where:
- The dimension is small
- The score function is costly (SVGD computation time is negligible).

FUTURE:
These approach could be superseded by using Gaussian Processes approximation of the score such as
are used in Bayesian Optimization. In this case, points selected should be those with highest
impact on the output (in the sense of uncertainty * sensitivity).

NOTE:
These functions are not used as is! Discuss whether we should or not keep this module.
"""

from picpacbayes.score_approx.sampling.iid_random import enrich_sample_iid
from picpacbayes.score_approx.sampling.partial_stein import (
    enrich_sample_svgd,
    enrich_sample_svgd_gauss,
)
