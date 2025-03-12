from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import auth_bp # import auth blueprint

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager() # JWTManager declaration

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb_database.db'
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    app.config.from_object(config_class)
    app.register_blueprint(auth_bp) # Register the auth blueprint

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)  # Initializing the JWTManager

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000) 