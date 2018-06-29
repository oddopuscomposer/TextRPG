import json


# ############## #
# #JSON Methods# #
# ############## #

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


def add_class():
    """
    adds a class to the classes json database
    :return:
    """
    classes = process_json("classes.json")
    name = input("Enter class name: ")
    classes["classes"][name] = {}
    health = input("Enter health: ")
    numeric_validation(health)
    classes["classes"][name]["health"] = int(health)

    mana = input("Enter mana: ")
    classes["classes"][name]["mana"] = int(mana)
    write_json("classes.json", classes)


def delete_class():
    """
    Removes class from classes.json
    :return:
    """
    pass


def add_equipable():
    """
    adds equipable item to items.json
    :return:
    """
    items = process_json("items.json")

    name = input("Enter item name: ")
    items["equipment"][name] = {}
    item = items["equipment"][name]

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

    cls = input("Enter required classes([class1],[class2]): ")
    # need validation
    words = cls.split(",")
    item["class"] = words

    slot = input("Enter slot: ")
    # need validation
    item["slot"] = slot

    item["stats"] = {}
    stats = input("Enter stats([att],[def],[evd]): ")
    words = stats.split(",")
    # need validation
    item["stats"]["att"] = words[0]
    item["stats"]["def"] = words[1]
    item["stats"]["evd"] = words[2]

    write_json("items.json", items)


def delete_equipable():
    """
    Remove equipable from items.json
    :return:
    """
    entry = input("Please enter an equipable: ")
    items = process_json("items.json")
    if entry in items["equipment"]:
        while True:
            confirm = input("Are you sure you want to delete " + entry + "? (y/n): ")
            if confirm == "y":
                del items["equipment"][entry]
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
    pass

def delete_misc_item():
    pass

# add_class()
delete_equipable()
#add_equipable()
