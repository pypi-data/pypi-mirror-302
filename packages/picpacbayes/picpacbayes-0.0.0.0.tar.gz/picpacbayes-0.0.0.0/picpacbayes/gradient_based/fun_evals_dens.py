""" 
FunEvalsDens class

Inherited from FunEvals, with added half_ldens information (log density with respect to the distribution it was generated)
"""

import os
import warnings
from typing import Optional, Union

import numpy as np

import apicutils.basic_io as io
from picproba.types import Samples
from picoptim.fun_evals import FunEvals, FUN_EVALS_INDICATOR
from apicutils import ShapeError, check_shape
from picproba import Proba, ProbaMap


# Evaluate log_dens on a list of parameters
def _half_log_dens(sample: Samples, proba: Proba):
    r"""
    Evaluate the log density of a probability distribution at each point in a sample

    Args:
        sample, Samples
        proba, the probability distribution whose log_dens is evaluated

    Meant to be used as weight correction, the full correction being:
        $\exp( _half_log_dens(sample, proba_1) - _half_log_dens(sample, proba_0))$
    if the sample is generated through proba_0, hence the name.
    """
    return np.array(proba._log_dens(sample))


class FunEvalsDens(FunEvals):
    """
    Manages the low level history of a PAC Bayesian optimisation problem
    Inherited from FunEvals class (added half_ldens information)

    Data can be accessed through methods
        params,
        half_ldens,
        vals,
        gen_tracker
    which take as input a number of data (optional, if None returns all data)

    params is a list of points x,
    vals the list of evaluations of the scoring function at x,
    half_ldens the half log densities for x wrt to the distribution from which x was generated,
    gen_tracker the information pointing from which distribution x was generated (latest generation
        is 0, -1 indicates that the parameter memory is not yet allocated)

    Data is stored in np.ndarray of fixed sized defined at initialisation. These should never be
    accessed by the users as they can be misleading (data suppression is lazy, i.e. only a count of
    stored data is changed).

    Main method is grad_score, used for the PAC Bayesian optimisation problem with corrected
    weights.

    Note:
        Half log density information is used to efficiently recompute the density ratio with an
        unknown distribution.
    """

    # For saving/loading purpose
    load_type = "FunEvalsDens"
    HALF_LDENS_PATH = "HALF_LDENS"

    def __init__(self, param_shape: tuple[int, ...], n_tot: int):
        super().__init__(param_shape, n_tot)

        self._half_ldens = np.zeros(n_tot)

    def add(self, params, half_ldens, vals) -> None:  # type: ignore # pylint: disable=W0221
        # Format input
        n = self.n_filled
        super().add(params, vals)
        n_end = n
        self._half_ldens[n:n_end] = half_ldens[:(n_end -n)]

    def extend_memory(self, n_add: int) -> None:
        """Add n_add slots to the memory"""
        FunEvals.extend_memory(self, n_add)
        half_ldens = np.zeros(self.n_tot)
        half_ldens[: self.n_filled] = self.half_ldens()
        self._half_ldens = half_ldens

    def half_ldens(self, k: Optional[int] = None) -> np.ndarray:
        """
        Clean look at the half log densities

        By default, outputs all half log densities logged.
        If 'k' is provided, the last 'k' half log densities logged are returned.
        """
        if k is None:
            init = 0
        else:
            init = max(0, self.n_filled - k)

        return self._half_ldens[init : self.n_filled]

    def corr_weights(
        self,
        proba: Proba,
        k: Optional[int] = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        r"""
        Selects the k last parameters and return them along with the evaluations and the correct
        weight corrections.

        The resulting samples and weights can be used to estimate integrals through
            $$\mathbb{E}_{proba}[f(x)] \simeq 1/N \sum \omega_i f(x_i)$$
        This is integral estimation is unbiased (variance analysis is not straightforward). The sub
        sums for each generation are also unbiased (but they are correlated with one another).
        """
        if k is None:
            k = self.n_filled

        return (
            self.params(k),
            self.vals(k),
            _half_log_dens(self.params(k), proba) - self.half_ldens(k),
        )

    def grad_score(
        self,
        d_map: ProbaMap,
        param: np.ndarray,
        gen_weights: Optional[Union[list, dict]] = None,
        gen_decay: float = 0.0,
        k: Optional[int] = None,
    ) -> tuple[np.ndarray, float, float]:
        r"""
        Outputs the derivative and evaluation at param of

        $$J(param) = \sum_{g>0} J_g(param) \exp(- g * gen_decay) / \sum_{g>0} \exp(-g * gen_decay)$$

        where J_g uses the sample S_g from generation g generated from param_g to estimate the mean
        through
            $J_g(param) =
        \sum_{x \in S_g} score(x) * \exp(log_dens(x, param) - log_dens(x, param_g)) / \lvert S_g \rvert

        The intuition being that if the distributions generating all parameters are similar, then
        it is beneficial to use the previous evaluations of the score function in order to minimize
        the variance of the derivative estimate.

        Note:
            if log_dens(x, param) - log_dens(x, param_g) is too high (
            i.e. the point x generated through distribution param_g is deemed much more likely to have been generated from
            param than param_g
            ), then problematic behaviour might happen, the impact of this single point becoming disproportionate.

        Args:
            d_map, the distribution map used in the PAC Bayesian optimisation problem
            param, the parameter at which the derivative is to be computed
            gen_weights, an optional list of weights specifying how each generation should be weighted (first element = latest generation)
            gen_decay, used if gen_weights is None.
                Controls speed of exponentially decaying given to generation k through
                    w_k = exp(-gen_decay * k).
                Default is 0 (no decay, all generation with same weight).
            k, controls maximum number of sample used. None amounts to all sample used.
        """
        # Construct current distribution
        proba = d_map(param)
        # Prepare log_dens_der function
        der_log = d_map._log_dens_der(param)

        # Obtain proper weight corrections for samples from previous generations
        sample, vals, log_dens = self.corr_weights(proba, k=k)

        # Set up weight given to a generation
        n_gen = self.n_gen
        if gen_weights is None:
            gen_weights = [np.exp(-gen_decay * i) for i in range(n_gen)]

        # Tackle case where gen_weights information passed is insufficient
        if len(gen_weights) < n_gen:
            warnings.warn(
                f"Missing information in gen_weights. Giving weight 0 to all generations further than {len(gen_weights)}"
            )
            gen_weights = list(gen_weights) + [
                0 for i in range(n_gen - len(gen_weights))
            ]

        # Prepare specific weight given to each sample
        gen_tracker = self.gen_tracker(k)
        count_per_gen = [np.sum(gen_tracker == i) for i in range(n_gen)]

        gen_factor = np.array(
            [gen_weights[gen] / count_per_gen[gen] for gen in gen_tracker]
        )
        gen_factor = gen_factor / np.sum(gen_factor)

        weights = np.exp(log_dens) * gen_factor
        weights = weights / np.sum(weights)

        # Compute mean value
        mean_val = np.sum(vals * weights)
        # Compute uncertainty using last generation only
        UQ_val0 = np.std(vals[gen_tracker == 0]) / np.sqrt(np.sum(gen_tracker == 0) - 2)

        # Compute estimation of mean score gradient
        grads = der_log(sample)
        grad = np.tensordot((vals - mean_val) * weights, grads, (0, 0))

        return grad, mean_val, UQ_val0

    def save(self, name: str, directory: Optional[str] = None, overwrite: bool = False) -> str:
        """
        Save FunEvalsDens object to folder 'name' situated in 'directory' (default to working folder)
        """

        full_path = super().save(name, directory, overwrite)
        io.rw_arr.save(io.combine_to_path(self.HALF_LDENS_PATH, io.rw_arr.ext, full_path), self.half_ldens())
        return full_path

    @classmethod
    def _load(cls, name:str, directory:Optional[str] = None):
        """Actual loading method for FunEvalsDens"""
        full_path = io.combine_to_path(name, "", directory)

        n_tot = io.rw_int.load(io.combine_to_path(cls.N_TOT_PATH, io.rw_int.ext, full_path))
        vals = io.rw_arr.load(io.combine_to_path(cls.VALS_PATH, io.rw_arr.ext, full_path))
        params = io.rw_arr.load(io.combine_to_path(cls.PARAMS_PATH, io.rw_arr.ext, full_path))
        half_ldens = io.rw_arr.load(io.combine_to_path(cls.HALF_LDENS_PATH, io.rw_arr.ext, full_path))
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
        if not len(half_ldens) == n:
           raise ValueError(
                f"Number of ts is not equal to number of values passed ({len(half_ldens)}, {n})"
            )
        params_shape = params.shape[1:]
        data = cls(params_shape, n_tot)
        data.add(params, half_ldens, vals)
        data._gen_tracker[:n] = gen

        return data
    
# ADd FunEvalsDens to list of loadable FunEvals
FUN_EVALS_INDICATOR.add(FunEvalsDens)