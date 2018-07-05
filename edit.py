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
    entry = input("Enter hp: ")
    health = numeric_validation(entry)
    classes["classes"][name]["start_hp"] = int(health)

    entry = input("Enter mp: ")
    mana = numeric_validation(entry)
    classes["classes"][name]["start_mp"] = int(mana)
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
    items["items"][name] = {}
    item = items["items"][name]

    desc = input("Enter item description: ")
    item["description"] = desc

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
    item["classes"] = words

    entry = input("Enter slot: ")
    slot = slot_validation(entry)
    item["slot"] = slot

    item["stats"] = {}
    stats = input("Enter buffs([att],[def],[evd],[hp],[mp]): ")
    words = stats.split(",")
    # need validation
    item["buffs"]["att"] = words[0]
    item["buffs"]["def"] = words[1]
    item["buffs"]["evd"] = words[2]
    item["buffs"]["hp"] = words[3]
    items["buffs"]["mp"] = words[4]

    write_json("items.json", items)


def delete_item():
    """
    Removes equipable from items.json
    :return:
    """
    entry = input("Please enter an equipable to delete: ")
    items = process_json("items.json")
    if entry in items["items"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                del items["items"][entry]
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
    # "buy_price": 10,
    # "sell_price": 5,
    # "rarity": "common",
    # "description": "",
    # "type": "misc"
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
    Adds enemy to enemies.json
    :return:
    """
    pass


def delete_enemy():
    """
    Removes enemy from enemies.json
    :return:
    """
    pass


def add_shop():
    """
    Adds shop to shops.json // [shops] [xref] locations[location][shops]
    :return:
    """
    pass


def delete_shop():
    """
    Removes shop from shops.json
    :return:
    """
    pass


def edit_game():
    """
    Main edit method
    :return:
    """
    pass

