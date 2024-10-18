import matplotlib.pyplot as plt

from picpacbayes.hist_bayes import HistBayesLog


def plot_hist_pbays(hist_bayes: HistBayesLog, plot=plt):
    """
    Plot evolution of KPIs of a PAC-Bayes learning task.
    KPIs plotted are the PAC-Bayes objective, the mean score, and the Kullback-Leibler divergence
    """

    plot.plot(hist_bayes.means(), label="Mean score")
    plot.plot(hist_bayes.pbayes_scores(), label="VI scores")
    plot.plot(hist_bayes.pbayes_scores() - hist_bayes.means(), label="Temperature * KL")
    plot.xlabel("Step")
    plot.legend()
    plot.title("Evolution of PAC-Bayes learning objectives")

    return plot
