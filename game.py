from game_utilities import process_json, write_json, remove_prefix


def launch(setting):
    """
    Launches the game or loads save data
    :param setting:
    :return:
    """
    player_data = process_json("saves.json")
    class_data = process_json("classes.json")

    saves = player_data["xref"]
    character = ""
    name = ""

    if setting == "saves":
        print(saves)
        save = input("Choose a save data(quit to exit): ")
        while True:
            if save in saves:
                character = player_data["saves"][save]
                name = character["name"]
                break
            elif save == "exit":
                print("")
                break
            else:
                print("save not found, try again or exit")
                save = input("Choose a save data(quit to exit): ")
    if setting == "new":
        character = player_data["saves"]["start_template"].copy()
        choose_status = False
        while not choose_status:
            name = input("What is your name?: ")
            if name == "start_template" or name in saves:
                break
            player_data["saves"][name] = character
            character = player_data["saves"][name]
            character["name"] = name
            print(class_data["xref"])
            cls = input("Choose your class: ")
            if cls in class_data["xref"]:
                character["class"] = cls
                character["hp"] = class_data["classes"][cls]["start_hp"]
                character["mp"] = class_data["classes"][cls]["start_mp"]
                character["max_hp"] = class_data["classes"][cls]["start_hp"]
                character["max_mp"] = class_data["classes"][cls]["start_mp"]
                choose_status = True
            else:
                print("Class doesnt exist")

    if setting == "saves":
        start_game(character)
    if name == "start_template" or name == "" or name in saves:
        print("Error: Can't use start_template, empty string as name of save, or Save file already exists")
        print("")
    else:
        if character["name"] != "example":
            player_data["xref"].append(character["name"])
            write_json("saves.json", player_data)
            start_game(character)


def start_game(character):
    """
    game loop
    :param character:
    :return:
    """
    game_status = True
    print("Welcome to the game!")
    print(character)
    savefile = process_json("saves.json")
    while game_status:
        print("#######################")
        print("")
        print("stats, inv, rest, goto, shop, encounter")
        selection = input("Select an option: ")
        if selection == "stats":
            show_stats(character)
        elif selection == "inv":
            manage_equipment(character)
        elif selection == "goto":
            go_to(character)
        elif selection == "rest":
            rest(character)
        elif selection == "shop":
            shop(character)
        elif selection == "encounter":
            encounter(character)
        else:
            print("Incorrect action, please try again")
        savefile["saves"][character["name"]] = character
        write_json("saves.json", savefile)


def show_stats(character):
    """
    Shows character stats/current save
    :return:
    """
    print("STATS")
    print("#######################")
    print("name: " + character["name"])
    print("level: " + str(character["level"]))
    print("class: " + character["class"])
    print("max hp: " + str(character["max_hp"]))
    print("hp: " + str(character["hp"]))
    print("max mp: " + str(character["max_mp"]))
    print("mp: " + str(character["mp"]))
    print("att: " + str(character["stats"]["att"]))
    print("def: " + str(character["stats"]["def"]))
    print("evd: " + str(character["stats"]["evd"]))
    print("exp: " + str(character["exp"]))
    print("next level: " + str(character["exp_req"]))
    print("training points: " + str(character["training_points"]))
    print("skills: " + str(character["skills"]))
    print("gold: " + str(character["gold"]))
    print("location: " + character["location"])
    print("#######################")


def show_inventory(character):
    """
    Prints equipment and inventory // Helper method for manage equipment
    :param character:
    :return:
    """
    print("Equipment")
    print("#######################")
    print("head: " + character["equipment"]["head"])
    print("chest: " + character["equipment"]["chest"])
    print("legs: " + character["equipment"]["legs"])
    print("feet: " + character["equipment"]["feet"])
    print("left_hand: " + character["equipment"]["left_hand"])
    print("right_hand: " + character["equipment"]["right_hand"])
    print("necklace: " + character["equipment"]["necklace"])
    print("ring: " + character["equipment"]["ring"])
    print("#######################")
    print("Inventory")
    print("#######################")
    inventory = ', '.join(character["inventory"])
    if len(inventory) > 0:
        print(inventory)
    else:
        print("none")


def update_stats(character, equip):
    """
    Update stats from equipment
    :return:
    """
    items = process_json("items.json")
    slot = items["equipment"][equip]["slot"]

    att_sum = 0
    def_sum = 0
    evd_sum = 0
    hp_sum = 0
    mp_sum = 0

    if character["equipment"][slot] != "empty":                         # if an item was just added
        att_sum += items["equipment"][equip]["buffs"]["att"]
        def_sum += items["equipment"][equip]["buffs"]["def"]
        evd_sum += items["equipment"][equip]["buffs"]["evd"]
        hp_sum += items["equipment"][equip]["buffs"]["hp"]
        mp_sum += items["equipment"][equip]["buffs"]["mp"]
    else:                                                               # if an item was just removed
        att_sum -= items["equipment"][equip]["buffs"]["att"]
        def_sum -= items["equipment"][equip]["buffs"]["def"]
        evd_sum -= items["equipment"][equip]["buffs"]["evd"]
        hp_sum -= items["equipment"][equip]["buffs"]["hp"]
        mp_sum -= items["equipment"][equip]["buffs"]["mp"]

    character["stats"]["att"] = character["stats"]["att"] + att_sum
    character["stats"]["def"] = character["stats"]["def"] + def_sum
    character["stats"]["evd"] = character["stats"]["evd"] + evd_sum
    character["max_hp"] = character["max_hp"] + hp_sum
    character["max_mp"] = character["max_mp"] + mp_sum

    if character["hp"] > character["max_hp"]:
        character["hp"] = character["max_hp"]

    if character["mp"] > character["max_mp"]:
        character["mp"] = character["max_mp"]


