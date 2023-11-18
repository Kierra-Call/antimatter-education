# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app import bcrypt

# model the class after the friend table from our database
class Planet: #TODO rename clas. Pascel case
    def __init__( self , data:dict ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.description = data['description']
        self.planet_link = data['planet_link']
        #No commas here or -> tuple!

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO planets(name, description, planet_link) VALUE (%(name)s, %(description)s,%(planet_link)s);" #TODO Name table, columns, and values  #When using %()s, you must pass in data
        new_row_id= connectToMySQL(DATABASE).query_db(query,data) #Returns back an INT, the ID of the row inserted
        return new_row_id

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM planets WHERE name = %(name)s;" #TODO Name table
        id_to_display = connectToMySQL(DATABASE).query_db(query,data)
        return id_to_display[0]

