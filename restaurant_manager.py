"""Command-line restaurant manager backed by MongoDB (PyMongo)."""
import json
import os
from pathlib import Path
from pprint import pprint

DEFAULT_JSON = Path(__file__).parent / "data" / "restaurants.json"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "dbRestaurantsAds"
COLLECTION_NAME = "restaurant"


# ------------------------------------------------------------------------
class File:
    """Context manager that opens a file and always closes it."""

    def __init__(self, file_path, file_mode, encoding="utf-8"):
        self.file_path = file_path
        self.file_mode = file_mode
        self.encoding = encoding
        self.file_object = None

    def __enter__(self):
        self.file_object = open(self.file_path, self.file_mode, encoding=self.encoding)
        return self.file_object

    def __exit__(self, *exc):
        if self.file_object:
            self.file_object.close()


# ------------------------------------------------------------------------
def read_json_file(file_name):
    try:
        with File(file_name, "r") as file1:
            return json.load(file1)
    except (OSError, json.JSONDecodeError) as error:
        print("Could not read JSON file:", error)
        return None


def connection(uri=MONGO_URI):
    from pymongo import MongoClient  # imported here so the module loads without pymongo
    return MongoClient(uri, serverSelectionTimeoutMS=3000)


def get_collection(client, database_name=DB_NAME, collection_name=COLLECTION_NAME):
    return client[database_name][collection_name]


def add_restaurants(collection, restaurants):
    """Insert restaurants; re-importing the same file updates records instead of duplicating them."""
    for restaurant in restaurants:
        collection.replace_one({"code": restaurant["code"]}, restaurant, upsert=True)
    print(f"{len(restaurants)} restaurants imported")


def show_all_restaurants(collection):
    for restaurant in collection.find():
        pprint(restaurant)


def search_by_name(collection, res_name):
    results = list(collection.find({"name": res_name}))
    if not results:
        print("not found ...")
    for restaurant in results:
        pprint(restaurant)
    return results


def delete_by_code(collection, res_code):
    result = collection.delete_one({"code": res_code})
    if result.deleted_count:
        print("delete is successful")
    else:
        print("no restaurant with that code")
    return result.deleted_count


# ------------------------------------------------------------------------
def ask_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        return None


def show_menu():
    print("\t\t\t1) Read file and insert to database")
    print("\t\t\t2) Show all restaurants")
    print("\t\t\t3) Search restaurant by name")
    print("\t\t\t4) Delete restaurant by code")
    print("\t\t\t0) Exit")
    return ask_int("Enter command code : ")


def main():
    collection = get_collection(connection())
    while True:
        try:
            match show_menu():
                case 1:
                    data = read_json_file(DEFAULT_JSON)
                    if data:
                        add_restaurants(collection, data)
                case 2:
                    show_all_restaurants(collection)
                case 3:
                    search_by_name(collection, input("Enter name to search : "))
                case 4:
                    code = ask_int("Enter code to delete : ")
                    if code is None:
                        print("Code must be a number")
                    else:
                        delete_by_code(collection, code)
                case 0:
                    break
                case _:
                    print("Unknown command")
        except Exception as error:  # e.g. MongoDB not running
            print("Database error:", error)


if __name__ == "__main__":
    main()