def manage_equipment(character):
    """
    Manage character equipment (Equip and Dequip)
    :param character:
    :return:
    """
    items = process_json("items.json")
    while True:
        show_inventory(character)
        entry = input("equip [item],dequip [slot], look [item], q to quit: ")
        if entry.startswith("equip"):
            item = remove_prefix(entry, "equip ")
            if item in items["equipment"]:
                if character["class"] or "any" in items["equipment"][item]["classes"]:
                    slot = items["equipment"][item]["slot"]
                    character["equipment"][slot] = item
                    character["inventory"].remove(item)
                    update_stats(character, item)
                    print("Equiped " + item)
                else:
                    print("Your class can't equip " + item + " or item not in inventory")
            else:
                print("The item is unequipable")
        elif entry.startswith("dequip"):
            slot = remove_prefix(entry, "dequip ")
            if slot in ["head", "chest", "legs", "feet", "left_hand", "right_hand", "necklace", "ring"]:
                if character["equipment"][slot] != "empty":
                    item = character["equipment"][slot]
                    character["equipment"][slot] = "empty"
                    character["inventory"].append(item)
                    update_stats(character, item)
                    print("Dequiped " + item)
                else:
                    print("Your slot is empty")
            else:
                print("Invalid slot")
        elif entry.startswith("look"):
            look = remove_prefix(entry, "look ")
            if look in character["inventory"]:
                for key in items["equipment"][look]:
                    print(key + ": " + str(items["equipment"][look][key]))
                exit = input("press anything to go back to inventory: ")
            else:
                print("Invalid Item")
        elif entry == "q":
            break
        else:
            print("Invalid input, try again")


def rest(character):
    """
    Heal character for health/mana
    :return:
    """
    locations = process_json("locations.json")
    location = character["location"]
    if location in locations["xref"]:
        if locations["locations"][location]:
            character["hp"] = character["max_hp"]
            character["mp"] = character["max_mp"]
            print("You are well rested.")
            print("+" + str(character["max_hp"] - character["hp"]) + " hp")
            print("+" + str(character["max_mp"] - character["mp"]) + " mp")

        else:
            print("You cant rest in this location.")


def go_to(character):
    """
    Travel to an adjacent location
    :param character:
    :return:
    """
    locations = process_json("locations.json")
    old_location = character["location"]
    loc_list = locations["locations"][old_location]["adjacent"]
    while True:
        print(loc_list)
        new_location = input("Choose a location (q to quit): ")
        if new_location in loc_list:
            if old_location in locations["locations"][new_location]["adjacent"]:
                character["location"] = new_location
                print("You are now in " + new_location)
                break
            else:
                print("This area is one way")
        elif new_location == "q":
            break
        else:
            print("Invalid location, please try again")


def shop(character):
    """
    Buy or Sell from Shop at Location if it exists
    :param character:
    :return:
    """
    shops = process_json("shops.json")
    locations = process_json("locations.json")
    location = character["location"]
    if not locations["locations"][location]["shops"]:
        print("There are no shops in this area")
    else:
        while True:
            print(locations["locations"][location]["shops"])
            store = input("Select a shop (q to quit): ")
            if store in locations["locations"][location]["shops"] and store in shops["xref"]:  # Shop loop
                shop_interaction(character, shops, store)
            elif store == "q":
                break
            else:
                print("Invalid Shop Name")


def shop_interaction(character, shops, store):
    """
    Helper method for shop // handles interaction with shop keeper
    :return:
    """
    items = process_json("items.json")
    print(shops["shops"][store]["npc"])
    print(shops["shops"][store]["inventory"])
    for item in shops["shops"][store]["inventory"]:
        match = items["equipment"][item]
        price = match["buy_price"]
        rarity = match["rarity"]
        classes = match["classes"]
        slot = match["slot"]
        damage = match["damage"]
        buffs = match["buffs"]

        print(item)
        print("price: " + str(price))
        print("rarity: " + rarity)
        print("classes: " + str(classes))
        print("slot: " + slot)
        print("damage: " + str(damage))
        for k in buffs:
            print(k + ": " + str(buffs[k]))
        print("----------------------------------------")

        while True:
            entry = input("What would you like to purchase? (q to quit): ")
            if entry in shops["shops"][store]["inventory"]:
                while True:
                    cost = items["equipment"][entry]["buy_price"]
                    resp = input("Would you like to buy " + entry + " for " + str(cost) + "? (y/n): ")
                    if resp == "y":
                        if character["gold"] > cost:
                            character["gold"] -= cost
                            character["inventory"].append(entry)
                            print("Item purchased for " + str(cost) + " gold")
                        else:
                            print("You dont have enough gold")
                        break
                    elif resp == "n":
                        break
                    else:
                        print("Invalid response")
                break
            elif entry == "q":
                break
            else:
                print("Item not in shop's inventory or does not exist")


def encounter(character):
    """
    Encounter an enemy
    :param character:
    :return:
    """
    pass

