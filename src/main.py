"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Favorite_Character, Favorite_Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.filter().all()
    print(users)
    result = list(map(lambda user: user.serialize(), users))
    print(result)
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(result), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    print(user)
    print(user.serialize())
    
    result = {
        "msg": f'número de usuario: {user_id}'
    }

    return jsonify(user.serialize()), 200

@app.route('/favoriteplanets/<int:planet_id>', methods=['POST'])
def add_favplan(planet_id):
    request_body=json.loads(request.data)




@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.filter().all()
    print(planets)
    result = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    result = {
        "msg": f'número de planeta: {planet_id}'
    }
    return jsonify(planet.serialize()), 200 

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.filter().all()
    result = list(map(lambda characters: characters.serialize(), characters))

    return jsonify(result), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.get(character_id)    
    result = {
        f'número de usuario: {character_id}'
    }

    return jsonify(character.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
