"""
source:
- the talk is on https://www.youtube.com/watch?v=S41zQEshs5k
- the slides are on https://docs.google.com/presentation/d/1_s_-8YM5_-CjWVHpbJcYF5gnvGYwwLDtCCqvl_G8I5s/present#slide=id.i35
- the talk uses the following question as an example:
  https://www.reddit.com/r/statistics/comments/jiwkx/good_news_everyone_i_need_help_figuring_out_which/)

The problem statement is as follows:
    
    "As part of a college course we gave a class of students a pre
    and post test ... to judge how well the students knew the
    material before and after the class.

    I would like to know what type of test to run and what I can
    justifiably infer from the data...

    We have 30 students who took the test twice (before and after). E
    test was 50 problems and the students received a number
    grade (with a corresponding percentage score)."

slide at 5:33,
and the next one,
and the next one
[when you're making your hypothesis precise, you're also choosing what your test
statistic is going to be
- you have to boil down the size of the *apparent effect* to *one number*]

"What are the chances of seeing an apparent effect as big as that by chance?"

The null hypothesis is a *model* of the system where the apparent effect is not
real - we're going to need to make some modeling assumptions:
slide at 11:07

slide exactly at 14:22

We have to be careful about what the p-value is, and what it isn't.
- It is the answer to one very specific question: "What are the chances of
  seeing what we saw by chance?"
- It doesn't tell us how likely it is that the students learned (so we don't
  have a probability for that without doing some more work).
- It doesn't really tell us about how much they learned - if we want to do that,
  then we have to do an estimation problem and that's a different statistical
  method. 
"""

import numpy as np
import random

def flip(pc):
    """Returns 1 with probability pc, and 0 otherwise."""
    return 1 if random.random() < pc else 0

def fake_exam(pc, num_questions):
    """Generates an exam score for a student with probability pc."""
    answers = [flip(pc) for __ in range(num_questions)]
    score = sum(answers)
    return score

def fake_diff(pc, num_questions):
    """Generates the difference in two exam scores for a student with
    probability pc."""
    post_exam_score = fake_exam(pc, num_questions)
    pre_exam_score = fake_exam(pc, num_questions)
    return post_exam_score - pre_exam_score

def fake_diffs(pcs, num_questions):
    """Generates differences in exam scores for students with given values of
    pc.

    This simulates running the entire experiment - giving a pre-test and a
    post-test to each student.

    Args:
        pcs (list): Values of pc, one for each student.
        num_questions (int): The number of questions.
    """
    return [fake_diff(pc, num_questions) for pc in pcs]

def p_value(delta, pcs, num_questions, iterations=10000):
    """Computes the probability of seeing a mean difference in exam scores
    which is >= delta for students with given values of pc.

    Args:
        delta (float): The observed difference in exam score means
        (the apparent effect).
        pcs (list): Values of pcs, one for each student.
        num_questions (int): The number of questions.
        iterations (int, optional): The number of iterations. Defaults to 10000.
    """
    count = 0
    for i in range(iterations):
        diffs = fake_diffs(pcs, num_questions)
        if np.mean(diffs) > delta:
            count += 1
    return count / iterations

if __name__ == '__main__':
    # I did not find the raw data anywhere, so I created my own data as follows:
    # a) called [random.randint(1, num_questions) for __ in range(30)] in an
    #    interactive Python session, and hard-coded the output here;
    num_questions = 50
    pre_exam_scores = [
        48, 27, 18, 43, 25, 25, 27, 17, 10, 29, 48, 43, 17, 25, 28, 14, 12, 26,
        19, 28, 36, 30, 12, 48, 19, 41, 1, 3, 30, 50
    ]
    # b) hard-coded the same observed difference in means;
    observed_mean_diff = 2
    # c) created the post-exam scores in the most naive way
    #    (even though, in this case, that gives rise to post-exam scores that
    #    are impossible to observe - because the last student's pre-exam score
    #    was already at its max;
    #    but that doesn't affect the rest of the procedure).
    post_exam_scores = [x + observed_mean_diff for x in pre_exam_scores]

    # Determine the p-value (computationally/empirically).
    delta = np.mean(np.array(post_exam_scores) - np.array(pre_exam_scores))
    pcs = np.array(pre_exam_scores) / 50
    p = p_value(delta, pcs, num_questions)
    print(f'The p-value, P(observed effect|H_0), has been estimated to be: {p}')
