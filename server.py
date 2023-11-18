from flask_app import app
from flask import render_template
#For every controller file, add below with commas
from flask_app.controllers import routes, users_controller, article_controller,planet_controller

#This is always at the bottom!
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.