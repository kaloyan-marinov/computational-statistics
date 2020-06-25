"""
Recipe for Hacking Statistics: Boostrap Resampling

Bootstrapping can be applied to even more complicated statistics.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

from scipy.stats import pearsonr

def setup_problem():
    pairs = [
        (8.1, 21), (8.3, 19), (8.7, 17), (8.9, 18), (9.0, 15), (9.1, 17),
        (9.2, 17), (9.3, 17), (9.4, 19), (9.6, 14), (9.9, 14), (10.0, 15),
        (10.0, 11), (10.5, 12), (10.6, 12), (10.6, 12), (10.6, 13), (11.2, 10),
        (11.7, 8), (12.6, 9)
    ]
    x = np.array([p[0] for p in pairs])
    y = np.array([p[1] for p in pairs])
    return x, y

def linear_fit_via_simulation(x, y, iterations=10000):
    n = len(x)
    results = np.empty((iterations, 2))
    for i in range(iterations):
        indices = np.random.randint(n, size=n)
        m, b = np.polyfit(x[indices], y[indices], deg=1)
        results[i] = (m, b)
    results_df = pd.DataFrame(data=results, columns=['slope', 'intercept'])
    return results_df

if __name__ == '__main__':
    # Set up the problem.
    x, y = setup_problem()

    # Visualize the raw data.
    target = os.path.abspath(__file__.replace('.py', '_1_raw_data.png'))

    fig, ax = plt.subplots()

    ax.scatter(x, y, s=10)
    ax.grid()
    ax.set(
        xlabel='quantity #1', ylabel='quantity #2',
        xlim=[7, 13], ylim=[0, 25]
    )

    fig.savefig(target)

    # Solve.
    results_df = linear_fit_via_simulation(x, y)

    # Visualize (the distribution of) the computed results.
    # (
    #   For future reference, the following are handy resources that I utilized
    #   in order to implement the code-block below:
    #       https://seaborn.pydata.org/generated/seaborn.jointplot.html#seaborn.jointplot
    #       https://kite.com/python/docs/seaborn.JointGrid
    #       https://www.kaggle.com/keshavbansal001/complete-seaborn-tutorial
    #       https://github.com/mwaskom/seaborn/issues/1873
    #       https://matplotlib.org/tutorials/introductory/customizing.html
    # )
    plt.style.use('seaborn')

    fig, ax = plt.subplots()

    joint_grid = sns.jointplot(
        'slope', 'intercept', data=results_df,
        kind='kde', color=sns.palettes.color_palette()[0]
    )
    joint_grid.set_axis_labels('slope', 'intercept')
    joint_grid.annotate(pearsonr)

    target = os.path.abspath(__file__.replace('.py', '_2_results_distrib.png'))
    joint_grid.savefig(target)
