from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from db.config import configure
from flask_jwt_extended import JWTManager
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

UPLOAD_FOLDER = '/path/to/the/uploads'

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
jwt = JWTManager(app)
setup_database = configure(app)
db = SQLAlchemy(setup_database)
migrate = Migrate(app, db)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.before_first_request
def create_tables():
  db.create_all()


import models
import UserResource, JwtResource, GmudResource, EmissorResource, FileResource

api.add_resource(UserResource.UserLogin, '/login')
api.add_resource(UserResource.UserRegistration, '/registration')
api.add_resource(JwtResource.TokenRefresh, '/token/refresh')
api.add_resource(JwtResource.UserLogoutRefresh, '/logout')
api.add_resource(GmudResource.GmudResource, '/gmuds')
api.add_resource(EmissorResource.EmissorResource, '/emissores')
api.add_resource(FileResource.FileResource, '/upload')


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenUser.is_jti_blacklisted(jti)