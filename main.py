import pymongo
import json
import os
from clear import *

def selectArticle(index, mydocs, dblp):
    numOfDocs = len(mydocs)
    if index.isdigit():
        index = int(index)
        if index >= 0 and index < numOfDocs:
            id = mydocs[index]["id"] if "id" in mydocs[index] else ""
            title = mydocs[index]["title"] if "title" in mydocs[index] else ""
            authors = ", ".join(mydocs[index]["authors"] if "authors" in mydocs[index] else [])
            abstract = mydocs[index]["abstract"] if "abstract" in mydocs[index] else ""
            year = mydocs[index]["year"] if "year" in mydocs[index] else ""
            venue = mydocs[index]["venue"] if "venue" in mydocs[index] else ""
            references = mydocs[index]["references"] if "references" in mydocs[index] else []

            query = {
                "id": {"$in": references}
            }
            pretty_references = []
            for x in dblp.find(query):
                pretty_references.append(x)

            clear()
            print(f"id: {id}")
            horizontal_line()
            print(f"title: {title}")
            horizontal_line()
            print(f"authors: {authors}")
            horizontal_line()
            print(f"abstract: {abstract}")
            horizontal_line()
            print(f"year: {year}")
            horizontal_line()
            print(f"venue: {venue}")
            horizontal_line()
            print(f"references:")
            for ref in pretty_references:
                id2 = ref["id"]
                title2 = ref["title"]
                year2 = ref["year"]
                print(
f"""
{{
    id: {id2},
    title: {title2},
    year: {year2}
}}
""")
            horizontal_line()
            input("Press ENTER to continue: ")
        else:
            return
    else:
        return

#
# This function creates a prompt that displays the operations that the
# user can perform. The user will then provide an integer between 1
# and 5. The user choice will be verified before it is returned as
# an integer
#
def userInterface():
    while True:
        clear()
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


def searchForArticles(port):
    myclient = pymongo.MongoClient("localhost", port)
    db = myclient["291db"]
    dblp = db["dblp"]
    clear()
    print("Type in your keywords separated by a space here.")
    keywords = [(int(row) if row.isdigit() else row) for row in input("Keywords: ").split()]
    if len(keywords) <= 0:
        print("Not enough keywords. Press ENTER to continue.")
        input()
        return

    query = {
        "$and": []
    }
    for key in keywords:
        query["$and"].append(
            {
                "$or": [
                    {"title": {"$regex": f"^.*{key}.*$", "$options": "i"}},
                    {"authors": {"$regex": f"^.*{key}.*$", "$options": "i"}},
                    {"abstract": {"$regex": f"^.*{key}.*$", "$options": "i"}},
                    {"venue": {"$regex": f"^.*{key}.*$", "$options": "i"}},
                    {"year": key}
                ]
            }
        )
    mydocs = []
    for x in dblp.find(query):
        mydocs.append(x)
    clear()
    print("index: id | title | year | venue")
    horizontal_line()
    for i, x in enumerate(mydocs):
        id = x["id"] if "id" in x else ""
        title = x["title"] if "title" in x else ""
        year = x["year"] if "year" in x else ""
        venue = x["venue"] if "venue" in x else ""
        print(f"{i}: {id} | {title} | {year} | {venue}")
        horizontal_line()
    print(
"""Select article: index + ENTER
Main Screen: ENTER""")
    index = input("Command: ")
    selectArticle(index, mydocs, dblp)
    


def searchForAuthors(port):
    myclient = pymongo.MongoClient("localhost", port)
    db = myclient["291db"]
    dblp = db["dblp"]


def listTheVenues(port):
    myclient = pymongo.MongoClient("localhost", port)
    db = myclient["291db"]
    dblp = db["dblp"]
    ########################################
    # James's work starts here
    ########################################


def addAnArticle(port):
    myclient = pymongo.MongoClient("localhost", port)
    db = myclient["291db"]
    dblp = db["dblp"]
    ########################################
    # Jugal's work starts here
    ########################################


#
# This is the main function and it is the first function that gets invoked.
# This function will ask the user for the port number. The port number will
# be used to connect to the MongoDB server throughout the program.
#
def main():
    clear()
    port = int(input("Port Number: "))
    clear()

    while True:
        choice = userInterface()
        if choice == 1:
            searchForArticles(port)
        elif choice == 2:
            searchForAuthors(port)
        elif choice == 3:
            listTheVenues(port)
        elif choice == 4:
            addAnArticle(port)
        else:
            return


if __name__ == "__main__":
    main()
