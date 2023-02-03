import bcrypt
import pymongo

import Helper

client = pymongo.MongoClient(
    "mongodb+srv://myappuser:mXksi132@cluster0.xxtjtei.mongodb.net/?retryWrites=true&w=majority")

db = client['myappdatabase']

collection = db['users']

user = {"username": "admin", "password": Helper.Passwords.hash_password('admin')}

collection.insert_one(user)


# def hash_password(password: str):
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode(), salt)
#     return hashed_password
#
#
# def verify_password(password: str, hashed_password: str):
#     return bcrypt.checkpw(password.encode(), hashed_password)
#
#
#
# client = pymongo.MongoClient(
#     "mongodb+srv://myappuser:mXksi132@cluster0.xxtjtei.mongodb.net/?retryWrites=true&w=majority")
#
# db = client['myappdatabase']
#
# collection = db['users']
#
# user = {"username": "admin", "password": hash_password('admin')}
#
# # x = collection.insert_one(user)
#
#
# myquery = { "username": "admin" }
#
# mydoc = collection.find(myquery)
#
# print(mydoc[0].get('password'))
#
# print(verify_password('admin', mydoc[1].get('password')))