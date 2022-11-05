import pymongo
import json
from clear import clear

#
# This function creates a prompt that displays the operations that the
# user can perform. The user will then provide an integer between 1
# and 5. The user choice will be verified before it is returned as
# an integer
#
def userInterface():
    while True:
        print(
"""(1) Search for articles
(2) Search for authors
(3) List the venues
(4) Add an article
(5) End the program"""
        )
        choice = input("Enter your choice (1 - 5): ")
        if choice == "1":
            return 1
        elif choice == "2":
            return 2
        elif choice == "3":
            return 3
        elif choice == "4":
            return 4
        elif choice == "5":
            return 5
        else:
            print("Your input is invalid. Press ENTER to continue.")
            input()
            clear()


def searchForArticles():
    pass


def searchForAuthors():
    pass


def listTheVenues():
    ########################################
    # James's work starts here
    ########################################
    pass


def addAnArticle():
    ########################################
    # Jugal's work starts here
    ########################################
    pass


#
# This is the main function and it is the first function that gets invoked.
# This function will ask the user for the port number. The port number will
# be used to connect to the MongoDB server throughout the program.
#
def main():
    clear()
    port = int(input("Port Number: "))
    clear()

    choice = userInterface()
    if choice == 1:
        searchForArticles()
    elif choice == 2:
        searchForAuthors()
    elif choice == 3:
        listTheVenues()
    elif choice == 4:
        addAnArticle()
    else:
        exit()


if __name__ == "__main__":
    main()
