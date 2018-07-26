import numpy as np
from game_utilities import *


def battle(character, enemy):
    """
    Main Battle Method
    :param character:
    :param enemy:
    :return:
    """
    character_stats = character["stats"]
    attack_turn = ""
    max_hp = enemy["hp"]
    enemy_name = enemy["name"]
    turn = 1
    run = False

    if evasion_check(character, enemy) == 1:  # if character is faster
        attack_turn = "character"
    else:  # if enemy is faster
        attack_turn = "enemy"

    print(character["name"] + ": " + str(character["hp"]))
    print(enemy_name + ": " + str(max_hp))

    print(attack_turn + " goes first")
    while True:  # A turn iteration
        print("################################")
        print("Turn - " + str(turn))
        if attack_turn == "character":  # if it is the character's turn to attack
            choice = input("attack, run, item: ")
            while True:
                if choice == "attack":
                    crit = critical_check(character)

                    if crit:
                        print("CRITICAL")
                    att = attack(character, crit)

                    print(character["name"] + " attacked with " + str(att) + " damage.")

                    defs = np.random.choice(enemy["defend"], 1)[0]

                    print(enemy_name + " defended with " + str(defs) + " block.")

                    damage = defend(enemy, att, defs, False)

                    print(enemy_name + " took " + str(damage) + " damage.")
                    if enemy["hp"] >= 0:
                        print(enemy_name + " has " + str(enemy["hp"]) + " HP left")
                    else:
                        print(enemy_name + " has 0 HP left")

                    break

                elif choice == "run":
                    run = run_check(character["level"], enemy["level"])
                    if run:
                        print("Success!")
                        break
                    else:
                        print("Failed!")
                        break
                else:
                    choice = input("attack, run, item: ")
            if run:
                break
            attack_turn = "enemy"

        else:  # if it is the enemy's turn to attack
            pass
            att = np.random.choice(enemy["attack"], 1)[0]

            print(enemy_name + " attacked with " + str(att) + " damage.")

            choice = input("defend, evade, parry: ")

            crit = critical_check(character)
            while True:
                if choice == "defend":
                    damage = defend(character, att, character["stats"]["def"], crit)
                    print(character["name"] + " defended with " + str(character["stats"]["def"]) + " block.")
                    print(character["name"] + " took " + str(damage))
                    print(character["name"] + " has " + str(character["hp"]) + " HP left.")
                    break
                elif choice == "evade":
                    damage = evade(character, att, character["stats"]["evd"], crit)
                    print(character["name"] + " evaded with " + str(character["stats"]["evd"]) + " evade")
                    print(character["name"] + " took " + str(damage))
                    print(character["name"] + " has " + str(character["hp"]) + " HP left.")
                    break
                elif choice == "parry":
                    pass
                    break
                else:
                    choice = input("defend, evade, parry: ")

            attack_turn = "character"
        if character["hp"] <= 0:
            print("You were defeated!")
            character["deaths"] += 1
            break
        if enemy["hp"] <= 0:
            print("The enemy was defeated!")
            loot(character, enemy)
            break
        turn += 1

    enemy["hp"] = max_hp


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
    print(character["name"] + " gained " + str(enemy["exp"]) + " experience")
    if character["exp"] > character["exp_req"]:
        character["exp"] = character["exp"] - character["exp_req"]
        character["level"] += 1
        print(character["name"] + " grew to level " + str(character["level"]))
        character["exp_req"] = progression[str(character["level"])]

    character["gold"] += enemy["gold"]
    if enemy["gold"] != 0:
        print(enemy["name"] + " dropped " + str(enemy["gold"]) + " gold")

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
        else:
            print(enemy["name"] + " did not drop anything")


def critical_check(character):
    """
    Checks to see if the action is a crit.
    :param character:
    :return:
    """
    chance = character["stats"]["crt"]
    roll = np.random.randint(1, 1000)
    #print("Your critical chance is " + str(chance) + " /1000 (" + percentage_converter(chance/1000) + "%)")
    if roll < chance:
        return True
    else:
        return False


def attack(character, critical):
    """
    Character attack damage calculations
    :param character:
    :param critical:
    :return:
    """
    items = process_json("items.json")["items"]
    att = 0
    if character["equipment"]["right hand"] != "empty":
        att = items[character["equipment"]["right hand"]]["damage"]


    if critical:
        return (character["stats"]["att"] + att) * 2
    else:
        return character["stats"]["att"] + att


def defend(entity, att, defense, critical):
    """
    Defending an attack
    :param entity:
    :param attack:
    :param defense:
    :param critical:
    :return:
    """
    if isinstance(defense, list):
        defense = np.random.choice(defense, 1)[0]

    damage = int(att - defense)
    if damage < 1:
        damage = 1
    if critical:
        damage = 0
    if att == 0:
        damage = 0

    entity["hp"] = entity["hp"] - damage

    return damage


def parry(entity, att, defense, critical):
    """
    Parrying an attack
    :param entity:
    :param attack:
    :param defense:
    :param critical:
    :return:
    """
    pass


def evade(entity, att, evd, critical):
    """
    Character evade mechanic
    :param entity:
    :param att:
    :param evd:
    :param critical:
    :return:
    """
    if evd > att:
        damage = 0
    else:
        damage = att

    entity["hp"] = entity["hp"] - damage

    return damage