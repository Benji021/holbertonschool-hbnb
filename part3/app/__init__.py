from flask import Flask, jsonify, request
from flask_restx import Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity # Import the JWT manager
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.services import HBnBFacade

facade = HBnBFacade()

def create_app():
    app = Flask(__name__)

    app.config["DEBUG"] = True  # Activate debug mode

    # Configure secret key for JWT
    app.config['JWT_SECRET_KEY'] = 'my_secret_key' # Replaces with a more secure key

    # Initialize the JWT manager
    jwt = JWTManager(app)

    # JWT error handling
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Le token a expiré"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"msg": "Token invalide"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"msg": "Token manquant"}), 401

    # Create API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Create a connection endpoint
    @app.route('/login', methods=['POST'])
    def login():

        # Retrieve user credentials sent in the request body
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        # Check identifiers (replace this logic with a real check in your DB)
        user = facade.authenticate_user(email, password)

        if not user:
            return jsonify({"msg": "Identifiants invalides"}), 401

        # Use user ID as identity in token
        access_token = create_access_token(identity=user.id)

        return jsonify(access_token=access_token), 200


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)  