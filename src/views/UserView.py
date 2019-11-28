from flask import request, Response, json, Blueprint, g

from ..models.UserModel import UserModel, UserShcema
from ..shared.Authentication import Auth

user_api = Blueprint('user', __name__)
user_schema = UserShcema()


@user_api.route('/add', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = user_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {__json_data(400, None, 'User already exist, please supply another email address')}
        return custom_response(message, 400)

    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user).data

    token = Auth.generate_token(ser_data.get('id'))

    json_datas = {}
    t = {}

    t['jwt_token'] = token
    json_datas['status'] = 200
    json_datas['result'] = t
    json_datas['error'] = None

    return custom_response(json_datas, 201)


@user_api.route('/all', methods=['GET'])
@Auth.auth_required
def get_all():
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True).data

    json_data = {
        'status': 200,
        'result': ser_users,
        'error': None
    }

    return custom_response(json_data, 200)


@user_api.route('/login', methods=['POST'])
def login():
    json_datas = {}

    req_data = request.get_json()

    data, error = user_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    if not data.get('email') or not data.get('password'):
        return custom_response(__json_data(400, None, 'you need email and password to sign in'), 400)

    user = UserModel.get_user_by_email(data.get('email'))

    if not user:
        return custom_response(__json_data(400, None, 'invalid credentials'), 400)

    if not user.check_hash(data.get('password')):
        return custom_response(__json_data(400, None, 'invalid credentials'), 400)

    ser_data = user_schema.dump(user).data

    token = Auth.generate_token(ser_data.get("id"))

    t = {"jwt_token": token}
    json_datas['status'] = 200
    json_datas['result'] = t
    json_datas['error'] = None

    return custom_response(json_datas, 200)


@user_api.route('/me?id=<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response(__json_data(404, None, 'User not found'), 404)

    ser_user = user_schema.dump(user).data

    return custom_response(__json_data(200, ser_user, None), 200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(__json_data(400, None, error), 400)

    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user).data

    return custom_response(__json_data(200, ser_user, None), 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response(__json_data(204, 'User has been deleted', None), 204)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user).data
    return custom_response(__json_data(200, ser_user, None), 200)

def __json_data(status, data, error):
    json_res = {
        'status': status,
        'result': data,
        'error': error
    }
    return json_res


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
