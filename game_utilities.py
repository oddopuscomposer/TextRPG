import json


def process_json(filename):
    json1_file = open("data/" + filename)
    json1_str = json1_file.read()
    return json.loads(json1_str)


def write_json(filename, data):
    with open('data/' + filename, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)


def add_class():
        classes = process_json("classes.json")
        name = input("Enter class name: ")
        classes["classes"][name] = {}
        health = input("Enter health: ")
        classes["classes"][name]["health"] = health
        mana = input("Enter mana: ")
        classes["classes"][name]["mana"] = mana
        write_json("classes.json", classes)


def add_item():
    items = process_json("items.json")
    name = input("Enter item name: ")
    items["items"][name] = {}
    health = input("Enter health: ")
    items["items"][name]["health"] = health
    mana = input("Enter mana: ")
    items["items"][name]["mana"] = mana
    write_json("items.json", items)


#add_class()
add_item()
