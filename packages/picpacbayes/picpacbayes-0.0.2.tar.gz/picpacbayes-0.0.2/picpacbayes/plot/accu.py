import matplotlib.pyplot as plt
import numpy as np

from picoptim.fun_evals import FunEvals


def plot_scores(
    sample_val: FunEvals,
    *args,
    plot=plt,
    marker: str = "x",
    s: float = 0.2,
    **kwargs
):
    """
    Plot the scores computed at each generation

    Note:
        This is a simplified version of the plot generated in plot_score_evol

        Main advantages:
        - Much quicker to produce
        - no interpolation

        Main disadvantage:
        - Needs quite a lot of points generated at each gen to be relevant
        - less smooth/might be less readable
    """

    generations = sample_val.gen_tracker()
    values = sample_val.vals()
    invert_gen = np.max(generations) - generations
    plot.scatter(invert_gen, values, *args, marker=marker, s=s, **kwargs)
    plot.xlabel("Step")
    plot.title("Evolution of scores evaluation")
    return plot
