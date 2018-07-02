from game_utilities import *


def delete_save():
    """
    Removes save from saves.json
    :return:
    """
    pass


def add_class():
    """
    adds a class to the classes json database
    :return:
    """
    classes = process_json("classes.json")
    name = input("Enter class name: ")
    classes["classes"][name] = {}
    entry = input("Enter health: ")
    health = numeric_validation(entry)
    classes["classes"][name]["health"] = int(health)

    entry = input("Enter mana: ")
    mana = numeric_validation(entry)
    classes["classes"][name]["mana"] = int(mana)
    classes["xref"].append(name)

    write_json("classes.json", classes)
    print("Successfully Added")


def delete_class():
    """
    Removes class from classes.json
    :return:
    """
    entry = input("Please enter a class to delete: ")
    classes = process_json("classes.json")
    if entry in classes["xref"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                del classes["classes"][entry]
                classes["xref"].remove(entry)
                print("Item deleted")
                break
            elif confirm == "n":
                break
            else:
                pass
    else:
        print("entry is not in classes")

    write_json("classes.json", classes)


def add_equipable():
    """
    adds equipable item to items.json
    :return:
    """
    items = process_json("items.json")

    name = input("Enter item name: ")
    items["equipment"][name] = {}
    item = items["equipment"][name]

    entry = input("Enter buy price: ")
    buy_price = numeric_validation(entry)
    item["buy_price"] = int(buy_price)

    entry = input("Enter sell price: ")
    sell_price = numeric_validation(entry)
    item["sell_price"] = int(sell_price)

    entry = input("Enter rarity(common, uncommon, rare, ancient, legendary): ")
    rarity = rarity_validation(entry)
    item["rarity"] = rarity

    entry = input("Enter damage: ")
    damage = numeric_validation(entry)
    item["damage"] = int(damage)

    cls = input("Enter required classes([class1],[class2]): ")
    # need validation
    words = cls.split(",")
    item["class"] = words

    slot = input("Enter slot: ")
    # need validation
    item["slot"] = slot

    item["stats"] = {}
    stats = input("Enter stats([att],[def],[evd]): ")
    words = stats.split(",")
    # need validation
    item["stats"]["att"] = words[0]
    item["stats"]["def"] = words[1]
    item["stats"]["evd"] = words[2]

    write_json("items.json", items)


def delete_equipable():
    """
    Removes equipable from items.json
    :return:
    """
    entry = input("Please enter an equipable to delete: ")
    items = process_json("items.json")
    if entry in items["equipment"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                del items["equipment"][entry]
                print("Item deleted")
                break
            elif confirm == "n":
                break
            else:
                pass
    else:
        print("entry is not in items")

    write_json("items.json", items)


def add_misc_item():
    """
    Adds misc item to items.json
    :return:
    """
    pass


def delete_misc_item():
    """
    Removes misc item from items.json
    :return:
    """
    pass

def add_skill():
    """
    Adds skill to skills.json
    :return:
    """
    pass


def delete_skill():
    """
    Removes skill from skills.json
    :return:
    """
    pass


def add_location():
    """
    Adds location to locations.json
    :return:
    """
    pass


def delete_location():
    """
    Removes location from locations.json
    :return:
    """
    pass


def add_npc():
    """
    Adds npc to npcs.json
    :return:
    """
    pass


def delete_npc():
    """
    Removes npc from npcs.json
    :return:
    """
    pass


def add_enemy():
    """
    Adds enemy from enemies.json
    :return:
    """
    pass


def delete_enemy():
    """
    Removes enemy from enemies.json
    :return:
    """
    pass


def edit_game():
    """
    Main edit method
    :return:
    """
    pass

# delete_class()
# add_class()
# delete_equipable()
# add_equipable()
