from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Quarterback, qb_schema, qbs_schema
# import uuid

api = Blueprint('api', __name__, url_prefix="/api")

@api.route('/quarterbacks', methods = ['POST'])
@token_required
def create_car(current_user_token):
    team = request.json['team']
    division = request.json['division']
    conference = request.json['conference']
    image_path = request.json['image_path']
    user_token = current_user_token.token
    print(team, division, conference, image_path, user_token)

    if not user_token:
        return jsonify({"error" : "Missing user token"}), 400

    # print(f'current_user_token.token | {current_user_token.token}')

    qb = Quarterback(team, division, conference, 'image_path', user_token=user_token)
    print(qb)

    db.session.add(qb)
    db.session.commit()

    response = qb_schema.dump(qb)
    return jsonify(response), 201