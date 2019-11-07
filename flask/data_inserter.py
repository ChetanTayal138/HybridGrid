from database_ops import insert_documents, insert_document, view_documents, get_database 
from collection_ops import get_collection 

def insert_values(db, col_name, g_name, new_values):

    col = get_collection(db, col_name)
    col.update({'gen_name':g_name} , {'$push' : {'DC' : new_values[0]}})
    col.update({'gen_name':g_name} , {'$push' : {'Schedule' : new_values[1]}})
    col.update({'gen_name':g_name} , {'$push' : {'Actual' : new_values[2]}})
    col.update({'gen_name':g_name} , {'$push' : {'OI_UI' : new_values[3]}})
    
    



def update_mongodb_values(result_set, db):

    collections = ['UPRVUNL', 'UPJVNL', 'IPP']

    for result in result_set[:9]: 
        insert_values(db, collections[0], result[-1] , list(result)[:-1])

    for result in result_set[9:12]: 
        insert_values(db, collections[1], result[-1] , list(result)[:-1])
    
    for result in result_set[12:]: 
        insert_values(db, collections[2], result[-1] , list(result)[:-1])
    


if __name__ == '__main__':
    insert_values('Uttar-Pradesh', 'UPJVNL', 'RIHAND' , [23, 41, 53,63])



    