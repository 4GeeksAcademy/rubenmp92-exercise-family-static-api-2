"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    if members is None:
        return jsonify ("La persona no existe"),404
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()   #va a coger toda la información del body postman
    if "first_name" not in body:
        return jsonify("Falta el campo first_name"),400
    if "age" not in body:
        return jsonify("Falta el campo age"),400
    if "lucky_numbers" not in body:
        return jsonify("Falta el campo lucky_numbers"),400
    if "id" in body:
        id = body["id"]
    else:
        id = jackson_family._generateId()

    new_member = {
            "id": id,
            "first_name": body["first_name"],
            "last_name": jackson_family.last_name,
            "age": body["age"],
            "lucky_numbers": ["lucky_mumbers"]
    }
    jackson_family.add_member(new_member)
    print(body)
    return jsonify ("add member completed"), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if (member == None):
        return jsonify("El miembro no existe"), 404
    print(id)
    return jsonify(member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
