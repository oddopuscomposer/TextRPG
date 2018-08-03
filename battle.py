import numpy as np
from game_utilities import *
from termcolor import colored


def battle(character, enemy):
    """
    Main Battle Method
    :param character:
    :param enemy:
    :return:
    """
    saves = process_json("saves.json")
    character_stats = character["stats"]
    max_hp = enemy["hp"]
    enemy_name = colored(enemy["name"], "red")
    character_name = colored(character["name"], "blue")
    turn = 1
    run = False

    if evasion_check(character, enemy) == 1:  # if character is faster
        attack_turn = "character"
    else:  # if enemy is faster
        attack_turn = "enemy"

    print(character_name + ": " + str(character["hp"]) + "/" + str(character["max_hp"]))
    print(enemy_name + ": " + str(max_hp) + "/" + str(max_hp))

    print(attack_turn + " goes first")
    while True:  # A turn iteration
        print("################################")
        print("Turn - " + str(turn))
        if attack_turn == "character":  # if it is the character's turn to attack
            choice = input("Attack, Item, Run: ").lower()
            while True:
                if choice == "attack":
                    crit = critical_check(character)

                    if crit:
                        print(colored("CRITICAL", "yellow"))
                    att = attack(character, crit)

                    print(character_name + " attacked with " + colored(str(att), 'blue') + " damage.")

                    defs = np.random.choice(enemy["defend"], 1)[0]

                    print(enemy_name + " defended with " + colored(str(defs), 'red') + " block.")

                    damage = defend(enemy, att, defs, False)

                    print(enemy_name + " took " + colored(str(damage), 'red') + " damage.")
                    if enemy["hp"] >= 0:
                        print(enemy_name + " has " + colored(str(enemy["hp"]), 'red') + " HP left")
                    else:
                        print(enemy_name + " has " + colored("0", 'red') + " HP left")

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

            print(enemy_name + " attacked with " + colored(str(att), "red") + " damage.")

            choice = input("defend, evade, parry: ")

            crit = critical_check(character)
            while True:
                if choice == "defend":
                    damage = defend(character, att, character["stats"]["def"], crit)
                    print(character_name + " defended with " + colored(str(character_stats["def"]), "blue") +
                          " block.")
                    print(character_name + " took " + colored(str(damage), 'blue') + " damage.")
                    print(character_name + " has " + colored(str(character["hp"]), 'blue') + " HP left.")
                    break
                elif choice == "evade":
                    damage = evade(character, att, character_stats["evd"], crit)
                    print(character_name + " evaded with " + colored(str(character_stats["evd"]), 'blue') + " evade")
                    print(character_name + " took " + colored(str(damage), 'blue') + " damage.")
                    print(character_name + " has " + str(character["hp"]) + " HP left.")
                    break
                elif choice == "parry":
                    pass
                    break
                else:
                    choice = input("defend, evade, parry: ")

            attack_turn = "character"
        if character["hp"] <= 0:
            print("You were " + colored("defeated!", "blue"))
            character["deaths"] += 1
            break
        if enemy["hp"] <= 0:
            print("The enemy was " + colored("defeated!", "red"))
            loot(character, enemy)
            break
        turn += 1

    saves["saves"][character["name"]] = character
    write_json("saves.json", saves)


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
    character_name = colored(character["name"], 'blue')
    enemy_name = colored(enemy["name"], 'red')
    progression = process_json("progression.json")
    character["exp"] += enemy["exp"]
    print(character_name + " gained " + colored(str(enemy["exp"]), 'magenta') + " experience")
    if character["exp"] > character["exp_req"]:
        character["exp"] = character["exp"] - character["exp_req"]
        character["level"] += 1
        print(character_name + " grew to level " + colored(str(character["level"]), 'magenta'))
        character["exp_req"] = progression[str(character["level"])]

    character["gold"] += enemy["gold"]
    if enemy["gold"] != 0:
        print(enemy["name"] + " dropped " + colored(str(enemy["gold"]), 'yellow') + " gold")

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
            print(enemy_name + " dropped a " + rarity_color_assigner(drop))
            character["inventory"].append(drop)
        else:
            print(enemy_name + " did not drop anything")
    else:
        print(enemy_name + " did not drop anything")


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
    :param att:
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