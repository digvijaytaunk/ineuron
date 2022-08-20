# 1 . Write a program to insert a record in sql table via api
# 2.  Write a program to update a record via api
# 3 . Write a program to delete a record via api
# 4 . Write a program to fetch a record via api
# 5 . All the above questions you have to answer for mongo db as well .

import os
from flask import Flask, request, jsonify
import mysql.connector as connection
import pymongo

app = Flask(__name__)

user_name = os.getenv('MYSQL_DB_LOCAL_USER')
password = os.getenv('MYSQL_DB_LOCAL_PASSWORD')

mongo_user = os.getenv('MONGO_DB_CLOUD_USER')
mongo_password = os.getenv('MONGO_DB_CLOUD_PASSWORD')

# SQL Connection
host = "localhost"
database = 'ineuron'
table = 'api_db'

conn = connection.connect(host=host, user=user_name, password=password)
cursor = conn.cursor()


# SQL Database Functions
def _db_insert_sql(data):
    try:
        prod = data['product_name']
        price = data['price']
        query = f'INSERT INTO {database}.{table} (product_name, price) Values ("{prod}", {price})'
        cursor.execute(query)
    except Exception as e:
        return {'Status': 'Fail', 'msg': e}

    return {'Status': 'Success', 'msg': ''}


def _db_update_sql(data):
    try:
        prod = data['product_name']
        price = data['price']
        query = f'UPDATE {database}.{table} SET product_name = "{prod}", price = {price}'
        cursor.execute(query)
    except Exception as e:
        return {'Status': 'Fail', 'msg': e}

    return {'Status': 'Success', 'msg': ''}


def _db_delete_sql(prod):
    try:
        query = f'DELETE FROM {database}.{table} WHERE product_name = "{prod}"'
        cursor.execute(query)
    except Exception as e:
        return {'Status': 'Fail', 'msg': e}

    return {'Status': 'Success', 'msg': ''}


def _db_fetch_sql():
    try:
        query = f'SELECT * FROM {database}.{table}'
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as e:
        return {'Status': 'Fail', 'msg': e}

    return {'Status': 'Success', 'msg': '', 'data': data}


# SQL Routes
@app.route('/sql/insert/', methods=['POST'])
def insert_sql():
    """
    Route to Add new data into SQL Database
    """
    if request.method == 'POST':
        data_obj = _parse_request(request.json)
        response = _db_insert_sql(data_obj)
        return "Success" if response["Status"] == "Success" else "Fail"


@app.route('/sql/update', methods=['POST'])
def update_sql():
    """
    Route to Edit/Update existing data in SQL Database
     Body = {"product_name": "Laptop", "price": 89000}
    """
    if request.method == 'POST':
        data_obj = _parse_request(request.json)
        response = _db_update_sql(data_obj)
        return "Success" if response["Status"] == "Success" else f"Fail {response['msg']}"


@app.route('/sql/delete', methods=['POST'])
def delete_sql():
    """
    Route to Delete existing data by providing index from SQL Database
    Body = {"product_name": "Laptop"}
    """
    if request.method == 'POST':
        product = request.json['product_name']
        response = _db_delete_sql(product)
        return "Success" if response["Status"] == "Success" else f"Fail {response['msg']}"


# TODO Add primary key to DB to fetch single item when index is passed from URL args.
@app.route('/sql/fetch', methods=['GET'])
def fetch_sql():
    """
    Route to Fetch existing data from SQL Database by providing index
    """
    if request.method == 'GET':
        response = _db_fetch_sql()
        return jsonify(response["data"]) if response["Status"] == "Success" else f"Fail {response['msg']}"


def _parse_request(req):
    """
    Extracts data from Request object
    """
    if 'product_name' in req and 'price' in req:
        prod = req['product_name']
        price = req['price']
        return {"product_name": prod, "price": price}


# MONGO connection *****************************************************************
client = pymongo.MongoClient(
    f"mongodb+srv://{mongo_user}:{mongo_password}@cluster0.malrj.mongodb.net/?retryWrites=true&w=majority"
)
db = client.test
mongo_database = client['ml_db']
collection = mongo_database['api_db']


# MOngo Database
def _db_insert_mongo(data_obj):
    try:
        collection.insert_one(data_obj)
    except Exception as e:
        return {'Status': 'Fail', 'msg': e}

    return {'Status': 'Success', 'msg': ''}


def _db_delete_mongo(data_obj):
    try:
        collection.delete_one(data_obj)
    except Exception as e:
        return {'Status': 'Fail', 'msg': e}

    return {'Status': 'Success', 'msg': ''}


def _db_update_mongo(data_obj):
    try:
        prod = data_obj['product_name']
        new_price = data_obj['price']
        collection.update_one({'product_name': prod}, {'$set': {'price': new_price}})
    except Exception as e:
        return {'Status': 'Fail', 'msg': e}

    return {'Status': 'Success', 'msg': ''}


# MONGO Routes
@app.route('/mongo/insert', methods=['POST'])
def insert_mongo():
    if request.method == 'POST':
        data_obj = _parse_request(request.json)
        response = _db_insert_mongo(data_obj)
        return "Success" if response["Status"] == "Success" else f"Fail {response['msg']}"


@app.route('/mongo/update', methods=['POST'])
def update_mongo():
    """
    Update the New Price of the product passed.
    Body = {"product_name": "Laptop", "price": 89000}
    """
    if request.method == 'POST':
        data_obj = _parse_request(request.json)
        response = _db_update_mongo(data_obj)
        return "Success" if response["Status"] == "Success" else f"Fail {response['msg']}"


@app.route('/mongo/delete', methods=['POST'])
def delete_mongo():
    """
    Route to Delete existing data by providing product name
    Body = {"product_name": "Laptop"}
    """
    if request.method == 'POST':
        response = _db_delete_mongo(request.json)
        return "Success" if response["Status"] == "Success" else f"Fail {response['msg']}"


@app.route('/mongo/fetch', methods=['GET'])
def fetch_mongo():
    """
    Route to Fetch existing data from MONGO Database
    """
    if request.method == 'GET':
        response = collection.find()
        print(response)
        data = []
        for record in response:
            del record['_id']
            data.append(record)
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

