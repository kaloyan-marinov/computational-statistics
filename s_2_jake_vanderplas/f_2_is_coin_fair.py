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

    p = p_value_via_simulation(n_flips, n_heads)
    print('Assuming the null hypothesis is true (i.e. assuming there is no'
          ' effect that we are interested in), the probability of getting the'
          f' observed data just by chance has been deteremined to be {p}')
