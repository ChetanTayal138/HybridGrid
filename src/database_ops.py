from data_storage import init_client




def list_databases():
	cl = init_client()
	return cl.database_names()


def get_database(dbname): #Getting the database
    db = init_client()[f'{dbname}']
    return db

def view_database(dbname):
    db = get_database(dbname)
    return f"{db}"
  
def view_collections(dbname):
	db = get_database(dbname)
	return f"{db.list_collection_names()}"


def add_collection(dbname,coll_name):
	db = get_database(dbname)
	collection = db[f'{coll_name}'] #Access a collection within a databasr 
	return collection 

def remove_collection(dbname,coll_name):
	db = get_database(dbname)
	collection = db[f'{coll_name}']
	return collection.drop() #Returns True if collection was dropped and false if collection was not dropped.







def del_database(dbname):
    client = init_client()
    client.drop_database(f'{dbname}')
    return client 



if __name__ == "__main__":

	print(list_databases())
	print(view_collections('test_database'))
	col = add_collection('test_database' , 'UPVURNL')
	print(col)
	print(view_collections('test_database'))