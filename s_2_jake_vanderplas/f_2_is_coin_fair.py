"""
Recipe for Hacking Statistics: Direct Simulation

That works well when you have some a-priori model of the world.
For example, you know that tossing a fair coin will land heads 50% of the time
and you and you can simulate that.
"""
import numpy as np

from s_2_jake_vanderplas.f_1_is_coin_fair import setup_coin_toss_problem

def p_value_via_simulation(n_flips, n_heads, iterations=100000):
    count = 0
    for i in range(iterations):
        trials = np.random.randint(2, size=n_flips)
        if trials.sum() >= n_heads:
            count += 1
    return count / iterations

if __name__ == '__main__':
    # Set up the problem.
    n_flips, n_heads = setup_coin_toss_problem()

    # Solve.
    p = p_value_via_simulation(n_flips, n_heads)
    print(f'P(the observed data | H_0) has been estimated to be {p}')
