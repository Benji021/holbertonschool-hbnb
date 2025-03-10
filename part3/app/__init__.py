from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity # Import the JWT manager
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

def create_app():
    app = Flask(__name__)

    # Configure secret key for JWT
    app.config['JWT_SECRET_KEY'] = 'my_secret_key' # Replaces with a more secure key

    # Initialize the JWT manager
    jwt = JWTManager(app)

    # Create API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)  