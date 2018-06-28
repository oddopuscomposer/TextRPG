import json


def process_json(filename):
    """
    Process the json to be read as a dictionary
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


def add_class():
    """
    adds a class to the classes json database
    :return:
    """
    classes = process_json("classes.json")
    name = input("Enter class name: ")
    classes["classes"][name] = {}
    health = input("Enter health: ")
    classes["classes"][name]["health"] = int(health)
    mana = input("Enter mana: ")
    classes["classes"][name]["mana"] = int(mana)
    write_json("classes.json", classes)

def remove_class():
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

    buy_price = input("Enter buy price: ")
    item["buy_price"] = int(buy_price)

    sell_price = input("Enter sell price: ")
    item["sell_price"] = int(sell_price)

    rarity = input("Enter rarity: ")
    item["rarity"] = rarity

    damage = input("Enter damage: ")
    item["damage"] = int(damage)

    cls = input("Enter required classes([class1],[class2]): ")
    words = cls.split(",")
    item["class"] = words

    slot = input("Enter slot: ")
    item["slot"] = slot

    item["stats"] = {}
    stats = input("Enter stats([att],[def],[evd]): ")
    words = stats.split(",")
    item["stats"]["att"] = words[0]
    item["stats"]["def"] = words[1]
    item["stats"]["evd"] = words[2]

    write_json("items.json", items)

def remove_equipable():
    """
    Remove equipable from items.json
    :return:
    """
    pass

# add_class()
# add_equipable()
