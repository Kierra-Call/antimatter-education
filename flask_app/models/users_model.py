# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')
# model the class after the friend table from our database
class User: #TODO rename clas. Pascel case
    def __init__( self , data:dict ):
        self.id = data['id'] #TODO remove/add columns needed from table
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #No commas here or -> tuple!
        #TODO Add additional columns from database here

    @classmethod
    def get_one_by_email(cls, data:dict):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)

        if not results:
            return []

        if len(results) < 1:
            return False

        dict = results[0]
        instance = cls(dict)
        return instance

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM TABLE_NAME;" #TODO Name table
        results = connectToMySQL(DATABASE).query_db(query) # make sure to call the connectToMySQL function with the schema you are targeting.
        all_users = [] # Create an empty list to append our instances of users
        for user in results: # Iterate over the db results and create instances of users with cls.
            all_users.append( cls(user) )
        return all_users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;" #TODO Name table
        id_to_display = connectToMySQL(DATABASE).query_db(query,data)
        return id_to_display[0]

    @classmethod
    def update_one(cls, data):
        query = "UPDATE TABLE_NAME SET COLUMN_NAME=%(VALUE)s WHERE id = %(id)s;" #TODO Name table, column, and value
        return connectToMySQL(DATABASE).query_db(query, data) #Returns "None"

    @classmethod
    def delete_one(cls, id:dict):
        query = "DELETE TABLE_NAME WHERE id = %(id)s;" #TODO Name table
        return connectToMySQL(DATABASE).query_db(query, id) #Returns "None"

    #Validators
    @staticmethod
    def validate_register(data:dict) -> bool:
        is_valid = True
        print(data)
        #run through some if checks -> come to be bad, then is_valid = False
        #TODO add validations!
        if len(data['first_name']) < 2:
            flash('First Name Too Short',"err_users_first_name")
            print("I AM FALSE")
            is_valid = False 

        if len(data['last_name']) < 2:
            flash('Last Name Too Short','err_users_last_name')
            is_valid = False 

        if len(data['password']) < 2:
            flash('Password Too Short','err_users_password')
            is_valid = False 

        if data['password'] != data['confirm_password']:
            flash('Passwords do not match','err_users_confirm_password')
            is_valid = False 

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "err_users_email")
            is_valid = False 

        if is_valid:
            if not PASSWORD_REGEX.match(data['password']): 
                flash("Password must have a minimum eight characters, at least one upper case English letter, one lower case English letter, one number and one special character", "err_users_password")
                is_valid = False 

        if is_valid:
            potential_user = User.get_one_by_email(data)
            if potential_user:
                flash('Email is already in use!','err_users_email')
                is_valid = False

            print("******I am valid from registration validator!******")

        return is_valid