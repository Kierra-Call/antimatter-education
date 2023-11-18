from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
# from flask_app.models. import Classname #TODO Add classname Add model name
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/register/page')
def register_page():
    return render_template('register.html')

@app.post('/register/user')
def register():
    is_valid = User.validate_register(request.form)
    # Call the save @classmethod on User
    
    print(request.form)
    if is_valid == False:
        return redirect('/register/page')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "email": request.form['email'], #TODO add all columns from Users table
        "first_name": request.form['first_name'], 
        "last_name": request.form['last_name'], 
        "password" : pw_hash
    }
    user_id = User.save(data)

    # store user id into session or other info
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect("/dashboard")

@app.route('/login/page')
def login_page():
    return render_template('login.html')

@app.post('/login')
def login():
    if session.get('user_id') is not None:
        return redirect('/')
    data = { "email" : request.form["email"] }
    user_in_db = User.get_one_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", "err_users_login")
        return redirect("/login/page")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "err_users_login")
        return redirect('/login/page')
    # if the passwords matched, we set the user_id into session
    session['first_name'] = user_in_db.first_name
    session['user_id'] = user_in_db.id
    return redirect("/")

@app.route('/logout')
def logout():
    if session.get('first_name') != None:
        print(f"deleting session first_name {session['first_name']}")
        del session['first_name']
    if session.get('user_id') != None:
        print(f"deleting session user_id {session['user_id']}")
        del session['user_id']

    print(session)
    return redirect('/')

#CRUD #TODO ASSIGN TABEL NAME IN FUNCTION NAMES AND URLS
@app.route('/users/all')
def users_all():
    #Function actions
    return render_template('TABLE_NAME_all.html') #TODO ASSIGN HTML FILE

@app.route('/TABLE_NAME/<int:id>') 
def users_one(): 
    #Function actions
    return render_template('TABLE_NAME_id.html') #TODO ASSIGN HTML FILE

@app.route('/users/<int:id>/edit') 
def users_one_edit(): 
    #Function actions
    return render_template('TABLE_NAME_id_edit.html') #TODO ASSIGN HTML FILE

@app.route('/users/<int:id>/update')
def users_one_update(): 
    #Function actions
    is_valid = CLASSNAME.validator() #TODO change classname

@app.route('/users/<int:id>/delete') 
def users_one_delete(): 
    #Function actions
    return redirect('NEW ROUTE AFTER DELETION') #TODO ADD ROUTE FOR REDIRECT
