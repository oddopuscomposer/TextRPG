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


def numeric_array_validation(entry):
    while True:
        count = 0
        for item in entry:
            if type(item) == int:
                count += 1

        if count != len(entry):
            entry = input("Please input an invalid integer array: ")
        else:
            return entry


def numeric_array_validation_at_least_one(entry):
    while True:
        count = 0

        for item in entry:
            try:
                item = int(item)
            except:
                pass
            if type(item) == int:
                count += 1

        if count != len(entry) or len(entry) < 1 or entry == ['']:
            entry = input("Please input an invalid integer array: ")
            entry = entry.split(",")
        else:
            final_entry = []
            for item in entry:
                final_entry.append(int(item))
            return final_entry


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


def array_validation(entry, checked):
    """
    Validates arrays
    :param entry:
    :param checked:
    :return:
    """
    while True:
        if type(entry) == str:
            if entry in checked:
                return entry
            else:
                entry = input("Try again: ")
        else:
            while True:
                count = 0
                for item in entry:
                    if item in checked:
                        count += 1
                    else:
                        break
                    if count == len(entry):
                        return entry

                entry = input("Please input a valid array: ")
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


def enemy_drop_validation(entry):
    items = process_json("items.json")["xref"]
    while True:
        drop = 0
        count = 0
        new_dict = {}
        for split in entry:
            pair = split.split(":")
            item = pair[0]
            prob = float(pair[1])
            if item in items and 0.0 < prob <= 1.0:
                count += 1
                drop += float(prob)
                new_dict[item] = float(prob)
            else:
                print("Item not exist or probability not between 0-1")
                entry = input("Please input valid values: ")
                break
        if count == len(entry) and drop <= 1:
            return new_dict
        else:
            print("Item not all valid or total drops probability greater than 1")
            entry = input("Please input valid values: ")

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
