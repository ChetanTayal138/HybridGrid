import mysql.connector
from mysql.connector import Error 
from mysqldb import get_query


HOST = 'localhost'
DATABASE = 'uttar_pradesh'
USER = 'root'
PASSWORD = 'iamaboy3801'
UP_URL = "http://www.upsldc.org/real-time-data"

def distribution_main():
    rs1 = None 


    try:
        connection = mysql.connector.connect(host = HOST, database = DATABASE , user = USER , password = PASSWORD)
        cursor = connection.cursor(buffered = True)
        queries = get_query("distrib_queries.txt")
        for query in queries:
            query = query.replace("\n" , "")
            cursor.execute(query)
            rs = cursor.fetchall()
            return rs 

            if "CURRENT" in query:
                query = query.replace("\n" , "")
                cursor.execute(query)
                rs2 = cursor.fetchall()
                
            elif "REQUIRED" in query:
                query = query.replace("\n" , "")
                cursor.execute(query)
                rs1 = cursor.fetchall()

    except Error as e:
        print(e)








if __name__ == '__main__':
    rs = distribution_main()
    print(rs)


