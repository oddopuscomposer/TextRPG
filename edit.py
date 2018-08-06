from game_utilities import *


def delete_save():
    """
    Removes save from saves.json
    :return:
    """
    saves = process_json("saves.json")
    print("Saves: " + ', '.join(list(saves["saves"].keys())))
    while True:
        print("Warning: deleting save template breaks new characters")
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
    classes = process_json("classes.json")
    print("Please do not remove Any from the game if you care about items that cater to all classes.")
    print(', '.join(classes["xref"]))
    entry = input("Please enter a class to delete: ")

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
    print("For example: Enter required classes([class1],[class2]): Archer,Knight,Any")
    cls = input("Enter required classes([class1],[class2]): ")
    words = cls.split(",")
    words = class_validation(words)
    item["classes"] = words

    print(["head", "chest", "legs", "feet", "left hand", "right hand", "necklace", "ring"])
    entry = input("Enter a slot/slots([slot1],[slot2]): ")
    entry = entry.split(",")
    slot = array_validation(entry, ["head", "chest", "legs", "feet", "left hand", "right hand", "necklace", "ring"])
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

    items["xref"].append(name)
    write_json("items.json", items)
    print("Item created and saved")


def delete_item():
    """
    Removes equipable from items.json
    :return:
    """
    items = process_json("items.json")
    print("Options: ")
    print(', '.join(list(items["items"].keys())))
    entry = input("Please enter an item to delete: ")

    if entry in items["items"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                del items["items"][entry]
                items["xref"].remove(entry)
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

    items["xref"].append(name)
    write_json("items.json", items)


def add_skill():
    """
    Adds skill to skills.json
    :return:
    """
    skills = process_json("skills.json")

    name = input("Enter skill name: ")
    try:
        skills["skills"][name]
        while True:
            choice = input("This skill already exists, do you want to overwrite? (y/n): ")
            if choice == "y":
                break
            elif choice == "n":
                return "null"
            else:
                print("Invalid input")
    except KeyError:
        pass

    skills["skills"][name] = {}
    skill = skills["skills"][name]

    skill_type = input("What kind of skill? (field or battle): ")

    if skill_type == "battle":
        skill["type"] = "battle"
        entry = input("Enter damage: ")
        dmg = numeric_validation(entry)
        skill["dmg"] = int(dmg)


    entry = input("Enter mana cost: ")
    mana = numeric_validation(entry)
    skill["mana"] = int(mana)

    print("Options: ")
    print(','.join(process_json("classes.json")["xref"]))
    print("For example: Enter required classes([class1],[class2]): Archer,Knight,Any")
    entry = input("Enter class requirement([class1],[class2]): ")
    entry = entry.split(",")
    words = class_validation(entry)
    skill["class"] = words

    entry = input("Enter level requirement: ")
    level = numeric_validation(entry)
    skill["level"] = int(level)

    entry = input("")

    write_json("skills.json", skills)


def delete_skill():
    """
    Removes skill from skills.json
    :return:
    """
    skills = process_json("skills.json")
    print("Options: ")
    print(', '.join(list(skills["skills"].keys())))
    entry = input("Please enter a skill to delete: ")

    if entry in skills["skills"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                del skills["skills"][entry]
                print("skill deleted")
                break
            elif confirm == "n":
                break
            else:
                pass
    else:
        print("entry is not in skills")

    write_json("skills.json", skills)


def add_location():
    """
    Adds location to locations.json
    :return:
    """
    locations = process_json("locations.json")
    shops = process_json("shops.json")

    name = input("Enter location name: ")
    try:
        locations["location"][name]
        while True:
            choice = input("This location already exists, do you want to overwrite? (y/n): ")
            if choice == "y":
                break
            elif choice == "n":
                return "null"
            else:
                print("Invalid input")
    except KeyError:
        pass

    locations["locations"][name] = {}
    location = locations["locations"][name]

    print("Options: ")
    print(','.join(process_json("shops.json")["xref"]))
    entry = input("What shops are in this location? ([shop1], [shop2]): ")
    if entry != "":
        entry = entry.split(",")
        entry = array_validation(entry, process_json("shops.json")["xref"])
        for shop in entry:
            shops["shops"][shop]["location"] = name

    else:
        entry = []

    location["shops"] = entry

    location["npcs"] = []

    while True:
        entry = input("Can you rest in this area? (y/n)")
        if entry == "y":
            entry = True
            break
        elif entry == "n":
            entry = False
            break
        else:
            print("Invalid input")

    location["rest"] = entry

    print("Options: ")
    print(','.join(locations["xref"]))
    entry = input("What locations are adjacent to this one? ([location1],[location2]): ")
    entry = entry.split(",")
    entry = array_validation(entry, locations["xref"])
    for loc in entry:
        locations["locations"][loc]["adjacent"].append(name)
    location["adjacent"] = entry

    print("Options: ")
    print('.'.join(process_json("enemies.json")["xref"]))
    entry = input("What enemies are here? ([enemy1],[enemy2]): ")
    entry = entry.split(",")
    entry = array_validation(entry, process_json("enemies.json")["xref"])
    print("Enemies: ")
    print(','.join(entry))
    print("Spawn rate is defined as a value 0-1 in decimal form")
    probs = input("What probabilities do these enemies have of appearing in this location? ([prob1],[prob2])")
    probs = probs.split(",")

    if len(probs) == len(entry):
        enemydict = {}
        print(entry)
        print(probs)
        for enemy, prob in zip(entry, probs):
            enemydict[enemy] = float(prob)

    location["enemies"] = enemydict

    locations["xref"].append(name)

    write_json("shops.json", shops)
    write_json("locations.json", locations)


def delete_location():
    """
    Removes location from locations.json
    :return:
    """
    locations = process_json("locations.json")
    print("Options: ")
    print(','.join(list(locations["locations"].keys())))
    entry = input("Please enter a location to delete: ")

    if entry in locations["locations"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                del locations["locations"][entry]
                locations["xref"].remove(entry)
                for loc in locations["locations"]:
                    if entry in locations["locations"][loc]["adjacent"]:
                        locations["locations"][loc]["adjacent"].remove(entry)

                print("Location deleted")
                break
            elif confirm == "n":
                break
            else:
                pass
    else:
        print("entry is not in locations")

    write_json("locations.json", locations)


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

    enemies = process_json("enemies.json")

    name = input("What is the enemy's name?: ")

    try:
        enemies["enemies"][name]
        while True:
            choice = input("This enemy already exists, do you want to overwrite? (y/n): ")
            if choice == "y":
                break
            elif choice == "n":
                return "null"
            else:
                print("Invalid input")
    except KeyError:
        pass

    enemies["enemies"][name] = {}
    enemy = enemies["enemies"][name]
    enemy["name"] = name

    entry = input("What is the enemy's level?: ")
    entry = numeric_validation(entry)
    enemy["level"] = int(entry)

    entry = input("What is the enemy's hp?: ")
    entry = numeric_validation(entry)
    enemy["hp"] = int(entry)

    entry = input("What are the enemy's attacks?([int1],[int2]): ")
    entry = entry.split(",")
    entry = numeric_array_validation_at_least_one(entry)
    enemy["attack"] = entry

    entry = input("What are the enemy's defends?([int1],[int2]): ")
    if entry == '':
        entry = []
    else:
        entry = entry.split(",")
    entry = numeric_array_validation_at_least_one(entry)
    enemy["defend"] = entry

    entry = input("What is the enemy's evasion?: ")
    entry = numeric_validation(entry)
    enemy["evd"] = entry

    print("Options: ")
    print(','.join(process_json("items.json")["xref"]))
    entry = input("What are the enemy's drops? ([item1]:[prob1],[item2]:[prob2]): ")
    entry = entry.split(",")
    entry = enemy_drop_validation(entry)
    enemy["drops"] = entry

    entry = input("What is the enemy's gold drop?: ")
    entry = numeric_validation(entry)
    enemy["gold"] = entry

    entry = input("What is the enemy's exp drop?: ")
    entry = numeric_validation(entry)
    enemy["exp"] = entry

    print("Enemy added")
    enemies["xref"].append(name)
    write_json("enemies.json", enemies)


def delete_enemy():
    """
    Removes enemy from enemies.json
    :return:
    """
    enemies = process_json("enemies.json")
    print("Options: ")
    print(', '.join(list(enemies["enemies"].keys())))
    entry = input("Please enter an enemy to delete: ")

    if entry in enemies["enemies"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                del enemies["enemies"][entry]
                enemies["xref"].remove(entry)
                print("enemy deleted")
                break
            elif confirm == "n":
                break
            else:
                pass
    else:
        print("entry is not in enemies")

    write_json("enemies.json", enemies)


def add_shop():
    """
    Adds shop to shops.json // [shops] [xref] locations[location][shops]
    :return:
    """
    shops = process_json("shops.json")
    locations = process_json("locations.json")

    name = input("Enter shop name: ")
    try:
        shops["location"][name]
        while True:
            choice = input("This shop already exists, do you want to overwrite? (y/n): ")
            if choice == "y":
                break
            elif choice == "n":
                return "null"
            else:
                print("Invalid input")
    except KeyError:
        pass

    shops["shops"][name] = {}
    shop = shops["shops"][name]
    shop["name"] = name

    print("Options: ")
    print(','.join(process_json("items.json")["xref"]))
    entry = input("What items are sold in this shop? ([item1],[item2]): ")
    entry = entry.split(",")
    entry = array_validation(entry, process_json("items.json")["xref"])
    shop["inventory"] = entry

    entry = input("Who is the shopkeeper?: ")
    shop["npc"] = entry

    print("Options: ")
    print(','.join(process_json("locations.json")["xref"]))
    entry = input("Where is this shop located?: ")
    entry = array_validation(entry, process_json("locations.json")["xref"])
    locations["locations"][entry]["shops"].append(name)
    shop["location"] = entry

    print("Shop created")
    shops["xref"].append(name)
    write_json("locations.json", locations)
    write_json("shops.json", shops)


def delete_shop():
    """
    Removes shop from shops.json
    :return:
    """
    shops = process_json("shops.json")
    locations = process_json("locations.json")
    print("Options: ")
    print(', '.join(list(shops["shops"].keys())))
    entry = input("Please enter a shop to delete: ")

    if entry in shops["shops"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                if entry in locations["locations"][shops["shops"][entry]["location"]]["shops"]:
                    locations["locations"][shops["shops"][entry]["location"]]["shops"].remove(entry)
                del shops["shops"][entry]
                shops["xref"].remove(entry)
                print("shop deleted")
                break
            elif confirm == "n":
                break
            else:
                pass
    else:
        print("entry is not in shops")

    write_json("shops.json", shops)
    write_json("locations.json", locations)


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
            while True:
                option = input("add or delete shops? (q to exit): ")
                if option == "add":
                    add_shop()
                elif option == "delete":
                    delete_shop()
                elif option == "q":
                    break
        if entry == "locations":
            while True:
                option = input("add or delete locations? (q to exit): ")
                if option == "add":
                    add_location()
                elif option == "delete":
                    delete_location()
                elif option == "q":
                    break
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
        if entry == "enemies":
            while True:
                option = input("add or delete enemies? (q to exit): ")
                if option == "add":
                    add_enemy()
                elif option == "delete":
                    delete_enemy()
                elif option == "q":
                    break
        elif entry == "q":
            break

