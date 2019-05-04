from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from db.config import configure
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)
setup_database = configure(app)
db = SQLAlchemy(setup_database)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


import models
import UserResource, JwtResource

api.add_resource(UserResource.UserLogin, '/login')
api.add_resource(UserResource.UserRegistration, '/registration')
api.add_resource(JwtResource.TokenRefresh, '/token/refresh')
api.add_resource(JwtResource.UserLogoutRefresh, '/logout')