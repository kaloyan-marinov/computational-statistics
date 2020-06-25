"""
Recipe for Hacking Statistics: Bootstrap Resampling (Bootstrapping)

Bootstrapping is well-studied in the statistics community and rests on solid
theoretical grounds.

Some caveats about bootstrapping are as follows:
- It doesn't work well for rank-based statistics (e.g. maximum value).
- It works poorly with very few samples (N > 20 is a good rule of thumb).
- As always, be careful about selection biases & non-independent data!

You have multiple measurements of the some unknown quantity.

How can you characterize the distribution of these measurements?
More concretely, you want to know: in the long run (i.e. if you were to make
measurements of the quantity of interest for an infinite amount of time), what
would be the average measurement, and what would would be the spread of that?
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def setup_problem():
    measurements = [
        48, 24, 32, 61, 51, 12, 32, 18, 19, 24,
        21, 41, 29, 21, 25, 23, 42, 18, 23, 13]
    return np.array(measurements)

def measurement_distrib_analytically(measurements):
    mean = np.mean(measurements)

    unbiased_std = np.std(measurements, ddof=1)
    n = len(measurements)
    standard_err_of_mean = unbiased_std / np.sqrt(n)
    # ... But what assumptions go into these formulas?
    return mean, standard_err_of_mean

def means_distrib_via_simulation(measurements_arr, iterations=1000):
    """
    Again, unlike coin flipping, we don't have a generating model.
    And unlike the previous example, we are not comparing 2 different groups.

    We treat the measurements as (a proxy to or measurement of) its own
    (sampling) distribution.

    Idea:
    Simulate the (sampling) distribution (of possible quantity measurements) by
    drawing samples with replacement repeatedly and computing the desired
    statistic.

    Motivation:
    The data estimates its own (sampling) distribution - we draw random samples
    from this distribution.

    Args:
        measurements (np.array, 1-dim): measurements of a quantity of interest
    """
    n = len(measurements_arr)
    means_arr = np.empty(iterations)
    for i in range(iterations):
        resampled_meas_arr = measurements_arr[np.random.randint(n, size=n)]
        means_arr[i] = np.mean(resampled_meas_arr)    
    return means_arr

if __name__ == '__main__':
    # Set up the problem.
    measurements = setup_problem()

    # Solve.
    mean, standard_err_of_mean = measurement_distrib_analytically(measurements)
    print('The distribution of the measurements is'
          f' {mean:0.2f} +/- {standard_err_of_mean:0.2f}')

    means_sim = means_distrib_via_simulation(
        np.array(measurements)
    )
    mean_sim = np.mean(means_sim)
    # It isn't necessary to set ddof=1 in the next instruction, because
    # len(means_arr) is large.
    standard_err_of_mean_sim = np.std(means_sim)
    print('The distribution of the measurements has been estimated to be'
          f' {mean_sim:0.2f} +/- {standard_err_of_mean_sim:0.2f}')

    # Plot the simulated means.
    target = os.path.abspath(__file__).replace('.py', '.png')
    print(f'Saving a plot to {target}')

    fig, ax = plt.subplots()
    
    ax.hist(means_sim, bins=40, rwidth=0.90)
    ax.set(xlabel="bootstrap resamplings' means", ylabel="counts")
    ax.grid()
    
    fig.savefig(target)
