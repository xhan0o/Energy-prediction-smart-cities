from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(120))
    username = db.Column(db.String(80))
    totalUsage = db.Column(db.String(120))


    def __init__(self, username, totalUsage, timestamp):
        self.username = username
        self.totalUsage = totalUsage
        self.timestamp = timestamp


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'totalUsage','timestamp')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    print request.json
    username = request.json['username']
    totalUsage = request.json['totalUsage']
    timestamp = request.json['timestamp']

    new_user = User(username, totalUsage, timestamp)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(**request.json)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
