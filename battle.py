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
    your_health = character["hp"]
    turn = evasion_check(character, enemy)
    turns = 0
    who_died = 0
    turn_count = 1
    escape_status = False

    while True:     # Full Fight
        print("Turn #" + str(turn_count))
        while True:     # Full Turn
            if escape_status:
                break
            if turn == 1:
                while True:
                    print("fight, item, run")
                    choice = input("Choose an option: ")
                    if choice == "fight":
                        pass
                        enemy_health -= 10
                        break
                    elif choice == "item":
                        pass
                        break
                    elif choice == "run":
                        escape_status = check_run_chance(character["level"], enemy["level"])
                        if escape_status:
                            break
                    else:
                        print("Please select a valid option")
                if enemy_health <= 0:
                    who_died = -1
                    break
                turn_count + turn
                turn = -1
                if turn_count == 0:
                    turns += 1
            if turn == -1:  # enemy turn
                #
                if your_health <= 0:
                    who_died = 1
                    break
                turn_count + turn
                if turn_count == 0:
                    turns += 1
                turn = 1
        break

    if who_died == 1:
        print("Death Message")
    else:
        loot(character, enemy)

    print("Battle ended")


def check_run_chance(character_level, enemy_level):
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

