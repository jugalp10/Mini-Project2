import pymongo
import re
from clear import *

#
# This function is invoked whenever a user selects an article. The index position and the
# list of articles are provided as input. The function will check if the index position is
# valid. When the index position is valid all the article fields which are contained in
# mydocs are displayed. For the references field the id, title, and year of the references
# are extracted from the MongoDB collection dblp. Once the user is done viewing the
# article the user is returned to the main screen.
# @param  index   an index giving the index position of the article in mydocs.
# @param  mydocs  a list containing all articles that match with the keyword specified by
#                 the user in the searchForArticles function.
# @param  dblp    this is the MongoDB collection containing a collection of articles.
# @return
#
def selectArticle(index, mydocs, dblp):
    numOfDocs = len(mydocs)
    if index.isdigit():
        index = int(index)
        if index >= 0 and index < numOfDocs:
            myArticle = mydocs[index]
            id = myArticle["id"] if "id" in myArticle else ""
            title = myArticle["title"] if "title" in myArticle else ""
            authors = ", ".join(myArticle["authors"] if "authors" in myArticle else [])
            abstract = myArticle["abstract"] if "abstract" in myArticle else ""
            year = myArticle["year"] if "year" in myArticle else ""
            venue = myArticle["venue"] if "venue" in myArticle else ""
            references = myArticle["references"] if "references" in myArticle else []

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
            query = {
                "id": {"$in": references}
            }
            pretty_references = []
            for x in dblp.find(query):
                pretty_references.append(x)
            for ref in pretty_references:
                id2 = ref["id"]
                title2 = ref["title"]
                year2 = ref["year"]
                print('-' * os.get_terminal_size().columns)
                print(
f"""    id: {id2},
    Title: {title2},
    Year: {year2}""")
            horizontal_line()
            input("Press ENTER to continue: ")
            return True
        else:
            # The user types in an invalid index.
            input("Index position is out of range. Press ENTER to try again: ")
            return True
    else:
        # The user chooses to exit the Search For Articles interface.
        return False


#
# This function is invoked in the searchForAuthors function. When an author is displayed the
# user can select an author and view all the articles published by that author. This function
# displays all the articles that are published by the selected author. The function takes in
# the parameter index and the list of authors myAuthors. Using index and myAuthors the author's
# name is retrieved. The author's name will then be used to retrieve all the articles under the
# author's name in dblp. The title, year, and venue of each article is displayed.
# @param  index      this is the index position of the author's name in the myAuthors list.
# @param  myAuthors  this is a list containing the names of all authors that match the keyword
#                    the user specified in searchForAuthors.
# @param  dblp       this is the MongoDB collection containing a collection of articles.
# @return
#
def selectAuthor(index, myAuthors, dblp):
    clear()
    numAuthors = len(myAuthors)
    if index.isdigit():
        index = int(index)
        if index >= 0 and index < numAuthors:
            authorName = myAuthors[index]
            horizontal_line()
            for article in dblp.aggregate([
                {"$match": {
                    "authors": authorName
                }},
                {"$project": {
                    "_id": 0,
                    "title": 1,
                    "year": 1,
                    "venue": 1
                }},
                {"$sort": {
                    "year": -1
                }}
            ]):
                title = article["title"] if "title" in article else ""
                year = article["year"] if "year" in article else ""
                venue = article["venue"] if "venue" in article else ""
                print(f"{title} | {year} | {venue}")
                horizontal_line()
            input("Press ENTER to continue: ")
            return True
        else:
            input("Index position is out of range. Press ENTER to try again: ")
            return True
    else:
        return False


#
# This function creates a prompt that displays the operations that the
# user can perform. The user will then provide an integer between 1
# and 5. The user choice will be verified before it is returned as
# an integer
# @return
#
def userInterface():
    while True:
        clear()
        horizontal_line()
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
            print("Your input is invalid. Press ENTER to try again.")
            input()
            clear()

#
# This function searches for articles. The function first asks the user for keywords. Articles that match with all
# the keywords the user specified are returned. A keyword match happens when the keyword is in at least one of the
# following: title, authors, abstract, venue, and year. The matching articles are stored in a list called mydocs and
# displayed accordingly. The user can also type in the index position of the article in the mydocs list and view the
# selected article. Viewing the selected article invokes the selectArticle function.
# @param  dblp  this is the MongoDB collection containing a collection of articles.
# @return
#
def searchForArticles(dblp):
    while True:
        clear()
        horizontal_line()
        print("Type in your keywords separated by a space here.")
        keywords = input("Keywords: ").split()
        if len(keywords) == 0:
            print("Not enough keywords. Press ENTER to try again.")
            input()
        else:
            break

    query = {
        "$text": {
            "$search": f"{' '.join(keywords)}"
        }
    }
    mydocs = []
    while True:
        clear()
        horizontal_line()
        print("index: id | title | year | venue")
        horizontal_line()
        i = 0
        for x in dblp.find(query):
            id = x["id"] if "id" in x else ""
            title = x["title"] if "title" in x else ""
            year = x["year"] if "year" in x else ""
            venue = x["venue"] if "venue" in x else ""
            print(f"{i}: {id} | {title} | {year} | {venue}")
            horizontal_line()
            mydocs.append(x)
            i += 1
        print(
"""Select article: index + ENTER
Main Screen: ENTER"""
        )
        if not selectArticle(input("Command: "), mydocs, dblp):
            break
    

