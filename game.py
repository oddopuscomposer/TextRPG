from game_utilities import process_json, write_json


def launch(setting):
    """
    Launches the game and loads save data
    :param type:
    :return:
    """
    player_data = process_json("saves.json")
    class_data = process_json("classes.json")

    saves = player_data["xref"]

    if setting == "saves":
        print(saves)
        save = input("Choose a save data: ")
        character = player_data["saves"][save]
    if setting == "new":
        character = player_data["saves"]["start_template"].copy()
        choose_status = False
        while not choose_status:
            name = input("What is your name?: ")
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

    start_game(character)
    print(character)


def start_game(character):
    """
    game loop
    :param character:
    :return:
    """
    game_status = True
    print("Welcome to the game!")
    print(character)
    while game_status:
        print("goto, shop, stats, rest")
        selection = input("Select an option: ")
        if selection == "stats":
            show_stats(character)


def show_stats(character):
    """
    Shows character stats/current save
    :return:
    """
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
    print("skills: " + character["skills"])
    print("location: " + character["location"])






def rest():
    pass


def go_to():
    pass


def shop():
    pass

