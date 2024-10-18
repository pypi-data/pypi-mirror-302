"""
HistLogVI class

Macro information on the evolution of a VarBUQ task
"""

import os
from typing import Optional, Sequence

import dill
import numpy as np

import apicutils.basic_io as io
from picproba.types import ProbaParam, ProbaParams
from apicutils import ShapeError, check_shape
from picproba import ProbaMap


class FullMemory(Exception):
    """Custom Error raised when trying to store memory to an already full memory manager"""


class HistVILog:
    r"""
    Manages the high level history of a PAC Bayesian optimisation problem of form

    $$S_{VI}(\theta) = E_{p(\theta)}[score] + C kl(p(\theta), p0).$$
    where $E_{p(\theta)}[score]$ is the expected value (or mean) of the score of the probability
    distribution $p(\theta)$.

    Stored data can be accessed through methods:
        proba_pars ($\theta$),
        VI_scores ($S_{VI}(\theta)$),
        KLs ($kl(p(\theta), p0)$),
        means ($E_{p(\theta)}[score]$)
    which take as input a number of data (optional, if None returns all data)

    Data is stored in np.ndarray of fixed sized defined at initialisation. These should never be
    accessed by the users as they can be misleading (data suppression is lazy, i.e. only a count
    of stored data is changed)

    The class is initialised by:
        A ProbaMap object (the function p mapping $\theta$ to a distribution)
        The maximal number of elements stored.
    """

    def __init__(self, proba_map: ProbaMap, n: int):
        self.proba_map = proba_map

        # Prepare memory
        self._proba_pars = np.zeros((n,) + proba_map.proba_param_shape)
        self._VI_scores = np.zeros(n)
        self._KLs = np.zeros(n)
        self._means = np.zeros(n)

        # Specify memory size and amount filled
        self._n_filled = 0
        self._n = n

    @property
    def n_filled(self):
        return self._n_filled

    @property
    def n(self):
        return self._n

    def is_empty(self) -> bool:
        """Checks if the history is empty"""
        return self._n_filled == 0

    @property
    def full(self) -> bool:
        """True if history is full"""
        return self._n == self._n_filled

    def add(
        self,
        proba_pars: ProbaParams,
        scores: Sequence[float],
        KLs: Sequence[float],
        means: Sequence[float],
    ) -> None:
        """
        Store multiple new information in the history
        """
        n = len(proba_pars)

        if not ((n == len(scores)) and (n == len(KLs)) and (n == len(means))):
            raise ShapeError(
                f"proba_pars, scores, KLS and means should have same length ({n}, {len(scores)}, {len(KLs)}, {len(means)})"
            )

        proba_pars = np.asarray(proba_pars)
        check_shape(proba_pars, (n,) + self.proba_map.proba_param_shape)

        n0 = self._n_filled

        if self.full:
            raise FullMemory("Already full")
        if n + n0 > self._n:
            raise Warning(
                f"Too much data is passed. Only storing first {self._n - n0}."
            )

        n = min(n, self._n - n0)

        self._proba_pars[n0 : (n0 + n)] = proba_pars
        self._VI_scores[n0 : (n0 + n)] = scores
        self._KLs[n0 : (n0 + n)] = KLs
        self._means[n0 : (n0 + n)] = means

        self._n_filled = self._n_filled + n

    def add1(self, proba_par: ProbaParam, score: float, KL: float, mean: float) -> None:
        """
        Store new information in the history. Similar to add, but does not expect list like elements.
        """
        if self.full:
            raise FullMemory("Already full")
        try:
            n = self._n_filled
            self._proba_pars[n] = proba_par
            self._VI_scores[n] = score
            self._KLs[n] = KL
            self._means[n] = mean

            self._n_filled += 1

        except Exception as exc:
            print(f"proba_par :{proba_par}\n score: {score}\n KL: {KL}\n mean: {mean}")
            raise exc

    def get(self, k: int = 1) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Outputs the description of the last k elements added to the memory
        """
        return self.proba_pars(k), self.VI_scores(k), self.KLs(k), self.means(k)

    def get_all(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return self.get(self._n_filled)

    def suppr(
        self, k: int = 1
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        To all purposes, deletes the k last inputs and returns the deleted inputs.
        """
        self._n_filled = max(0, self._n_filled - k)
        return self.proba_pars(k), self.VI_scores(k), self.KLs(k), self.means(k)

    def proba_pars(self, k: Optional[int] = None) -> np.ndarray:
        """
        Outputs the last k distribution parameters.
        Last element is last distribution parameter
        """

        if k is None:
            init = 0
        else:
            init = max(0, self._n_filled - k)

        return self._proba_pars[init : self._n_filled]

    def VI_scores(self, k: Optional[int] = None) -> np.ndarray:
        """
        Outputs the last VI scores (last element is last score)
        """

        if k is None:
            init = 0
        else:
            init = max(0, self._n_filled - k)

        return self._VI_scores[init : self._n_filled]

    def KLs(self, k: Optional[int] = None) -> np.ndarray:
        """
        Outputs the last k KLs (last element is last KL)
        """

        if k is None:
            init = 0
        else:
            init = max(0, self._n_filled - k)

        return self._KLs[init : self._n_filled]

    def means(self, k: Optional[int] = None) -> np.ndarray:
        """
        Outputs the last k means (last element is last mean)
        """

        if k is None:
            init = 0
        else:
            init = max(0, self._n_filled - k)

        return self._means[init : self._n_filled]

    def best(self) -> tuple[np.ndarray, float]:
        if self._n_filled == 0:
            raise ValueError("Empty history")

        pars, scores = self.proba_pars(), self.VI_scores()

        best_ind = np.nanargmin(scores)
        return pars[best_ind], scores[best_ind]

    def save(self, name: str, path: str = ".", overwrite: bool = True) -> str:
        if not os.path.isdir(path):
            raise ValueError(f"{path} should point to a folder")
        acc_path = os.path.join(path, name)
        os.makedirs(acc_path, exist_ok=overwrite)

        proba_pars, VI_scores, KLs, means = self.get_all()
        io.rw_arr.save(os.path.join(acc_path, "proba_pars.json"), proba_pars)
        io.rw_arr.save(os.path.join(acc_path, "VI_scores.json"), VI_scores)
        io.rw_arr.save(os.path.join(acc_path, "KLs.json"), KLs)
        io.rw_arr.save(os.path.join(acc_path, "means.json"), means)

        with open(os.path.join(acc_path, "proba_map.dl"), "wb") as file:
            dill.dump(self.proba_map, file)
        return acc_path


def load_hist_vi(path: str) -> HistVILog:
    """Load a HistVILog from saved file"""
    # Check folder existence
    if not os.path.isdir(path):
        raise ValueError(f"{path} should point to a folder")

    # Load data
    proba_pars = io.rw_arr.load(os.path.join(path, "proba_pars.json"))
    VI_scores = io.rw_arr.load(os.path.join(path, "VI_scores.json"))
    KLs = io.rw_arr.load(os.path.join(path, "KLs.json"))
    means = io.rw_arr.load(os.path.join(path, "means.json"))

    # Load proba_map using dill
    with open(os.path.join(path, "proba_map.dl"), "rb") as file:
        proba_map: ProbaMap = dill.load(file)

    n = len(proba_pars)
    hist = HistVILog(proba_map, n)
    hist.add(proba_pars, VI_scores, KLs, means)  # type: ignore
    return hist
