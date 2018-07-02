import json


########################################################################################################################
# JSON & String Methods                                                                                                         #
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
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

########################################################################################################################
# Validations                                                                                                          #
########################################################################################################################


def numeric_validation(entry):
    """
    Validates numeric inputs for entry
    :param entry: string
    :return:
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
    pass


def slot_validation(entry):
    """
    Validates character slots
    :param entry: string
    :return:
    """
    pass


def array_validation(entry):
    """
    Validates proper array entry
    :param entry: array
    :return:
    """
    pass

