from database_ops import get_database
from extractor import create_generators, get_generator_data
from database_ops import delete_all_documents , insert_document , view_documents, insert_documents
from extractor import extract_result_set
from mysqldb import sql_main
from data_inserter import insert_values , update_mongodb_values
from collection_ops import view_collections 


HOST = 'localhost'
DATABASE = 'uttar_pradesh'
USER = 'root'
PASSWORD = '********'
UP_URL = "http://www.upsldc.org/real-time-data"



"""
Values get refreshed every 5 minutes
In one hour there will be 12 observations 
In 24 hours there will be 24x12 = 288 observations 
In 30 days there will be 288x30 = 8640 observations 

How do I scale this up?

4 values for each Document in a collection where the document name is the name of the Generator.
JSON associated with each generator should will look like this :- 

{
    gen_name : 'ANPARA-A'  
    DC : [] , 
    Schedule : [] , 
    Actual : [] , 
    OI_UI : []
}

"""



def check_collecions(db):
    if(view_collections(db) == ['UPJVNL', 'UPRVUNL', 'IPP']):
        return True
    return False






def init_mongodb(db,flush = True, view = True):

    UPRVUNL, UPJVNL ,IPP  = create_generators()

    if flush:
        print(delete_all_documents(db,'UPRVUNL'))
        print(delete_all_documents(db,'UPJVNL'))
        print(delete_all_documents(db,'IPP'))

    for key in UPRVUNL: 
        insert_document(db, 'UPRVUNL', {'gen_name': key , 'DC' : UPRVUNL[key]['DC'] , 'Schedule' : UPRVUNL[key]['Schedule'] , 'Actual' : UPRVUNL[key]['Actual'] , 'OI_UI' : UPRVUNL[key]['OI_UI']})

    for key in UPJVNL:
        insert_document(db, 'UPJVNL', {'gen_name': key ,'DC' : UPJVNL[key]['DC'] , 'Schedule' : UPJVNL[key]['Schedule'] , 'Actual' : UPJVNL[key]['Actual'] , 'OI_UI' : UPJVNL[key]['OI_UI']})

    for key in IPP:
        insert_document(db, 'IPP', {'gen_name': key , 'DC' : IPP[key]['DC'] , 'Schedule' : IPP[key]['Schedule'] , 'Actual' : IPP[key]['Actual'] , 'OI_UI' : IPP[key]['OI_UI']})

    if view:
        view_documents(db, 'UPRVUNL')    
        view_documents(db, 'UPJVNL')
        view_documents(db, 'IPP')

    return db 


def main():


    
   
    db = get_database('Uttar-Pradesh')
    if(check_collecions(db) == False):
        db = init_mongodb(get_database('Uttar-Pradesh'),flush = True, view = True)

    

    dict_UPRVUNL, dict_UPJVNL, dict_IPP = get_generator_data(UP_URL)
    res = extract_result_set(dict_UPRVUNL, dict_UPJVNL, dict_IPP)
    update_mongodb_values(res , db)
    print("UPDATED MONGO")
    view_documents(db, 'UPJVNL')
    rs  = sql_main(res, HOST,DATABASE, USER, PASSWORD)
    print("UPDATED DATABASE")










if __name__ == "__main__":
    main()







