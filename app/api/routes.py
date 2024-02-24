from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Quarterback, qb_schema, qbs_schema
# import uuid

api = Blueprint('api', __name__, url_prefix="/api")

@api.route('/quarterbacks', methods = ['POST'])
@token_required
def create_qb(current_user_token):
    team = request.json['team']
    user_token = current_user_token.token

    if not user_token:
        return jsonify({"error" : "Missing user token"}), 400

    try:
        if team in qb_info:
            div_conf_tpl, image_link = qb_info[team] 
            division, conference = div_conf_tpl   
        else:
            division = request.json['division']
            conference = request.json['conference']
            image_link = request.json['image_link']
    
    except KeyError:

        return jsonify({"error":"No team with that name found; check your spelling"}, "error")

    qb = Quarterback(team, division, conference, image_link, user_token=user_token)
    print(qb)

    db.session.add(qb)
    db.session.commit()

    response = qb_schema.dump(qb)
    return jsonify(response), 201

@api.route('/quarterbacks', methods = ['GET'])
@token_required
def get_qbs(current_user_token):
    a_user = current_user_token.token
    qbs = Quarterback.query.filter_by(user_token = a_user).all()
    response = qbs_schema.dump(qbs)
    return jsonify(response), 200

@api.route('/quarterbacks/<id>', methods = ['GET'])
@token_required
def get_single_qb(current_user_token, id):
    qb = Quarterback.query.get(id)
    response = qb_schema.dump(qb)
    return jsonify(response)

@api.route('/quarterbacks/<id>', methods = ['POST', 'PUT'])
@token_required
def update_qb(current_user_token, id):
    qb = Quarterback.query.get(id)
    qb.team = request.json["team"]
    qb.division = request.json["division"]
    qb.conference = request.json["conference"]
    qb.image_link = request.json["image_link"]
    qb.user_token = current_user_token.token

    db.session.commit()
    response = qb_schema.dump(qb)
    return jsonify(response), 200

@api.route('/quarterbacks/<id>', methods = ['DELETE'])
@token_required
def delete_qb(current_user_token, id):
    qb = Quarterback.query.get(id)

    db.session.delete(qb)
    db.session.commit()
    response = qb_schema.dump(qb)
    return jsonify(response)










qb_info = {
'bills': [('afc east', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723457/bills_zplcjn.png'],
'dolphins': [('afc east', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723459/dolphins_zb2b7t.png'],
'patriots': [('afc east', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/patriots_fsq94s.png'],
'jets': [('afc east', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/jets_a4bf2m.png'],
'ravens': [('afc north', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723455/ravens_es66tt.png'],
'bengals': [('afc north', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723457/bengals_o86yah.png'],
'browns': [('afc north', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723457/browns_qy2qtb.png'],
'steelers': [('afc north', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723455/steelers_ur8yws.png'],
'texans': [('afc south', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723455/texans_tbls1s.png'],
'colts': [('afc south', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723458/colts_bz0vpq.png'],
'jaguars': [('afc south', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/jaguars_em5o3b.png'],
'titans': [('afc south', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723455/titans_kp7tbf.png'],
'broncos': [('afc west', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723457/broncoos_nbtqmh.png'],
'chiefs': [('afc west', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723458/chiefs_ugmtys.png'],
'raiders': [('afc west', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/raiders_rmijha.png'],
'chargers': [('afc west', 'afc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723458/chargers_pf0kwn.png'],
'cowboys': [('nfc east', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723458/cowboys_ubcojz.png'],
'giants': [('nfc east', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/giants_hpyx2u.png'],
'eagles': [('nfc east', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723459/eagles_h5pipx.png'],
'commanders': [('nfc east', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723458/commanders_jolwjy.png'],
'bears': [('nfc north', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723457/bears_pgcmlt.png'],
'lions': [('nfc north', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/lions_ipc9so.png'],
'packers': [('nfc north', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/packers_xi2esb.png'],
'vikings': [('nfc north', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723456/vikings_vruadw.png'],
'falcons': [('nfc south', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723459/falcons_lccovf.png'],
'panthers': [('nfc south', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/panthers_f5hybg.png'],
'saints': [('nfc south', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723455/saints_wx7t1n.png'],
'buccaneers': [('nfc south', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723457/buccaneers_c6pw7g.png'],
'cardinals': [('nfc west', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723458/cardinals_kjksgt.png'],
'rams': [('nfc west', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723454/rams_lcuxo6.png'],
'49ers': [('nfc west', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723456/49ers_zmseuz.png'],
'seahawks': [('nfc west', 'nfc'), 'https://res.cloudinary.com/dkeozpkpv/image/upload/v1708723455/seahwaks_kuvr00.png']
}