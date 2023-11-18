import os
import imghdr
from flask import render_template, redirect, request, session, url_for, abort, send_from_directory
from flask_app import app, bcrypt
from flask_app.models.articles_model import Article #TODO Add classname Add model name
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt        
from werkzeug.utils import secure_filename
import datetime
bcrypt = Bcrypt(app)

#CRUD #TODO ASSIGN TABEL NAME IN FUNCTION NAMES AND URLS
@app.route('/articles/all')
def articles_all():
    if session.get('user_id') == None:
        return redirect('/login/page')
    articles = Article.get_all_join()
    # date_uploaded = datetime.datetime.strptime(articles['created_at'],'%Y-%m-%d')
    return render_template('article_dashboard.html', articles=articles)

@app.post('/articles/search')
def articles_all_search():
    if session.get('user_id') == None:
        return redirect('/login/page')
    articles = Article.get_all_join_search(request.form)
    search_term = request.form['search']
    return render_template('articles_search.html', articles=articles, search_term=search_term)

@app.route('/articles/new') 
def articles_new(): 
    if session.get('user_id') == None:
        return redirect('/login/page')
    return render_template('article_new.html') #TODO ASSIGN HTML FILE

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/articles/create', methods=['POST']) #TODO add table name
def articles_create():
    if session.get('user_id') == None:
        return redirect('/login/page')

    is_valid = Article.validator(request.form)
    if not is_valid:
        return redirect('/articles/new')

    uploaded_file = request.files['photo']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != Article.validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    data = {
        **request.form,
        'photo': filename,
        'user_id': session['user_id']
    }
    new_row_id = Article.create(data)
    return redirect("/articles/all") #TODO add route

@app.route('/articles/<int:id>') 
def articles_one(id): 
    if session.get('user_id') is None:
        return redirect('/login/page')
    user = User.get_one({'id': session['user_id']})
    if user['id'] != session['user_id']:
        return redirect('/articles/all')
    article = Article.get_one_join({'id': id})
    return render_template('article_view.html', article=article) #TODO ASSIGN HTML FILE

@app.route('/articles/<int:id>/edit') 
def articles_one_edit(id): 
    if session.get('user_id') is None:
        return redirect('/login/page')
    
    user = User.get_one({'id': session['user_id']})
    if user['id'] != session['user_id']:
        redirect('/articles/all')
    
    article = Article.get_one({'id': id}) #To prepolulate article information
    return render_template('article_edit.html', article=article) #TODO ASSIGN HTML FILE

@app.post('/articles/<int:id>/update')
def articles_one_update(id): 
    if session.get('user_id') is None:
        return redirect('/login/page')
    
    user = User.get_one({'id': session['user_id']})
    if user['id'] != session['user_id']:
        return redirect('/articles/all')
    
    is_valid = Article.validator(request.form)
    if not is_valid:
        return redirect(f'/articles/{id}/edit')
    
    data = {
        **request.form,
        'user_id': session['user_id'],
        'id': id
    }
    
    nothing = Article.update_one(data)
    return redirect('/articles/all')

@app.route('/articles/<int:id>/delete')
def articles_one_delete(id): 
    if session.get('user_id') is None:
        return redirect('/login/page')
    
    user = User.get_one({'id': session['user_id']})
    if user['id'] != session['user_id']:
        return redirect('/articles/all')
    
    nothing = Article.delete_one({'id': id})
    return redirect('/articles/all')
