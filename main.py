import datetime
from pymongo import MongoClient
from datetime import date
import pprint
from bson import ObjectId

connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
database = client["Flora"]
floral_d = database["Floral Distribution"]
conserve_s = database["conserve status"]
species_s =database["species"]
loc=database["location"]