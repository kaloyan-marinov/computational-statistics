"""
Statistics is fundamentally about
Asking the Right Question (about your Data).

Thesis: If you can write a for-loop, you can do statistics.

Warm-up:
You toss a coin 30 times and see 22 heads. Is it a fair coin?

Advocate:
    A fair coin should show heads exactly 50% of time. This coin is biased.
Skeptic:
    Even a fair coin could show 22 heads in 30 tosses. It might just be chance.
Classic method:
    Assume the Skeptic is correct: test the null hypothesis.
    What is the probability of a fair coin showing 22 heads simply by chance,
    i.e. what is P(22 heads in 30 tosses | fair coin) = ?

    Analytically, P(22 heads in 30 tosses | fair coin)
    = (30 choose 22) 0.5^22 (1 - 0.5)^(30 - 22)
"""

import matplotlib.pyplot as plt
import os

from scipy.special import binom

def setup_coin_toss_problem():
    n_flips = 30
    n_heads = 22
    return n_flips, n_heads

def p_value_analytically(n_flips, n_heads, p_heads=0.5):
    return (binom(n_flips, n_heads) * p_heads**n_heads
    * (1 - p_heads)**(n_flips - n_heads)
    )

if __name__ == '__main__':
    # Set up the problem.
    n_flips, n_heads = setup_coin_toss_problem()

    # Simulate.
    possible_heads_counts = range(n_flips)
    probabilities = [
        p_value_analytically(n_flips, i) for i in possible_heads_counts
    ]

    # Summarize the results.
    p_value = sum([
        probabilities[i] for i in possible_heads_counts if i >= n_heads
    ])
    print('Assuming the null hypothesis is true (i.e. assuming there is no'
          ' effect that we are interested in), the probability of getting the'
          f' observed data just by chance is {p_value}')

    # Plot the results.
    target = os.path.abspath(__file__).replace('.py', '.png')
    print(f'Saving a plot to {target}')
    fig, ax = plt.subplots()

    ax.step(possible_heads_counts, probabilities, where='mid')
    '''
    ax.plot(possible_heads_counts, probabilities, 'C1o')
    '''
    ax.set(xlabel='number of heads', ylabel='probability')
    ax.grid()

    ax.axvline(x=22, color='red')

    ax.text(22.5, 0.06, 'tosses with >= 22 heads', color='red')

    fig.savefig(target)
