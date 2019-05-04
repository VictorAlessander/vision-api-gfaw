from main import db
from passlib.hash import pbkdf2_sha256 as sha256
import datetime


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def retrieve_user(cls, user):
    return User.query.filter_by(username=user).first()

  @classmethod
  def user_already_exists(cls, user):
    return True if User.query.filter(User.username == user).first() else False

  @staticmethod
  def generate_hash(password):
    return sha256.hash(password)

  @staticmethod
  def verify_hash(password, hash):
    return sha256.verify(password, hash)


class RevokedTokenUser(db.Model):

  __tablename__ = 'revoked_tokens'

  id = db.Column(db.Integer, primary_key=True)
  jti = db.Column(db.String(120))

  def add(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def is_jti_blacklisted(cls, jti):
    query = cls.query.filter_by(jti=jti).first()
    return bool(query)


class Gmud(db.Model):

  __tablename__ = 'gmuds'

  id = db.Column(db.Integer, primary_key=True)
  numero = db.Column(db.String(30), unique=True, nullable=False)
  responsavel = db.Column(db.String(80), unique=False, nullable=False)
  data = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)


  def save(self):
    db.session.add(self)
    db.session.commit()