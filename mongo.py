from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongofriend'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mongofriend'

mongo = PyMongo(app)

CORS(app)


@app.route('/api/friends', methods=['GET'])
def get_all_friends():
    friends = mongo.db.friends
    result = []
    for field in friends.find():
        result.append({'_id': str(field['_id']), 'title': field['title']})
    return jsonify(result)


@app.route('/api/friend', methods=['POST'])
def add_friend():
    friends = mongo.db.friends
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = request.get_json()['password']
    birth_date = request.get_json()['birth_date']

    friend_id = friends.insert({'first_name': first_name,
                                'last_name': last_name,
                                'email': email,
                                'password': password,
                                'birth_date': birth_date})
    new_friend = friends.find_one({'_id': friend_id})
    result = {'id': new_friend['id']}
    return jsonify({'reuslt': result})


@app.route('/api/friend/<id>', methods=['PUT'])
def update_friend(id):
    friends = mongo.db.friends
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = request.get_json()['password']
    birth_date = request.get_json()['birth_date']

    friends.find_one_and_update({'_id': ObjectId(id)}, {
        "$set": {'first_name': first_name,
                 'last_name': last_name,
                 'email': email,
                 'password': password,
                 'birth_date': birth_date
                 }}, upsert=False)
    new_friend = friends.find_one({'_id': ObjectId(id)})
    result = {'id': new_friend['id']}
    return jsonify({"result": result})


@app.route('/api/friend/<id>', methods=['DELETE'])
def delete_friend(id):
    friends = mongo.db.friends
    response = friends.delete_one({'_id': ObjectId(id)})
    if response.deleted_count == 1:
        result = {'message': 'record deleted'}
    else:
        result = {'message': 'no record found'}
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
