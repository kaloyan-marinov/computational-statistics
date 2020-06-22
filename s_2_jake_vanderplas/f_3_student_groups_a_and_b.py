"""
Recipe for Hacking Statistics: Shuffling

Inspired by John Rauser's "Statistics Without All the Agonizing Pain".

You have two groups of students: Group A and Group B.
Let's say you are researcher, and you want to answer whether the students in
Group A are better than those in Group B.
You give them all the same test, which is scored on a scale from 0 to 100.
"""

import numpy as np
import random

def setup_problem():
    group_a_scores = [84, 72, 57, 46, 63, 76, 99, 91]
    group_b_scores = [81, 69, 74, 61, 56, 87, 69, 65, 66, 44, 62, 69]
    return group_a_scores, group_b_scores

def p_value_analytically_by_hand(group_a_scores, group_b_scores):
    """Apply Welch's t-test:
    1. compute the t-statistic;
    2. look up how the t-statistic is distributed, which depends on something
       called "degrees of freedom";
    3. look up that you can find (an approximation of) the degrees of freedom
       by means of the Welch-Satterthwaite equation;
    4. use the determined (approximate) degrees of freedom for your desired
       significance level to determine "the critical value" of the t-statistic;
    5. check whether the observed/computed t-value is > than t_crit.

    Conclude that the difference of 6.6 is not significant at the p = 0.05
    level.

    [We've entirely lost track of what question we're answering!]
    """
    pass

def p_value_analytically(group_a_scores, group_b_scores):
    from statsmodels.stats.weightstats import ttest_ind
    t, p, dof = ttest_ind(
        group_a_scores, group_b_scores,
        alternative='larger',
        usevar='unequal'
    )
    # ... But what question is this answering?
    return p

def p_value_via_simulation(delta, group_a_scores, group_b_scores,
                           iterations=10000):
    """
    Unlike coin flipping, we don't have a (theoretical) generative model
    - we can't simulate a student.

    All we have are their test scores, so we need some way for those test scores
    to be the simulation themselves.

    Idea:
    Simulate the (sampling) distribution (of possible test scores) by shuffling
    the labels repeatedly and computing the desired statistic.

    Motivation:
    In the null hypothesis - if the students in group A and the students in
    Group B are really the same, then switching them shouldn't change the
    result!
    """
    size_a = len(group_a_scores)
    size_b = len(group_b_scores)
    scores = group_a_scores + group_b_scores

    count = 0
    for i in range(iterations):
        # Shuffle labels.
        random.shuffle(scores)
        # Rearrange.
        simulated_group_a_scores = scores[:size_a]
        simulated_group_b_scores = scores[size_a + 1:]
        # Compute means.
        mean_a = np.mean(simulated_group_a_scores)
        mean_b = np.mean(simulated_group_b_scores)
        
        if mean_a - mean_b > delta:
            count += 1

    return count / iterations

if __name__ == '__main__':
    # Set up the problem.
    group_a_scores, group_b_scores = setup_problem()

    mean_a = np.mean(group_a_scores)
    mean_b = np.mean(group_b_scores)
    delta = mean_a - mean_b
    print(round(mean_a, 1))
    print(round(mean_b, 1))
    print(round(delta, 1))

    # Solve.
    p = p_value_analytically(group_a_scores, group_b_scores)
    print(f'P(the observed effect | H_0) is {p}')

    p_sim = p_value_via_simulation(delta, group_a_scores, group_b_scores)
    print(f'P(the observed effect | H_0) has been estimated to be {p_sim}')
