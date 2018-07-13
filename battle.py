import numpy as np
from game_utilities import *


def battle(character, enemy):
    """
    Main Battle Method
    :param character:
    :param enemy:
    :return:
    """
    enemy_health = enemy["hp"]
    character_health = character["hp"]
    character_stats = character["buffs"]


def run_check(character_level, enemy_level):
    """
    Run away mechanic
    :param character_level:
    :param enemy_level:
    :return:
    """

    chance = np.random.randint(0, 100)
    print("You try to run.")

    diff = abs(character_level - enemy_level)
    enemy_win = 50 - (3.5 * diff)
    char_win = 50 + (5.5 * diff)

    if enemy_win < 5:
        enemy_win = 5

    if character_level < enemy_level:
        if chance < enemy_win:
            run = True
        else:
            run = False
    elif character_level == enemy_level:
        if chance < 50:
            run = True
        else:
            run = False
    else:
        if chance < char_win:
            run = True
        else:
            run = False

    if run:
        print("You escaped!")
    else:
        print("You couldn't run away!")

    return run


def evasion_check(character, enemy):
    """
    Compares evasion stats
    :param character:
    :param enemy:
    :return:
    """
    character_speed = character["stats"]["evd"]
    enemy_speed = enemy["evd"]

    if character_speed > enemy_speed:
        check = 1
    elif character_speed == enemy_speed:
        check = np.random.choice([-1, 1], 1)
    else:
        check = -1
    return check


def loot(character, enemy):
    """
    Enemy resource transfer
    :param character:
    :param enemy:
    :return:
    """
    progression = process_json("progression.json")
    character["exp"] += enemy["exp"]
    if character["exp"] > character["exp_req"]:
        character["exp"] = character["exp"] - character["exp_req"]
        character["level"] += 1
        character["exp_req"] = progression[str(character["level"])]

    if enemy["drops"] != {}:

        items = list(enemy["drops"].keys())
        probs = list((enemy["drops"].values()))

        max_rate = 0
        for item in probs:
            max_rate += item

        if max_rate != 1 and max_rate > 0:
            none_rate = 1 - max_rate
            probs.append(none_rate)
            items.append("none")

        drop = np.random.choice(items, 1, probs)[0]

        if drop != "none":
            print(enemy["name"] + " dropped a " + drop)
            character["inventory"].append(drop)


def crit_check(character):
    """
    Checks to see if the action is a crit.
    :param character:
    :return:
    """
    chance = character["buffs"]["crt"]
    roll = np.random.randint(1, 1000)
    if roll < chance:
        return True
    else:
        return False
