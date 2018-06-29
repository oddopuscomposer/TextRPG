import json
from game import launch


def main():
    status = True
    while status:
        print("Welcome to the RPG")
        command = input("1 for new game, 2 for load, 3 for edit, anything else for quit: ")
        if command == "1":
            launch("new")
        elif command == "2":
            launch("saves")
        elif command == "3":
            pass
        else:
            status = False
            print("Quit")



main()

