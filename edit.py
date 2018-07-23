from game_utilities import *


def delete_save():
    """
    Removes save from saves.json
    :return:
    """
    saves = process_json("saves.json")
    print("Saves: " + list(saves["saves"].keys()))
    while True:
        choice = input("Which save file would you like to delete?(q to quit): ")
        if choice in saves["saves"].keys():
            del saves["saves"][choice]
            saves["xref"].remove(choice)
            print("Save file deleted")
            break
        elif choice == "q":
            break
        else:
            print("That save file doesnt exist")
    write_json("saves.json", saves)


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

    try:
        items["items"][name]
        while True:
            choice = input("This item already exists, do you want to overwrite? (y/n): ")
            if choice == "y":
                break
            elif choice == "n":
                return "null"
            else:
                print("Invalid input")
    except KeyError:
        pass

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

    print("Options: ")
    print(','.join(process_json("classes.json")["xref"]))
    cls = input("Enter required classes([class1],[class2]): ")
    words = cls.split(",")
    words = class_validation(words)
    item["classes"] = words

    print(["head", "chest", "legs", "feet", "left hand", "right hand", "necklace", "ring"])
    entry = input("Enter a slot/slots([slot1],[slot2]): ")
    entry = entry.split(",")
    slot = slot_validation(entry)
    item["slot"] = slot

    item["buffs"] = {}
    print("These buffs are integer values separated by commas")
    stats = input("Enter buffs([att],[def],[evd],[hp],[mp],[crt]): ")
    words = stats.split(",")
    words = stat_validation(words)
    item["buffs"]["att"] = words[0]
    item["buffs"]["def"] = words[1]
    item["buffs"]["evd"] = words[2]
    item["buffs"]["hp"] = words[3]
    item["buffs"]["mp"] = words[4]
    item["buffs"]["crt"] = words[5]

    item["type"] = "equipment"

    write_json("items.json", items)
    print("Item created and saved")


def delete_item():
    """
    Removes equipable from items.json
    :return:
    """
    items = process_json("items.json")
    print("Options: ")
    print(','.join(list(items["items"].keys())))
    entry = input("Please enter an item to delete: ")

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

    item["type"] = "misc"

    write_json("items.json", items)


def add_skill():
    """
    Adds skill to skills.json
    :return:
    """
    skills = process_json("skills.json")

    name = input("Enter skill name: ")
    skills["skills"][name] = {}
    skill = skills["skills"][name]

    entry = input("Enter damage: ")
    dmg = numeric_validation(entry)
    skill["dmg"] = int(dmg)

    entry = input("Enter mana cost: ")
    mana = numeric_validation(entry)
    skill["mana"] = int(mana)

    entry = input("Enter class requirement([class1],[class2]): ")
    entry = entry.split(",")
    words = class_validation(entry)
    skill["class"] = words

    entry = input("Enter level requirement: ")
    level = numeric_validation(entry)
    skill["level"] = int(level)

    write_json("skills.json", skills)


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
    while True:
        print("classes, items, shops, locations, enemies, saves, npcs, skills, progression, passives")
        entry = input("What would you like to edit? (q to exit to menu): ")
        if entry == "classes":
            while True:
                option = input("add or delete classes? (q to exit): ")
                if option == "add":
                    add_class()
                elif option == "delete":
                    delete_class()
                elif option == "q":
                    break
        if entry == "items":
            while True:
                option = input("add or delete items? (q to exit): ")
                if option == "add":
                    option_two = input("equipable or misc?: ")
                    if option_two == "equipable":
                        add_equipable()
                    elif option_two == "misc":
                        add_misc_item()
                    else:
                        print("Invalid input")
                elif option == "delete":
                    delete_item()
                elif option == "q":
                    break
        if entry == "shops":
            pass
        if entry == "locations":
            pass
        if entry == "locations":
            pass
        if entry == "saves":
            delete_save()
        if entry == "npcs":
            pass
        if entry == "skills":
            while True:
                option = input("add or delete skills? (q to exit): ")
                if option == "add":
                    add_skill()
                elif option == "delete":
                    delete_skill()
                elif option == "q":
                    break
        if entry == "progression":
            pass
        if entry == "passives":
            pass
        elif entry == "q":
            break

