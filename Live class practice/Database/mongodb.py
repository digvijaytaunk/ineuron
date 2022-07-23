import os
import pymongo

from data import student_data, product_data


user_name = os.getenv('MONGO_DB_CLOUD_USER')
password = os.getenv('MONGO_DB_CLOUD_PASSWORD')

# Connection string from MongoDB Atlas
client = pymongo.MongoClient(
    f"mongodb+srv://{user_name}:{password}@cluster0.malrj.mongodb.net/?retryWrites=true&w=majority"
)

db = client.test
database = client['ml_db']
collection = database["ineuron_test"]


def insert_data(data_to_insert):
    """
    Insert command to insert one record or many records by passing array or records
    """
    # Insert 1 record by passing 1 JSON object
    collection.insert_one(data_to_insert)

    # insert many by passing array of many records
    collection.insert_many(data_to_insert)


def find_all_in_collection():
    """
    Returns all the records exists in the provided Collection
    """
    return collection.find()


def find_with_query():
    """
    Different find functions to fetch data from collection
    """
    check_in_string = collection.find({'key': {'$in': ['A', 'P']}})
    greater_than = collection.find({'status': {"$gt": "C"}})
    greater_than_equal = collection.find({'qty': {'$gte': 75}})
    multiple_keys = collection.find({'item': 'sketch pad', 'qty': 95})
    multiple_keys_with_query = collection.find({'item': 'sketch pad', 'qty': {"$gte": 75}})
    or_operator = collection.find({'$or': [{'item': 'sketch pad'}, {'qty': {"$gte": 75}}]})


def update():
    """
    Update records by passing the object data to find and new object with new value
    """
    collection.update_one({'key_to_find': 'with_value'}, {'$set': {'key': 'New Value'}})


def find_by_key_value(coll, key, val):
    """
    Find data by key value pair
    """
    return coll.find({key: val})


def insert():
    """
    Function to Insert record(s)
    """
    collection.insert_one({"one": "data"})
    collection.insert_many([{"one": "data"}, {"two": "data"}])


def delete():
    """
    Function to Delete record(s)
    """
    collection.delete_many({"student_id": 5})
    collection.delete_one({"student_id": 5})


if __name__ == '__main__':
    # INSERT DATA
    # data = {'key': 'value'}
    # insert_data(data)

    # Find all
    all_data = find_all_in_collection()
    for record in all_data:
        print(record)

    # DELETE
    # delete()


