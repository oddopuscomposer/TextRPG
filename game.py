import json
from game_utilities import process_json


def launch(setting):
    """
    Launches the game and loads save data
    :param type:
    :return:
    """
    player_data = process_json("saves.json")["saves"]
    class_data = process_json("classes.json")

    saves = []
    for key in player_data.keys():
        saves.append(key)

    if setting == "saves":
        print(saves)
        save = input("Choose a save data: ")
        character = player_data[save]
    if setting == "new":
        character = player_data["start_template"]
        choose_status = False
        while not choose_status:
            name = input("What is your name?: ")
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
                choose_status = False
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
    while game_status:
        print("goto, shop, stats, rest")
        selection = input("Select an option: ")

