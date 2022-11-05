import pymongo
import json


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

    myclient = pymongo.MongoClient("localhost", port)
    db = myclient["291db"]
    db["dblp"].drop()
    dblp = db["dblp"]

    data = []
    with open(fileName, "r") as f:
        for line in f:
            data.append(json.loads(line.strip()))

    dblp.insert_many(data)


if __name__ == "__main__":
    main()
