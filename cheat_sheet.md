1. mkdir hello_flask - Make directory "Hello_Flask"
2. cd hello_flask - Enters directory
3. cls - Clears screen
4. pip install pipenv - global install
5. pipenv install flask - starts pip virtual environment // installs flask
6. pip list - to show what's in your environment
7. python server.py
8. pipenv shell
9. dir - list directories


# Checklist

1. Create new folder
2. Go into folder
3. Open terminal 
    - pipenv install flask - only needs done once per project!
    - pipenv install pymysql - only needs done once per project!
    - pipenv install flask-bcrypt - only needs done once per project!
4. WARNING check for pipfile and pipfile.lock
5. launch view
    - pipenv shell -done everytime you want to start your server
6. Create folder structure
    1. Root folder 📁
        1. Flask_app 📁
            1. config 📁
                -  mysqlconnection.py 📄
            2. controllers 📁
                -  controller_name 📄
            3. models 📁
                - model.py 📄
            4. static  📁
                1. css 📁
                    -  styles 📄
                2. js 📁
                    -  script.js 📄
            5. templates 📁
                -  index.html 📄
            6. \_\_init__.py 📄
        2. pipfile 📄
        3. pipfile.lock 📄
        4. server.py 📄
7. Add boilerplate code
8. run python server.py
9. Test

# My file Boilerplates
## mysqlconnection.py
```py
# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = False)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query:str, data:dict=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
```
## \_\_init__ file
```py
from flask import Flask  # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
app.secret_key = "Keep it safe"
DB = "your DB name here"

```
## server.py
```py
from flask_app import app
#For every controller file, add below 
from flask_app.controllers import controller_name


#This is always at the bottom!
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.
```


## controller.py
```py
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.model_name import Classname

@app.route('/')
def hello_world():
    return 'Hello World!'  


#CRUD #TODO ASSIGN TABEL NAME IN FUNCTION NAMES AND URLS
@app.route('/TABLE_NAME/new') 
def TABLE_NAME_new(): 
    #Function actions
    return render_template('TABLE_NAME_new.html') #TODO ASSIGN HTML FILE

@app.route('/TABLE_NAME/create') 
def TABLE_NAME_create(): 
    #Function actions
    return redirect('NEW ROUTE AFTER CREATE') #redirect #TODO ADD ROUTE FOR REDIRECT

@app.route('/TABLE_NAME/id') 
def TABLE_NAME_id(): 
    #Function actions
    return render_template('TABLE_NAME_id.html') #TODO ASSIGN HTML FILE

@app.route('/TABLE_NAME/id/edit') 
def TABLE_NAME_id_edit(): 
    #Function actions
    return render_template('TABLE_NAME_id_edit.html') #TODO ASSIGN HTML FILE

@app.route('/TABLE_NAME/id/update')
def TABLE_NAME_id_update(): 
    #Function actions
    return redirect('NEW ROUTE AFTER UPDATE') #TODO ADD ROUTE FOR REDIRECT

@app.route('/TABLE_NAME/id/delete') E
def TABLE_NAME_id_delete(): 
    #Function actions
    return redirect('NEW ROUTE AFTER DELETION') #TODO ADD ROUTE FOR REDIRECT



# /Tablename/id?/action
# 1. /tablename/new -> Display \\ Displaying the form to create a new row
# 2. /tablename/create -> Redirect \\ Processing the data from the form from the new route
# 3. /tablename/id -> Display \\ Show route, this route displays the SINGLE ITEM with the id
# 4. /tablename/id/edit -> Display \\ This is a display route that shows the form to edit the row information
# 5. /tablename/id/update -> Redirect \\ The route that processes the form from the edit route
# 6. /tablename/id/delete -> Redirect \\ This is the route that 
```



## model.py file
```py
# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
class Friend:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #No commas here or -> tuple!
        #TODO Add additional columns from database here


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM friends;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('first_flask').query_db(query)
        # Create an empty list to append our instances of friends
        all_friends = []
        #Safety
        if not results:
            return = []
        # Iterate over the db results and create instances of friends with cls.
        for friend in results:
            all_friends.append( cls(friend) )
        return all_friends
            
```


```html
<label for="NAME">NAME</label>
<input type="text" name="NAME" id="NAME">
{% for message in get_flashed_messages(category_filter=['err_NAME_NAME']) %}
<p class="err-msg">{{message}}</p>
{% end for%}
```