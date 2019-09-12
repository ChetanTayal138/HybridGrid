from pymongo import MongoClient 
from data_gather import *



UP_URL = "http://www.upsldc.org/real-time-data"




def init_client(): #Making connection with MongoClient 
    client = MongoClient(r'mongodb://localhost:27017/')
    return client 

def get_database(dbname): #Getting the database
    db = init_client()[f'{dbname}']
    return db

def insertPost(in_post , dbname):
    DB = get_database(f'{dbname}')
    posts = DB.posts
    print("POSTS ARE" + str(posts))


def insertPosts(in_posts,dbname):  
    DB = get_database(f'{dbname}')
    print(DB)
    posts = DB.posts 
    post_id = posts.insert_many(in_posts).inserted_ids #Inserting a list of dictionaries
    return DB , post_id



def init_env(dbname1, dbname2):
    DB1 = get_database(dbname1)
    DB2 = get_database(dbname2)
    print(type(DB1))






if __name__ == "__main__" :
    # postslist = get_data(UP_URL , js = True)
    # DB , postid = insertPosts(postslist, 'UPS')
    # for post in DB.posts.find():
    #     print(post)
    print(del_database("UPS"))
    init_env("test_database" , "UPS")


#Create 2 Databases for Uttar Pradesh - Summary DataBases and Real Time Database
#Create Seperate Collections for Each Region 
#In each Collection, create a document for each region
