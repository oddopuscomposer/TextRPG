from game import launch
from edit import edit_game


def main():
    status = True
    while status:
        print("Welcome to the TextRPG created by ChresSSB")
        print("1. New Game")
        print("2. Load Game")
        print("3. Edit Game")
        print("4. Credits")
        print("5. Quit")
        command = input("Select an option: ").lower()
        if command == "1" or command.startswith("new"):
            launch("new")
        elif command == "2" or command.startswith("loa"):
            launch("saves")
        elif command == "3" or command.startswith("edi"):
            edit_game()
        elif command == "4" or command.startswith("cre"):
            print("Thank you for ShoShin for very minor help on edit methods and Khajeet for being a tester")
        elif command == "5" or command.startswith("qu"):
            status = False
        else:
            print("Select a valid option!")


main()

