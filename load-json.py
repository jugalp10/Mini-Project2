import pymongo
import json


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
