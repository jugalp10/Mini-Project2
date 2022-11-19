import pymongo
from pymongo import TEXT
import json
import os


#
# This is the main function and it is the first function that gets invoked.
# This function will prompt the user to provide the name of the JSON file
# containing the data. The user will also be prompted for the port number
# of the mongoDB server that is running in the background. The function will
# create a database called 291db, then it will create a new collection called
# dblp. The function will read all the documents from the JSON file and
# insert them into the dblp collection.
#
def main():
    print("Don't include the .json extension.")
    fileName = input("JSON File name (*.json): ")
    fileName += ".json"
    port = int(input("Port Number: "))

    query = f"mongoimport --port {port} --db 291db --collection dblp --drop --batchSize 15000 --file {fileName}"
    os.system(query)

    myclient = pymongo.MongoClient("localhost", port)
    db = myclient["291db"]
    dblp = db["dblp"]
    dblp.aggregate([
        {"$addFields": {"year_str": {"$toString": "$year"}}},
        {"$out": "dblp"}
    ])
    dblp.create_index(
        keys = [
            ("title", TEXT),
            ("authors", TEXT),
            ("abstract", TEXT),
            ("venue", TEXT),
            ("year_str", TEXT)
        ],
        default_language='none'
    )
    dblp.create_index(
        keys = [
            ("references", 1)
        ],
        default_language='none'
    )


if __name__ == "__main__":
    main()
