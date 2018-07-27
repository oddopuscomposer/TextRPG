from battle import *


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
        print("Saves: ")
        for item in saves:
            print("     - " + item)
        save = input("Choose a save data: ")
        while True:
            if save in saves:
                character = player_data["saves"][save]
                name = character["name"]
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

            classes = []
            for item in class_data["xref"]:
                if item != "Any":
                    classes.append(item)
            print(classes)
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
        #print("Error: Can't use start_template, empty string as name of save, or Save file already exists")
        print("Error")
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
    # print(character)
    save_file = process_json("saves.json")
    while game_status:
        print("#######################")
        print("1. Stats")
        print("2. Inventory")
        print("3. Rest")
        print("4. Travel")
        print("5. Shop")
        print("6. Encounter")
        print("7. Quit")
        print("#######################")
        selection = input("Select an option: ").lower()
        if selection.startswith("sta") or selection == "1":
            show_stats(character)
        elif selection.startswith("inv") or selection == "2":
            manage_equipment(character)
        elif selection.startswith("res") or selection == "3":
            rest(character)
        elif selection.startswith("trav") or selection.startswith("goto") or selection == "4":
            go_to(character)
        elif selection.startswith("sho") or selection == "5":
            shop(character)
        elif selection.startswith("enc") or selection == "6":
            encounter(character)
        elif selection.startswith("qui") or selection == "7":
            break
        else:
            print("Unrecognized Action. Please try again!")
        save_file["saves"][character["name"]] = character
        write_json("saves.json", save_file)


def show_stats(character):
    """
    Shows character stats/current save
    :return:
    """
    print("Stats:")
    print("#######################")
    print("Name: " + character["name"])
    print("Level: " + str(character["level"]))
    print("Class: " + character["class"])
    print("Deaths: " + str(character["deaths"]))
    print("HP: " + str(character["hp"]) + "/" + str(character["max_hp"]))
    print("MP: " + str(character["mp"]) + "/" + str(character["max_mp"]))
    print("Attack: " + str(character["stats"]["att"]))
    print("Defense: " + str(character["stats"]["def"]))
    print("Evasion: " + str(character["stats"]["evd"]))
    print("Critical: " + str(character["stats"]["crt"]))
    print("Exp: " + str(character["exp"]))
    print("Next Level: " + str(character["exp_req"]))
    print("Training Points: " + str(character["training_points"]))
    print("Skills: " + str(character["skills"]))
    print("Gold: " + str(character["gold"]))
    print("Location: " + character["location"])
    print("#######################")


def show_inventory(character):
    """
    Prints equipment and inventory // Helper method for manage equipment
    :param character:
    :return:
    """
    print("")
    print("#######################")
    print("Equipment")
    print("#######################")
    for k, v in character["equipment"].items():
        if v != "empty":
            print("- " + v)

    print("")
    print("#######################")
    print("Inventory")
    print("#######################")
    item_list = []
    if len(character["inventory"]) > 0:
        for item in character["inventory"]:
            item_list.append(item)
            if len(item_list) == 3:
                print('     '.join(item_list))
                item_list = []
        if len(item_list) > 0:
            print('     '.join(item_list))
    else:
        print("Your inventory is empty. :<")
    print("")


