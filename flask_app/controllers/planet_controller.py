from flask import render_template, redirect, request, session
from flask_app import app, bcrypt
from flask_app.models.articles_model import Article #TODO Add classname Add model name
from flask_app.models.users_model import User
from flask_app.models.planets_model import Planet
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/the-solar-system')
def solar():
    return render_template('solar_system.html')

@app.route('/planet/<name>')
def planet_one(name):
    planet = Planet.get_one({'name': name})
    return render_template('planet_view.html', planet=planet)

#CRUD #TODO ASSIGN TABEL NAME IN FUNCTION NAMES AND URLS
# @app.route('/TABLE_NAME/all')
# def TABLE_NAME_all():
#     #Function actions
#     return render_template('TABLE_NAME_all.html')

# @app.route('/TABLE_NAME/new') 
# def TABLE_NAME_new(): 
#     #Function actions
#     return render_template('TABLE_NAME_new.html') #TODO ASSIGN HTML FILE

# @app.route('/create', methods=['POST']) #TODO add table name
# def TABLE_NAME_create():
#     # if there are errors:
#     # We call the staticmethod on Burger model to validate
#     return redirect("/NEW_ROUTE_AFTER_CREATE") #TODO add route

# @app.route('/TABLE_NAME/<int:id>') 
# def TABLE_NAME_one(): 
#     #Function actions
#     return render_template('TABLE_NAME_id.html') #TODO ASSIGN HTML FILE

# @app.route('/TABLE_NAME/<int:id>/edit') 
# def TABLE_NAME_one_edit(): 
#     #Function actions
#     return render_template('TABLE_NAME_id_edit.html') #TODO ASSIGN HTML FILE

# @app.route('/TABLE_NAME/<int:id>/update')
# def TABLE_NAME_one_update(): 
#     #Function actions
#     is_valid = CLASSNAME.validator() #TODO change classname

#     if not is_valid:
#         return redirect('/TABLE_NAME/edit')
#     return redirect('NEW ROUTE AFTER UPDATE') #TODO ADD ROUTE FOR REDIRECT

# @app.route('/TABLE_NAME/<int:id>/delete') 
# def TABLE_NAME_one_delete(): 
#     #Function actions
#     return redirect('NEW ROUTE AFTER DELETION') #TODO ADD ROUTE FOR REDIRECT
