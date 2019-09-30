import mysql.connector
from mysql.connector import Error
from extractor import extract_result_set 
from generator_data import get_generator_data


HOST = 'localhost'
DATABASE = 'uttar_pradesh'
USER = 'root'
PASSWORD = 'iamaboy3801'
UP_URL = "http://www.upsldc.org/real-time-data"


def get_query(filename):
    queries = []
    f = open(filename , "r")
    for line in f:
        queries.append(line)

    return queries

def sql_main(new_data):

    rs = []

    try:
            connection = mysql.connector.connect(host = HOST,database = DATABASE,user = USER,password = PASSWORD)
            cursor = connection.cursor(buffered = True)
            queries = get_query("queries.txt")
        
            for query in queries:

                if "UPDATE" in query:
                    query = query.replace("\n",  "")
                    for i in new_data:
                        cursor.execute(query , i)
                    #rs.append(cursor.fetchall())

                else:
                    query = query.replace("\n",  "")
                    cursor.execute(query)
                    rs.append(cursor.fetchall())

            connection.commit()
            cursor.close()
                

    except Error as e:
        print("Error Encountered : " + str(e))
        return False


    return True



if __name__ == '__main__':
        

        dict_UPRVUNL, dict_UPJVNL, dict_IPP = get_generator_data(UP_URL)
        res = extract_result_set(dict_UPRVUNL, dict_UPJVNL, dict_IPP)
        if((sql_main(res))):
            print("SUCCESSFULLY UPDATED DATABASE")






