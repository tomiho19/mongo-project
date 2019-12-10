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
    title = request.get_json()['title']

    friend_id = friends.insert({'title': title})
    new_friend = friends.find_one({'_id': friend_id})

    result = {'title': new_friend['title']}

    return jsonify({'reuslt': result})


@app.route('/api/friend/<id>', methods=['PUT'])
def update_friend(id):
    friends = mongo.db.friends
    title = request.get_json()['title']

    friends.find_one_and_update({'_id': ObjectId(id)}, {"$set": {"title": title}}, upsert=False)
    new_friend = friends.find_one({'_id': ObjectId(id)})

    result = {'title': new_friend['title']}

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
