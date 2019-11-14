import mysql.connector
from mysql.connector import Error
from extractor import extract_result_set 
from generator_data import get_generator_data


def get_query(filename):

    queries = []
    f = open(filename , "r")
    for line in f:
        queries.append(line)
    return queries




def sql_main(new_data, HOST, DATABASE, USER, PASSWORD):

    try:
        connection = mysql.connector.connect(host = HOST,database = DATABASE,user = USER,password = PASSWORD)
        cursor = connection.cursor(buffered = True)
        queries = get_query("queries.txt")
    
        for query in queries:

            if "UPDATE" in query:
                query = query.replace("\n",  "")
                for i in new_data:
                    print(i)
                    cursor.execute(query , i)
                

            else:
                query = query.replace("\n",  "")
                cursor.execute(query)
                rs = (cursor.fetchall())

        connection.commit()
        cursor.close()

        return rs
            

    except Error as e:
        print("Error Encountered : " + str(e))
        return False




if __name__ == '__main__':


        dict_UPRVUNL, dict_UPJVNL, dict_IPP = get_generator_data(UP_URL)
        res = extract_result_set(dict_UPRVUNL, dict_UPJVNL, dict_IPP)
        rs = sql_main(res, HOST, DATABASE, USER, PASSWORD)
        






