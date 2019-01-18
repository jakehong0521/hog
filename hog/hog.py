"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    s = 1
    score = 0
    r = []
    while s <= num_rolls:
        r.append(dice())
        s += 1
    for i in range(num_rolls):
        if r[i] == 1:
            return 0
        else:
            score += r[i]
    return score
    # END Question 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    if num_rolls > 0:
        score = roll_dice(num_rolls, dice)
    else:
        if opponent_score//10 > opponent_score % 10:
            score = opponent_score//10 + 1
        else:
            score = opponent_score % 10 + 1
    if score == 1:
        return 1
    if score == 0:
        return 0
    if is_prime(score):
        return next_prime(score)
    else:
        return score
def is_prime(score):
    if score == 2:
        return True
    for i in range(2, score):
        if score % i == 0:
            return False
    return True
def next_prime(score):
    s = score + 1
    i = 2
    while i < s:
        if s % i == 0:
            s += 1
            i = 2
        i += 1
    return s
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (opponent_score + score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    # first_score = [int(i) for i in str(score0)]
    # second_score = [int(i) for i in str(score1)]
    # if len(first_score) == 1:
    #     if (first_score[-1] == second_score[-2] and second_score[-1] == 0):
    #         return True
    #     else:
    #         return False
    # if len(second_score) == 1:
    #     if second_score[-1] == first_score[-2] and first_score[-1] == 0:
    #         return True
    #     else:
    #         return False
    # if len(second_score) == 1 and len(first_score) == 1:
    #     if first_score[0] == second_score[0]:
    #         return True
    #     else:
    #         return False
    # elif (first_score[-1] == second_score[-2]) and (first_score[-2] == second_score[-1]): 
    #     return True
    # else:
    #     return False
    a = score0
    b = score1
    if a > 100:
        a -= 100
    if b > 100:
        b -= 100
    if (a // 10 == b % 10 and a % 10 == b // 10):
        return True
    return False
    
    # END Question 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    
    while score0 < goal and score1 < goal:
        if player == 0:
            current_score = take_turn(strategy0(score0, score1), score1, dice = select_dice(score0,score1))
            if current_score == 0:
                score1 += strategy0(score0, score1)
            else:
                score0 += current_score
            player = other(player)
        else:
            current_score = take_turn(strategy1(score1,score0), score0, dice = select_dice(score1, score0))
            if current_score == 0:
                score0 += strategy1(score1, score0)
            else:
                score1 += current_score
            player = other(player)
        if is_swap(score0, score1):
            a = score0
            score0 = score1 
            score1 = a
    # END Question 5 

    return score0, score1

#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def average(*args):
        a = 0 
        for i in range(num_samples):
            a += fn(*args) 
        return a / num_samples
    return average 
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    num_set = []
    a = make_averaged(roll_dice, num_samples)
    for i in range(10):
        num_set.append(a(i+1, dice))
    maxs = max(num_set)
    for item in range(10):
        if num_set[item] == maxs:
            return item + 1

    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    opp = opponent_score
    maxopp = max((opp // 10 + 1), (opp % 10 + 1))
    if is_prime(maxopp):
        maxopp = next_prime(maxopp)
    if maxopp >= margin:
        return 0
    return num_rolls
    
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    opp = opponent_score
    maxopp = max((opp //10 + 1), (opp % 10 + 1))
    if is_prime(maxopp):
        maxopp = next_prime(maxopp)
    if is_swap(score + maxopp, opponent_score):
        if (score + maxopp < opponent_score):
            return 0
    return num_rolls
    # END Question 9


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN Question 10    
    o = opponent_score
    s = score
    dice = select_dice(s,o)
    if dice == six_sided:
        nr = 5  #num rolls if strategies don't work
    else:
        nr = 4  #if four-sided dice
    pg = 0      #doesn't do anything really
    i = 10
    while i >= nr:  #if piggy back results in beneficial swap
        if is_swap(s, o+i) and o > s and i > pg:
            pg = i
        i -= 1
    if pg == 0:
        pg = nr
    margin = 5
    hd = max(o // 10 + 1, o % 10 + 1)   #highest digit for opponent
    if is_prime(hd):
        hd = next_prime(hd) 
    sw = swap_strategy(s, o, num_rolls = nr)
    ba = bacon_strategy(s, o, margin, num_rolls = nr)
    #ms = max_scoring_num_rolls(four_sided,num_samples=10000)
    if is_swap(s + hd, o) and o > s:
        if margin > o - (s + hd):
            return sw
        else:
            return ba
    if pg != nr:
        return pg
    else:
        if ba != nr:
            return ba
    return nr 


    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
