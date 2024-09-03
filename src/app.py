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
from models import db, User, Person, PersonFavorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

    users = User.query.all()

    return jsonify([user.serialize() for user in users]), 200

@app.route('/people', methods=['GET'])
def get_all_people():

    people = Person.query.all()

    return jsonify([person.serialize() for person in people]), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_all_user_favorites(user_id):

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "user not found"}), 404

    user_favorites = [person.serialize() for person in user.person_favorites]
    return jsonify({"data": user_favorites}), 200



@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    user_id = request.json.get('user_id')
    favorite = PersonFavorite(user_id=user_id, person_id=person_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(person_id):
    user_id = request.json.get('user_id')
    favorite = PersonFavorite.query.filter_by(user_id=user_id, person_id=person_id).first_or_404() 
    db.session.delete(favorite)
    db.session.commit()
    return '' , 204  

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)