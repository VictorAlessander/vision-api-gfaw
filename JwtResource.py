from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, create_access_token

class UserLogoutRefresh(Resource):
  @jwt_refresh_token_required
  def post(self):
    jti = get_raw_jwt()['jti']

    try:
      revoked_token = RevokedTokenUser(jti)
      revoked_token.add()

      return {'message': 'Token revogado'}
    except Exception as err:
      print(err)
      return {'message': 'Algo está errado'}, 500


class TokenRefresh(Resource):
  @jwt_refresh_token_required
  def post(self):
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return {'access_token': access_token}