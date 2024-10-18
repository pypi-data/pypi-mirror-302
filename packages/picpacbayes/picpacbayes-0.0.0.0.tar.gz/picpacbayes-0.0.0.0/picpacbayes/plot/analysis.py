import os

import matplotlib.pyplot as plt

from picpacbayes.optim_result_vi import OptimResultVI
from picpacbayes.plot.accu import plot_scores
from picpacbayes.plot.hist_vi import plot_hist_vi
from picpacbayes.plot.optim_result import plot_score_evol


def make_analysis_plots(optim_result: OptimResultVI, save_path="."):
    plot = plot_scores(optim_result.sample_val, plot=plt)
    plot.savefig(os.path.join(save_path, "scores_scatter.pdf"))
    plot.show()
    plot.clf()

    plot = plot_hist_vi(optim_result.log_vi, plot=plt)
    plot.savefig(os.path.join(save_path, "KPI_evol.pdf"))
    plot.show()
    plot.clf()

    plot = plot_score_evol(optim_result, plot=plt)
    plot.savefig(os.path.join(save_path, "scores_evol.pdf"))
    plot.show()
    plot.clf()
