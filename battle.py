import numpy as np


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
        print("Turn #" + turn_count)
        while True:     # Full Turn
            if escape_status:
                break
            if turn == 1:
                while True:
                    print("fight, item, run")
                    choice = input("Choose an option: ")
                    if choice == "fight":
                        pass

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
    pass
