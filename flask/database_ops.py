from pymongo import MongoClient 
from collection_ops import view_collections , add_collection , get_collection 
from extractor import create_generators 


UP_URL = "http://www.upsldc.org/real-time-data"


def init_client(): #Making connection with MongoClient 
    client = MongoClient(r'mongodb://localhost:27017/')
    return client 


def create_databases(databases):
    client = init_client()
    dbs = []
    for database in databases:
        dbs.append(client[f"{database}"])

    return dbs 


def list_databases():
    cl = init_client()
    return cl.database_names()


#Obtain the database required 
def get_database(dbname): 
    db = init_client()[f'{dbname}']
    return db

def del_database(dbname):
    client = init_client()
    client.drop_database(f'{dbname}')
    return client 

def insert_document(db,col_name,doc_dict):
    col = get_collection(db,col_name)
    return col.insert_one(doc_dict)


#doc_dicts is a list of dictionary
def insert_documents(db,col_name,doc_dicts):  
    col = get_collection(db,col_name)
    return col.insert_many(doc_dicts)

def view_documents(db, col_name):
    col = get_collection(db,col_name)
    for document in col.find():
        print(document)
    

def get_documents(db , col_name):
    docs = [] 
    col = get_collection(db, col_name)
    for document in col.find():
        docs.append(document)

    return docs 


def delete_all_documents(db, col_name):
    col = get_collection(db,col_name)
    x = col.delete_many({})
    return x.deleted_count




if __name__ == "__main__":
    print(list_databases())
