from flask_restful import reqparse, Resource
from models import User
from flask_jwt_extended import (
  create_access_token,
  create_refresh_token,
  jwt_required,
  jwt_refresh_token_required,
  get_jwt_identity,
  get_raw_jwt
  )


class UserRegistration(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser()

    self.parser.add_argument(
      'username',
      required=True,
      location='json',
      help='Username nao pode ser nulo'
    )

    self.parser.add_argument(
      'password',
      required=True,
      location='json',
      help='Password nao pode ser nulo'
    )

  def post(self):
    data = self.parser.parse_args()

    new_user = User(
      username=data['username'],
      password=User.generate_hash(data['password'])
    )

    try:
      if User.validate_already_exists(data['username']):
        return {'message': 'O usuario ja existe'}
      else:
        new_user.save()
        return {
          'message': 'Usuario {} foi criado com sucesso'.format(data['username'])
        }
    except Exception as err:
      print(err)
      return {'message': 'Algo está incorreto'}


class UserLogin(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()

    self.parser.add_argument(
      'username',
      required=True,
      location='json',
      help='Username nao pode ser nulo'
    )

    self.parser.add_argument(
      'password',
      required=True,
      location='json',
      help='Password nao pode ser nulo'
    )

  def post(self):
    data = self.parser.parse_args()

    user = User.authenticate(data['username', data['password']])

    if user and User.verify_hash(data['password'], user.password):
      access_token = create_access_token(identity=data['username'])
      refresh_token = create_refresh_token(identity=data['username'])

      return {'access_token': access_token, 'refresh_token': refresh_token}

    else:
      return {'message': 'Usuario ou senha incorretos'}