def update_stats(character, equip):
    """
    Update stats from equipment
    :return:
    """
    items = process_json("items.json")
    slot = items["items"][equip]["slot"]

    att_sum = 0
    def_sum = 0
    evd_sum = 0
    hp_sum = 0
    mp_sum = 0
    crt_sum = 0

    if character["equipment"][slot] != "empty":                         # if an item was just added
        att_sum += items["items"][equip]["buffs"]["att"]
        def_sum += items["items"][equip]["buffs"]["def"]
        evd_sum += items["items"][equip]["buffs"]["evd"]
        hp_sum += items["items"][equip]["buffs"]["hp"]
        mp_sum += items["items"][equip]["buffs"]["mp"]
        crt_sum += items["items"][equip]["buffs"]["crt"]
    else:                                                               # if an item was just removed
        att_sum -= items["items"][equip]["buffs"]["att"]
        def_sum -= items["items"][equip]["buffs"]["def"]
        evd_sum -= items["items"][equip]["buffs"]["evd"]
        hp_sum -= items["items"][equip]["buffs"]["hp"]
        mp_sum -= items["items"][equip]["buffs"]["mp"]
        crt_sum -= items["items"][equip]["buffs"]["crt"]

    character["stats"]["att"] = character["stats"]["att"] + att_sum
    character["stats"]["def"] = character["stats"]["def"] + def_sum
    character["stats"]["evd"] = character["stats"]["evd"] + evd_sum
    character["stats"]["crt"] = character["stats"]["crt"] + crt_sum
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
            if item in items["items"]:
                if items["items"][item]["type"] == "equipment":
                    if character["class"] or "any" in items["items"][item]["classes"]:
                        slot = items["items"][item]["slot"]
                        character["equipment"][slot] = item
                        character["inventory"].remove(item)
                        update_stats(character, item)
                        print("Equipped " + item)
                    else:
                        print("Your class can't equip this " + item)
                else:
                    print("This item can not be equipped.")
            else:
                print("This item does not exist.")
        elif entry.startswith("dequip"):
            dequip = "fail"
            item = remove_prefix(entry, "dequip ")
            if item in items["items"]:
                for slot in character["equipment"]:
                    if character["equipment"][slot] == item:
                        character["equipment"][slot] = "empty"
                        character["inventory"].append(item)
                        update_stats(character, item)
                        dequip = "success"
                        print("Dequiped " + item)
                if dequip == "fail":
                    print("You do not have that item equipped.")
            else:
                print("Item does not exist.")
        elif entry.startswith("look"):
            look = remove_prefix(entry, "look ")
            if look in character["inventory"]:
                if items["items"][look]["type"] == "equipment":
                    print("Name: " + look)
                    print("Description: " + items["items"][look]["description"])
                    print("Rarity: " + items["items"][look]["rarity"])
                    print("Buy Price: " + str(items["items"][look]["buy_price"]))
                    print("Sell Price: " + str(items["items"][look]["sell_price"]))
                    print("Type: " + items["items"][look]["type"])
                    print("Slot: " + items["items"][look]["slot"])
                    print("Required Classes: " + ', '.join(items["items"][look]["classes"]))
                    print("Properties: ")
                    print("     HP: +" + str(items["items"][look]["buffs"]["hp"]))
                    print("     MP: +" + str(items["items"][look]["buffs"]["mp"]))
                    print("     Attack: +" + str(items["items"][look]["buffs"]["att"]))
                    print("     Defense: +" + str(items["items"][look]["buffs"]["def"]))
                    print("     Evasion: +" + str(items["items"][look]["buffs"]["evd"]))
                    print("     Critical: +" + str(items["items"][look]["buffs"]["crt"]))
                    input("press anything to go back to inventory: ")
                if items["items"][look]["type"] == "misc":
                    print("Name: " + look)
                    print("Description: " + items["items"][look]["description"])
                    print("Rarity: " + items["items"][look]["rarity"])
                    print("Buy Price: " + str(items["items"][look]["buy_price"]))
                    print("Sell Price: " + str(items["items"][look]["sell_price"]))
                    print("Type: " + items["items"][look]["type"])
                    input("press anything to go back to inventory: ")
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
            print("You feel well rested.")
            print("+" + str(character["max_hp"] - character["hp"]) + " hp")
            print("+" + str(character["max_mp"] - character["mp"]) + " mp")
            character["hp"] = character["max_hp"]
            character["mp"] = character["max_mp"]

        else:
            print("You can't rest in this location.")


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
        print(', '.join(loc_list))
        new_location = input("Choose a location (q to quit): ")
        for loc in loc_list:
            if loc.startswith(new_location):
                new_location = loc
                break

        if new_location in loc_list:
            if old_location in locations["locations"][new_location]["adjacent"]:
                character["location"] = new_location
                print("You are now in " + new_location)
                break
            else:
                print("You can not go back the same way!")
                while True:
                    cont = input("Continue?(y/n): ")
                    if cont == "y":
                        character["location"] = new_location
                        print("You are now in " + new_location)
                        break
                    elif cont == "n":
                        break
                    else:
                        print("Invalid option!")
                    break
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
            print(', '.join(locations["locations"][location]["shops"]))
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
    while True:
        option = input("buy(b) or sell(s)? (q for quit): ")
        if option == "b" or option == "buy":
            if len(shops["shops"][store]["inventory"]) != 0:
                print("Inventory: ")
            else:
                print("There is nothing in this shop!")
            count = 0
            for item in shops["shops"][store]["inventory"]:
                count += 1
                print(str(count) + ". " + item)
            print("")
            while True:
                entry = input("What are you interested in buying? (q to quit): ")
                if entry == "q":
                    break
                try:
                    entry = int(entry)
                    if entry <= len(shops["shops"][store]["inventory"]):
                        entry = shops["shops"][store]["inventory"][entry-1]
                        print(entry)
                except ValueError:
                    for item in shops["shops"][store]["inventory"]:
                        if item.startswith(entry):
                            entry = item

                if entry in shops["shops"][store]["inventory"]:
                    while True:
                        match = items["items"][item]
                        price = match["buy_price"]
                        rarity = match["rarity"]
                        if match["type"] == "equipment":
                            classes = match["classes"]
                            slot = match["slot"]
                            damage = match["damage"]
                            buffs = match["buffs"]
                        print("----------------------------------------")
                        print(item)
                        print("price: " + str(price))
                        print("rarity: " + rarity)
                        if match["type"] == "equipment":
                            print("classes: " + str(', '.join(classes)))
                            print("slot: " + slot)
                            print("damage: " + str(damage))
                            for k in buffs:
                                print(k + ": " + str(buffs[k]))
                        print("----------------------------------------")
                        cost = items["items"][entry]["buy_price"]
                        while True:
                            number = input("How many " + entry + " would you like to buy?: ")
                            try:
                                int(number)
                                break
                            except ValueError:
                                print("Please input a number!")
                        price = int(number) * cost
                        if price > character["gold"]:
                            print("You do not have enough gold!")
                        else:
                            if int(number) == 1:
                                resp = input("Would you like to buy " + entry + " for " + str(price) + "? (y/n): ")
                            elif int(number) == 0:
                                break
                            else:
                                resp = input("Would you like to buy " + str(number) + " " + entry + " for " + str(price) + "? (y/n): ")
                            if resp == "y":
                                if character["gold"] > price:
                                    character["gold"] -= price
                                    for x in range(int(number)-1):
                                        character["inventory"].append(entry)
                                    print(str(number) + " " + entry + " purchased for " + str(price) + " gold")
                                else:
                                    print("You do not have enough gold")
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
        elif option == "s" or option == "sell":
            show_inventory(character)
            while True:
                sell = input("What would you like to sell? (q to quit): ")
                for item in character["inventory"]:
                    if item.startswith(sell):
                        sell = item
                        break

                if sell in character["inventory"]:
                    print("You have " + str(character["inventory"].count(sell)) + " " + sell + " in your inventory.")
                    while True:
                        number = input("How many would you like to sell?: ")
                        try:
                            int(number)
                            break
                        except ValueError:
                            print("Please input a number!")
                    if int(number) <= character["inventory"].count(sell):
                        price = items["items"][sell]["sell_price"]
                        price = price * int(number)
                        if number == 1:
                            confirm = input("Are you sure you want to sell " + sell + " for " + str(
                                price) + " gold? (y/n): ")
                        elif number == 0:
                            break
                        else:
                            confirm = input("Are you sure you want to sell " + str(number) + " " + sell + " for " + str(price) + " gold? (y/n): ")
                        if confirm == "y":
                            for x in range(int(number)-1):
                                character["inventory"].remove(sell)
                            character["gold"] += price
                            print(str(number) + " " + sell + " sold for " + str(price) + " gold")
                        elif confirm == "n":
                            break
                        else:
                            print("Invalid input")
                    else:
                        print("You do not have that many " + sell + " in your inventory.")
                elif sell == "q":
                    break
                else:
                    print("You do not have " + sell + " in your inventory.")

        elif option == "q":
            break
        else:
            print("Invalid selection")


def encounter(character):
    """
    Encounter an enemy
    :param character:
    :return:
    """
    location = character["location"]
    locations = process_json("locations.json")
    enemies = process_json("enemies.json")

    curr_location = locations["locations"][location]
    location_enemies = list(curr_location["enemies"].keys())
    location_rates = list(curr_location["enemies"].values())

    max_rate = 0
    for item in location_rates:
        max_rate += item

    if max_rate != 1 and max_rate > 0:
        none_rate = 1 - max_rate
        location_rates.append(none_rate)
        location_enemies.append("none")

    if len(location_enemies) > 0:
        print("You look around for enemies...")
        choice = numpy.random.choice(location_enemies, 1, location_rates)
        if choice[0] != "none":
            print("###########################")
            print("##########BATTLE###########")
            print("###########################")
            print(choice[0] + " wants to fight")
            enemy = enemies["enemies"][choice[0]]
            battle(character, enemy)
        else:
            print("No enemies found")
    else:
        print("There are no enemies in this area.")