#
# This function first prompts the user for a single keyword. The user's keyword will be used to search
# for authors that match the keyword. A keyword match happens if the author's name contains the keyword.
# All the authors from dblp that match with the keyword are printed. The author's name and the number of
# publications are printed. The user has the option to type in the index position of the author to view
# all the articles that the author published.
# @param  dblp  this is the MongoDB collection containing a collection of articles.
# @return
#
def searchForAuthors(dblp):
    while True:
        clear()
        horizontal_line()
        print("Type in a keyword.")
        keyword = input("Keyword: ")
        if keyword == "":
            input("You did not specify a keyword. Press ENTER to try again.")
        else:
            break
    authors = []
    while True:
        clear()
        horizontal_line()
        print("index: Author Name | Number of Publications")
        i = 0
        for author in dblp.aggregate([
            # Filter out articles that don't contain an author matching keyword
            {"$match": {
                "$text": {
                    "$search": f"{keyword}"
                }
            }},
            # Unwind remaining articles
            {"$unwind": "$authors"},
            # Filter out authors not matching keyword
            {"$match": {
                "authors": {
                    "$regex": f".*\\b{keyword}\\b.*",
                    "$options": "i"
                }
            }},
            # Count the number of publications by remaining authors
            {"$group": {
                "_id": "$authors",
                "Number Of Publications": {
                    "$sum": 1
                }
            }},
            # Simple projection
            {"$project": {
                "_id": 0,
                "authorName": "$_id",
                "Number Of Publications": 1
            }}
        ]):
            horizontal_line()
            authorName = author["authorName"]
            numPublications = author["Number Of Publications"]
            print(f"{i}: {authorName} | {numPublications}")
            authors.append(authorName)
            i += 1
        horizontal_line()
        print("Select author: index + ENTER")
        print("Main Screen: ENTER")
        if not selectAuthor(input("Command: "), authors, dblp):
            break


#
# This function first prompts the user for a number. This number will be the number of venues
# that will be displayed. The function will first filter out any articles that do not belong
# to a venue. After the articles are grouped together by the venue that they are in. The venue
# title, number of articles, and number of references are projected. The function will sort
# the venues by the number of articles. In the case of a tie the number of references will be
# used.
# @param  dblp  this is the MongoDB collection containing a collection of articles.
# @return
#
def listTheVenues(dblp):
    while True:
        clear()
        number = input("Enter a number n and see a listing of top n venues.\nNumber: ")
        if number.isdigit():
            number = int(number)
            if number > 0:
                break
            else:
                input("The number must be greater than 0. Press ENTER to continue.")
        else:
            input("Please enter a number. Press ENTER to continue.")
        clear()

    clear()
    print("Venue | Number of Articles | Number of References")
    for x in dblp.aggregate([
        # Filter out any documents without venues
        {"$match": {
            "venue": {
                "$exists": "true",
                "$nin": ["", "null"]
            }
        }},
        # Join each article (a1) with another article (a2) where
        # a1.id in a2.references
        {"$lookup": {
            "from": "dblp",
            "localField": "id",
            "foreignField": "references",
            "as": "second"
        }},
        # For each article count the number of references.
        {"$group": {
            "_id": {
                "venue": "$venue",
            },
            "Number Of Articles": {
                "$sum": 1
            },
            "Number Of References": {
                "$sum": {
                    "$size": {
                        "$ifNull": ["$second", []]
                    }
                }
            }
        }},
        # Simple projection
        {"$project": {
            "_id": 0,
            "venue": "$_id.venue",
            "Number Of Articles": 1,
            "Number Of References": 1
        }},
        # Sort by number of references first in descending order.
        # If tie then sort by number of articles in descending order.
        # If tie then sort alphabetically in ascending order.
        {"$sort": {
            "Number Of References": -1,
            "Number Of Articles": -1,
            "venue": 1
        }},
        # Only show the top n venues.
        {"$limit": number}
    ]):
        horizontal_line()
        venue_name = x["venue"]
        num_of_articles = x["Number Of Articles"]
        num_of_references = x["Number Of References"]
        print(f"{venue_name} | {num_of_articles} | {num_of_references}")
    horizontal_line()
    input("Press ENTER to continue: ")
    clear()


def addAnArticle(dblp):
    ########################################
    # Jugal's work starts here
    ########################################
    pass


#
# This is the main function and it is the first function that gets invoked.
# This function will ask the user for the port number. The port number will
# be used to connect to the MongoDB server throughout the program.
# @return
#
def main():
    clear()
    port = int(input("Port Number: "))
    myclient = pymongo.MongoClient("localhost", port)
    db = myclient["291db"]
    dblp = db["dblp"]
    clear()

    while True:
        choice = userInterface()
        if choice == 1:
            searchForArticles(dblp)
        elif choice == 2:
            searchForAuthors(dblp)
        elif choice == 3:
            listTheVenues(dblp)
        elif choice == 4:
            addAnArticle(dblp)
        else:
            return


if __name__ == "__main__":
    main()
