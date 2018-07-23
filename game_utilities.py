import json
import numpy

# Validations and utilities for larger game methods

########################################################################################################################
# JSON & String Methods                                                                                                #
########################################################################################################################


def process_json(filename):
    """
    Processes the json to be read as a dictionary
    :param filename: JSON file
    :return:
    """
    json1_file = open("data/" + filename)
    json1_str = json1_file.read()
    return json.loads(json1_str)


def write_json(filename, data):
    """
    Writes the dictionary changes to the JSON file
    :param filename: JSON file
    :param data: dictionary
    :return:
    """
    with open('data/' + filename, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)


def remove_prefix(text, prefix):
    """
    Removes prefix from a string
    :param text:
    :param prefix:
    :return:
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def percentage_converter(fraction):
    return str(fraction * 100)

########################################################################################################################
# Validations                                                                                                          #
########################################################################################################################


def numeric_validation(entry):
    """
    Validates numeric inputs for entry
    :param entry: string
    :return: entry
    """
    while True:
        try:
            entry = int(entry)
            break
        except ValueError:
            entry = input("Please enter a valid integer: ")
    return entry


def rarity_validation(entry):
    """
    Validates rarity of equipables and items
    :param entry: string
    :return:
    """
    while True:
        if entry in ["common", "uncommon", "rare", "ancient", "legendary"]:
            break
        else:
            entry = input("Please enter a valid rarity: ")
    return entry


def class_validation(entry):
    """
    Validates classes
    :param entry: array
    :return:
    """
    classname = process_json("classes.json")
    while True:
        count = 0
        for item in entry:
            if item in classname["xref"]:
                count += 1
            else:
                break
            if count == len(entry):
                return entry

        entry = input("Please input a valid class/classes: ")
        entry = entry.split(",")


def slot_validation(entry):
    """
    Validates character slots
    :param entry: string
    :return:
    """
    slots = ["head", "chest", "legs", "feet", "left hand", "right hand", "necklace", "ring"]

    while True:
        count = 0
        for item in entry:
            if item in slots:
                count += 1
            else:
                break
            if count == len(entry):
                return entry

        entry = input("Please input a valid slot/slots: ")
        entry = entry.split(",")


def stat_validation(entry):
    """
    Validates proper integer array entry used for stats related methods
    :param entry: array
    :return:
    """
    while True:
        for item in entry:
            try:
                item = int(item)
            except ValueError:
                print("Please enter 6 integers separated by commas example: 10,23,12,34,54,22")
                entry = input("Enter buffs([att],[def],[evd],[hp],[mp],[crt]): ")
                break
        break
    return entry

########################################################################################################################
# Game Utilities                                                                                                       #
########################################################################################################################


def passive_modifier(character, att):
    """
    Modifies attack damage dependant on class ability
    :param cls:
    :param att: initial attack damage
    :return: mod_att: modified attack damage
    """
    cls = character["class"]
    if cls == "Archer":
        pass
    elif cls == "Knight":
        pass
    else:
        print("Invalid Class")
