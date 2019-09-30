from generator_data import get_generator_data
from database_ops import get_database , list_databases , view_documents , get_documents , insert_document 
from collection_ops import view_collections
from extractor import extract_result_set 
from mysqldb import sql_main 

UP_URL = "http://www.upsldc.org/real-time-data"




def main():
    UPRVUNL, UPJVNL, IPP   = get_generator_data(UP_URL) #returns list of categories with each item in the list itself being a list of dicitonaries
    # print(UPRVUNL)
    db = get_database('Uttar-Pradesh')
    
    # resultset = extract_result_set(UPRVUNL, UPJVNL, IPP)
    # if(sql_main(resultset)):
    #     print("SUCCESSFULLY UPDATED MYSQL DATABASE")

    

    # print(insert_document(db, 'UPRVUNL' , UPRVUNL))
    print(insert_document(db, 'UPJVNL' , UPJVNL))
    # print(insert_document(db, 'IPP' , IPP))

    

    print(get_documents(db,'UPJVNL'))
   # print(get_documents(db,'UPRVUNL'))
   # print(get_documents(db, 'IPP'))


    







if __name__ == "__main__":
    main()