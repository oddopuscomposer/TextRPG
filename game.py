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
                character["health"] = class_data["classes"][cls]["start_health"]
                character["mana"] = class_data["classes"][cls]["start_mana"]
                character["max_health"] = class_data["classes"][cls]["start_health"]
                character["max_mana"] = class_data["classes"][cls]["start_mana"]
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
        print("stats, inv, goto, shop, encounter")
        selection = input("Select an option: ")
        if selection == "stats":
            show_stats(character)
        elif selection == "inv":
            manage_equipment(character)
        elif selection == "goto":
            pass
        elif selection == "shop":
            pass
        elif selection == "encounter":
            pass
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
    print("max health: " + str(character["max_health"]))
    print("health: " + str(character["health"]))
    print("max mana: " + str(character["max_mana"]))
    print("mana: " + str(character["mana"]))
    print("att: " + str(character["stats"]["att"]))
    print("def: " + str(character["stats"]["def"]))
    print("evd: " + str(character["stats"]["evd"]))
    print("exp: " + str(character["exp"]))
    print("next level: " + str(character["exp_req"]))
    print("training points: " + str(character["training_points"]))
    print("skills: " + str(character["skills"]))
    print("location: " + character["location"])
    print("#######################")


def show_inventory(character):
    """
    Prints equipment and inventory
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
    inventory = ''.join(character["inventory"])
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
    mana_sum = 0
    if character["equipment"][slot] != "empty":                         # if an item was just added
        att_sum += items["equipment"][equip]["buffs"]["att"]
        def_sum += items["equipment"][equip]["buffs"]["def"]
        evd_sum += items["equipment"][equip]["buffs"]["evd"]
        hp_sum += items["equipment"][equip]["buffs"]["hp"]
        mana_sum += items["equipment"][equip]["buffs"]["mana"]
    else:                                                               # if an item was just removed
        att_sum -= items["equipment"][equip]["buffs"]["att"]
        def_sum -= items["equipment"][equip]["buffs"]["def"]
        evd_sum -= items["equipment"][equip]["buffs"]["evd"]
        hp_sum -= items["equipment"][equip]["buffs"]["hp"]
        mana_sum -= items["equipment"][equip]["buffs"]["mana"]

    character["stats"]["att"] = character["stats"]["att"] + att_sum
    character["stats"]["def"] = character["stats"]["def"] + def_sum
    character["stats"]["evd"] = character["stats"]["evd"] + evd_sum
    character["max_hp"] = character["max_hp"] + hp_sum
    character["max_mana"] = character["max_mana"] + mana_sum


def manage_equipment(character):
    """
    Manage character equipment (Equip and Dequip)
    :param character:
    :return:
    """
    items = process_json("items.json")
    while True:
        show_inventory(character)
        entry = input("equip [item],dequip [slot], q to quit: ")
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
    if location in locations:
        if locations[location]:
            character["health"] = character["max_health"]
            character["mana"] = character["max_mana"]
            print("You are well rested.")
        else:
            print("You cant rest in this location.")


def go_to(character):
    """
    Travel to a location
    :param character:
    :return:
    """
    pass


def shop(character):
    """
    Buy or Sell from Shop at Location if it exists
    :param character:
    :return:
    """
    pass

