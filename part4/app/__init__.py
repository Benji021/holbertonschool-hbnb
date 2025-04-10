import os
from flask import Flask, render_template
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.extensions import bcrypt, jwt, db
from app.database import init_db, seed_db

def create_app(config_class="config.DevelopmentConfig"):
    # Define path file Templates and Static
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')

    # Déboguer les chemins
    print("TEMPLATE_DIR:", TEMPLATE_DIR)  # Affiche le chemin pour vérifier si c'est correct
    print("STATIC_DIR:", STATIC_DIR)  # Affiche le chemin des fichiers statiques

    # Déboguer les fichiers dans templates
    print("Files in TEMPLATE_DIR:", os.listdir(TEMPLATE_DIR))

    # Create the Flask application, specifying folders for templates and static files
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/swagger')
    bcrypt.init_app(app=app)
    jwt.init_app(app=app)
    db.init_app(app)
    with app.app_context():
        init_db()
        seed_db()
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Define a route for the home page
    @app.route('/')
    def home():
        print("Rendering index.html...")
        return render_template('index.html')
    
    return app