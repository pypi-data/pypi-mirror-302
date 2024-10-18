"""Function form for PAC-Bayes minimisation, with solver inference"""

from typing import Callable, Optional, Type, Union

import numpy as np

from picpacbayes.pac_bayes_solver import PACBayesSolver
from picpacbayes.gradient_based import (
    GradientBasedPBayesSolver,
    # KNNBayesSolver,
)
from picpacbayes.optim_result_pbayes import OptimResultPBayes
from picpacbayes.score_approx import (
    GaussianSABS,
    PreExpSABS,
    ScoreApproxPBayesSolver,
)
from picproba import ProbaMap

set_pac_bayes_solver = {
    "corr_weights",
    # "knn",
    "SuPAC-CE",
    "score_approx",
    "score_approx_gauss",
    "score_approx_pre_exp",
    "score_approx_exp",
}


def infer_pb_routine(
    proba_map: ProbaMap, pac_bayes_solver: Optional[Union[str, Type[PACBayesSolver]]] = None
) -> Type[PACBayesSolver]:
    """Infer which pac_bayes_solver from 'proba_map' and 'pac_bayes_solver' arguments.

    Check Coherence between 'pac_bayes_solver' and 'proba_map'.

    Rules:
        If None, defaults to 'corr_weights' for generic distribution and the adequate
        'score_approx' routines for ExponentialFamily, PreExpFamily, and Gaussian related
        distributions.
        If 'score_approx', checks the appropriate version of 'score_approx' depending on the
        'proba_map' passed.
    """
    if (pac_bayes_solver is None) or (pac_bayes_solver == "score_approx") or (pac_bayes_solver == "SuPAC-CE"):
        if proba_map.map_type == "Gaussian":
            return GaussianSABS
        if proba_map.map_type == "PreExpFamily":
            return PreExpSABS
        if proba_map.map_type == "ExponentialFamily":
            return ScoreApproxPBayesSolver
        if pac_bayes_solver is None:
            return GradientBasedPBayesSolver

        raise ValueError(
            "'score_approx' can only be used for Gaussian, Block diagonal Gaussian or Exponential Families"
        )
    elif isinstance(pac_bayes_solver, str):
        if pac_bayes_solver == "score_approx_gauss":
            if proba_map.map_type != "Gaussian":
                raise ValueError(
                    "'score_approx_gauss' can only be used for 'GaussianMap', 'BlockDiagGaussMap', 'FactCovGaussianMap', 'FixedCovGaussianMap' or 'TensorizedGaussianMap'"
                )
            return GaussianSABS

        elif pac_bayes_solver == "score_approx_pre_exp":
            if proba_map.map_type != "PreExpFamily":
                raise ValueError(
                    "score_approx_pre_exp can only be used for PreExpFamily"
                )
            return PreExpSABS

        elif pac_bayes_solver == "score_approx_exp":
            if proba_map.map_type != "ExponentialFamily":
                raise ValueError(
                    "score_approx_exp can only be used for ExponentialFamily"
                )
            return ScoreApproxPBayesSolver

        elif pac_bayes_solver == "corr_weights":
            return GradientBasedPBayesSolver
        # Deactivated KNN for now
        # elif pac_bayes_solver == "knn":
        #     return KNNBayesSolver

        else:
            raise ValueError(
                f"'pac_bayes_solver' must be one of {set_pac_bayes_solver} (value {pac_bayes_solver})"
            )

    else:
        return pac_bayes_solver


def pacbayes_minimize(
    fun: Callable[[np.ndarray], float],
    proba_map: ProbaMap,
    temperature: float,
    optimizer: Optional[Union[str, type[PACBayesSolver]]] = None,
    parallel: bool = True,
    vectorized: bool = False,
    **kwargs,
) -> OptimResultPBayes:

    Optim = infer_pb_routine(proba_map=proba_map, pac_bayes_solver=optimizer)

    optim = Optim(
        fun=fun,
        proba_map=proba_map,
        temperature=temperature,
        parallel=parallel,
        vectorized=vectorized,
        **kwargs,
    )
    optim.optimize()

    return optim.process_result()
