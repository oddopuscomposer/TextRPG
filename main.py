from game import launch
from edit import edit_game


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
            edit_game()
        else:
            status = False
            print("Quit")



main()

