# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app import bcrypt
import imghdr
from flask_app.models import users_model

# model the class after the friend table from our database
class Article: #TODO rename clas. Pascel case
    def __init__( self , data:dict ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.content = data['content']
        self.photo = data['photo']
        self.author = data['author']
        self.user_id = data['user_id']
        self.header = data['header']

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO articles(name, content, photo, author, header, user_id) VALUE (%(name)s, %(content)s,%(photo)s,%(author)s,%(header)s, %(user_id)s);" #TODO Name table, columns, and values  #When using %()s, you must pass in data
        new_row_id= connectToMySQL(DATABASE).query_db(query,data) #Returns back an INT, the ID of the row inserted
        return new_row_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM articles;" #TODO Name table
        results = connectToMySQL(DATABASE).query_db(query) # make sure to call the connectToMySQL function with the schema you are targeting.
        all_users = [] # Create an empty list to append our instances of users
        for user in results: # Iterate over the db results and create instances of users with cls.
            all_users.append( cls(user) )
        return all_users

    @classmethod
    def get_all_join(cls):
        query = "SELECT * FROM articles JOIN users ON users.id = articles.user_id ORDER BY articles.created_at DESC;" #TODO Name table
        list_of_dict = connectToMySQL(DATABASE).query_db(query) # make sure to call the connectToMySQL function with the schema you are targeting.
        
        if not list_of_dict:
            return []
        
        articles = [] #For instances

        for user in list_of_dict:
            article = cls(user)
            user_data = {
                **user, #Including the non-conflicting columns
                'id' : user['users.id'],
                'created_at' : user['users.created_at'],
                'updated_at' : user['users.updated_at']
            }
            user_instance = users_model.User(user_data)
            article.user_instance = user_instance
            articles.append(article) 

        return articles

    @classmethod
    def get_all_join_search(cls, data:dict):
        print(data)
        search = data['search']
        query = f"SELECT * FROM articles JOIN users ON users.id = articles.user_id WHERE articles.name LIKE '%{search}%' ORDER BY articles.created_at DESC ;" #TODO Name table
        list_of_dict = connectToMySQL(DATABASE).query_db(query) # make sure to call the connectToMySQL function with the schema you are targeting.
        
        if not list_of_dict:
            return []
        
        articles = [] #For instances

        for user in list_of_dict:
            article = cls(user)
            user_data = {
                **user, #Including the non-conflicting columns
                'id' : user['users.id'],
                'created_at' : user['users.created_at'],
                'updated_at' : user['users.updated_at']
            }
            user_instance = users_model.User(user_data)
            article.user_instance = user_instance
            articles.append(article) 

        return articles

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM articles WHERE id = %(id)s;" #TODO Name table
        id_to_display = connectToMySQL(DATABASE).query_db(query,data)
        return id_to_display[0]
    
    @classmethod
    def get_one_join(cls, data):
        query = "SELECT * FROM articles JOIN users ON users.id = articles.user_id WHERE articles.id = %(id)s;" #TODO Name table
        list_of_dict = connectToMySQL(DATABASE).query_db(query,data) # make sure to call the connectToMySQL function with the schema you are targeting.
        
        if not list_of_dict:
            return []

        article = cls(list_of_dict[0])
        user_data = {
            **list_of_dict[0], #Including the non-conflicting columns
            'id' :list_of_dict[0]['users.id'],
            'created_at' :list_of_dict[0]['users.created_at'],
            'updated_at' :list_of_dict[0]['users.updated_at']
        }
        user_instance = users_model.User(user_data)
        article.user_instance = user_instance
        return article

    @classmethod
    def update_one(cls, data):
        print(data)
        query = "UPDATE articles SET name=%(name)s,content=%(content)s, author=%(author)s, header=%(header)s  WHERE id = %(id)s;" #TODO Name table, column, and value
        return connectToMySQL(DATABASE).query_db(query, data) #Returns "None"
    
    @classmethod
    def delete_one(cls, id:dict):
        query = "DELETE FROM articles WHERE id = %(id)s;" #TODO Name table
        return connectToMySQL(DATABASE).query_db(query, id) #Returns "None"
        
    @staticmethod
    def validate_image(stream):
        header = stream.read(512)
        stream.seek(0) 
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')

    @staticmethod
    def validator(data:dict) -> bool:
        is_valid = True
        if (len(data['name']) == 0):
            flash('Name is required','err_articles')
            is_valid = False 
        elif (len(data['name']) < 3):
            flash('Name is too short','err_articles')
            is_valid = False 

        if (len(data['header']) == 0):
            flash('Header is required','err_articles')
            is_valid = False 
        elif (len(data['header']) < 3):
            flash('Header is too short','err_articles')
            is_valid = False 

        if (len(data['content']) == 0):
            flash('Content is required','err_articles')
            is_valid = False 
        elif (len(data['content']) < 3):
            flash('Content is too short','err_articles')
            is_valid = False 

        if (len(data['author']) == 0):
            flash('Author is required','err_articles')
            is_valid = False 
        elif (len(data['author']) < 3):
            flash('Author is too short','err_articles')
            is_valid = False 

        return is_valid