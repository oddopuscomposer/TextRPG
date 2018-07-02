from game_utilities import process_json, write_json, remove_prefix


def launch(setting):
    """
    Launches the game and loads save data
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
            if save in player_data["saves"]:
                character = player_data["saves"][save]
                break
            elif save == "exit":
                print("Relaunch game to return to title screen")
            else:
                print("save not found, try again or exit")
    if setting == "new":
        character = player_data["saves"]["start_template"].copy()
        choose_status = False
        while not choose_status:
            name = input("What is your name?: ")
            if name == "start_template":
                break
            player_data["saves"][name] = character
            character = player_data["saves"][name]
            character["name"] = name
            print(class_data["xref"])
            cls = input("Choose your class: ")
            if cls in class_data["xref"]:
                character["class"] = cls
                character["health"] = class_data["classes"][cls]["health"]
                character["mana"] = class_data["classes"][cls]["mana"]
                choose_status = True
            else:
                print("Class doesnt exist")
        player_data["xref"].append(character["name"])
        write_json("saves.json", player_data)

    if name != "start_template":
        start_game(character)
    else:
        print("Error: Can't use start_template as name of save, restart game and try again")


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
    print("level: " + character["level"])
    print("class: " + character["class"])
    print("health: " + character["health"])
    print("mana: " + character["mana"])
    print("att: " + character["stats"]["att"])
    print("def: " + character["stats"]["def"])
    print("evd: " + character["stats"]["evd"])
    print("exp: " + character["stats"]["exp"])
    print("next level: " + character["stats"]["exp_req"])
    print("training points: " + character["training_points"])
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
                if character["class"] in items["equipment"][item]["classes"]:
                    slot = items["equipment"][item]["slot"]
                    character["equipment"][slot] = item
                    character["inventory"].remove(item)
                    print("Equiped " + item)
                else:
                    print("Your class can't equip " + item + " or item not in inventory")
            else:
                print("The item is unequipable")
        elif entry.startswith("dequip"):
            slot = remove_prefix(entry, "dequip ")
            if character["equipment"][slot] != "empty":
                item = character["equipment"][slot]
                character["equipment"][slot] = "empty"
                character["inventory"].append(item)
                print("Dequiped " + item)
            else:
                print("Your slot is empty")
        elif entry == "q":
            break
        else:
            print("Invalid input, try again")




def rest():
    """
    Heal
    :return:
    """
    pass


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

