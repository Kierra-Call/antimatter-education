from flask import Flask  # Import Flask to allow us to create our app
from flask_bcrypt import Bcrypt
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg','.png']
app.config['UPLOAD_PATH'] = 'flask_app/static/assets/uploads'
bcrypt = Bcrypt(app)
app.secret_key = "Keep it safe"
DATABASE = "antimatter_education_schema"
