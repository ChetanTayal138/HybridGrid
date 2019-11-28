import mysql.connector
from mysql.connector import Error 
from distribution import distribution_main 


HOST = 'localhost'
DATABASE = 'uttar_pradesh'
USER = ''
PASSWORD = ''
UP_URL = "http://www.upsldc.org/real-time-data"

def calculate_difference(HOST , DATABASE , USER , PASSWORD):

    try:
        connection = mysql.connector.connect(host = HOST, database = DATABASE , user = USER , password = PASSWORD)
        cursor = connection.cursor(buffered = True)
        queries = get_query("algo_queries.txt")
        for query in queries:
            query = query.replace("\n" , "")
            cursor.execute(query)
            diff_rs = (cursor.fetchall())
            return diff_rs
    except Error as e:
        pass
        





def get_query(filename):

    queries = []
    f = open(filename , "r")
    for line in f:
        queries.append(line)
    return queries


def generate_dictionary(result_set):
    rs = distribution_main()

    gen_dicts = { 1:[[],[],[],[],[]] , 2:[[],[],[],[],[]] , 3:[[],[],[],[],[]] , 4:[[],[],[],[],[]] , 5:[[],[],[],[],[]] , 6:[[],[],[],[],[]] , 7:[[],[],[],[],[]] , 8: [[],[],[],[],[]] , 9 : [[],[],[],[],[]]}

    for i in rs:
        gen_dicts[i[0]][4].append(i[1])


    
    
    for rset in result_set:
        gen_dicts[rset[1]][0].append(rset[0])
        gen_dicts[rset[1]][1].append(rset[2])
    return gen_dicts
    
def calculate_sum(gdicts):

    sums = []
    for i in gdicts:
        sums.append(sum(gdicts[i][1]))
    return sums 



def calculate_proportions(summ , gen_dicts):

    for i in range(1,len(gen_dicts)+1):
        for val in gen_dicts[i][1]:
            gen_dicts[i][2].append(round(val/(summ[i-1]+0.1)  , 2))
    return gen_dicts


def calculate_required(gen_dicts):

    for i in gen_dicts:
        for j in range(len(gen_dicts[i][1])):
            gen_dicts[i][3].append(round(gen_dicts[i][4][0] * gen_dicts[i][2][j] , 2)) 
    return gen_dicts


def create_resultset(gen_dicts):
    resultset = []
    

    for i in gen_dicts:
        for j in range(len(gen_dicts[i][1])):
            resultset.append((gen_dicts[i][3][j],gen_dicts[i][0][j]))

    return resultset


def required_main():
    
    rs = calculate_difference(HOST , DATABASE , USER , PASSWORD)
    gen_dict = generate_dictionary(rs)
    summ = calculate_sum(gen_dict)
    gen_dict = calculate_proportions(summ, gen_dict)
    gen_dict =  calculate_required(gen_dict)
    i = create_resultset(gen_dict)
    
    try:
        connection = mysql.connector.connect(host = HOST, database = DATABASE , user = USER , password = PASSWORD)
        cursor = connection.cursor(buffered = True)
        queries = get_query("algo_queries.txt")
        for query in queries:
            if "UPDATE" in query:
                query = query.replace("\n" , "")
                for j in i:
                    cursor.execute(query,j)

        connection.commit()
        cursor.close()

    except Error as e: 

        print(e)



if __name__ == "__main__":

    required_main()
