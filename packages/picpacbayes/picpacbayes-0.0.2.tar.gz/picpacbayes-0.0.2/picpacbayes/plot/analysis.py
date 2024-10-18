import os

import matplotlib.pyplot as plt

from picpacbayes.optim_result_pbayes import OptimResultPBayes
from picpacbayes.plot.accu import plot_scores
from picpacbayes.plot.hist_bayes import plot_hist_bayes
from picpacbayes.plot.optim_result import plot_score_evol


def make_analysis_plots(optim_result: OptimResultPBayes, save_path="."):
    plot = plot_scores(optim_result.sample_val, plot=plt)
    plot.savefig(os.path.join(save_path, "scores_scatter.pdf"))
    plot.show()
    plot.clf()

    plot = plot_hist_bayes(optim_result.log_pbayes, plot=plt)
    plot.savefig(os.path.join(save_path, "KPI_evol.pdf"))
    plot.show()
    plot.clf()

    plot = plot_score_evol(optim_result, plot=plt)
    plot.savefig(os.path.join(save_path, "scores_evol.pdf"))
    plot.show()
    plot.clf()
