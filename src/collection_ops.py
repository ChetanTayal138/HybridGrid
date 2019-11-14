from summary_data import get_summary_data 
from pymongo import MongoClient 


UP_URL = "http://www.upsldc.org/real-time-data"


def view_collections(db):
	return db.list_collection_names()

def get_collection(db,col_name):
	return db[f'{col_name}']


def add_collection(db,col_name):
	collection = db[f'{col_name}'] #Access a collection within a databasr 
	return collection 

def remove_collection(db,col_name):
	collection = db[f'{col_name}']
	return collection.drop() #Returns True if collection was dropped and false if collection was not dropped.



if __name__ == '__main__':
	client = MongoClient(r'mongodb://localhost:27017/')
	db = client['Uttar-Pradesh']


	### INITIALISING THE COLLECTIONS ###
	# collections = ['UPRVUNL', 'UPJVNL', 'IPP']
	# cols = []

	### ADDING THE COLLECTIONS TO THE NEEDED DATABASE ###

	# for collection in collections:
	# 	cols.append(add_collection(db, collection))

	# print(cols)

	print(view_collections(db))
