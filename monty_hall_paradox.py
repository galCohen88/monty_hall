from random import randint

# configuration (for your choice)
NUMBER_OF_GAMES = 1000000
PLAYER_REPLACE_CURTAINS = True

# constants
GOAT_BEHIND_CURTAIN_REWARD = 0
CAR_BEHIND_CURTAIN_REWARD = 1

CURTAIN_NOT_SELECTED_BY_PLAYER = 0
CURTAIN_SELECTED_BY_PLAYER = 1

SCORE_IDX = 0
SELECTION_IDX = 1


# this will prove the existence of the paradox
# WITH RESULT OF 0.666 AFTER REPLACING THE PLAYER CHOICE

def run(number_of_games, replace_choose_after_choice_curtain_extraction, number_of_curtains=3):
    """
    :param number_of_games how many games player will play
    :type int
    :param replace_choose_after_choice_curtain_extraction should player replace his pick after curtains extraction
    :type bool
    :param number_of_curtains (default 3)
    :returns total games won
    """
    total_games_score = 0
    for i in range(0, number_of_games):
        total_games_score += monty_hall_game(replace_choose_after_choice_curtain_extraction, number_of_curtains)
    return total_games_score


def monty_hall_game(number_of_curtains, replace_choose_after_choice_curtain_extraction):
    """
    :param number_of_curtains determines the number of curtains in monty hall game
    :type int
    :param replace_choose_after_choice_curtain_extraction if player should replace choose (after extraction of other curtains)
    :returns int (1 / 0) 1 if player won, 0 if player lose
    """
    curtains = [[GOAT_BEHIND_CURTAIN_REWARD for x in range(2)] for y in range(number_of_curtains)]
    car_idx = randint(0, number_of_curtains - 1)
    curtains[car_idx][SCORE_IDX] = CAR_BEHIND_CURTAIN_REWARD

    first_player_pick_idx = randint(0, len(curtains) - 1)
    curtains[first_player_pick_idx][SELECTION_IDX] = CURTAIN_SELECTED_BY_PLAYER
    curtains = remove_curtain(curtains)
    first_selection_new_index = -1
    for i, curtain in enumerate(curtains):
        if curtain[SELECTION_IDX] == CURTAIN_SELECTED_BY_PLAYER:
            first_selection_new_index = i

    if replace_choose_after_choice_curtain_extraction:
        curtains[first_selection_new_index][SELECTION_IDX] = CURTAIN_NOT_SELECTED_BY_PLAYER
        second_player_pick_idx = 1 if first_selection_new_index == 0 else 0
        curtains[second_player_pick_idx][SELECTION_IDX] = CURTAIN_SELECTED_BY_PLAYER
    return calculate_game_result(curtains)


def remove_curtain(curtains):
    while len(curtains) > 2:
        remove_idx = randint(0, len(curtains) - 1)
        if curtains[remove_idx][SELECTION_IDX] == CURTAIN_NOT_SELECTED_BY_PLAYER and \
                        curtains[remove_idx][SCORE_IDX] == GOAT_BEHIND_CURTAIN_REWARD:
            del curtains[remove_idx]
    return curtains


def calculate_game_result(curtains):
    for curtain in curtains:
        if curtain[SELECTION_IDX] == CURTAIN_SELECTED_BY_PLAYER and curtain[SCORE_IDX] == CAR_BEHIND_CURTAIN_REWARD:
            return 1
    return 0


print 'player won {0}% of the games'.format(
    (run(NUMBER_OF_GAMES, 3, PLAYER_REPLACE_CURTAINS) / float(NUMBER_OF_GAMES)) * 100)
