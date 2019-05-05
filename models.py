from main import db
from passlib.hash import pbkdf2_sha256 as sha256
import datetime


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  documents = db.relationship('File', backref='user')

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

  
class File(db.Model):

  __tablename__ = 'files'

  
  id = db.Column(db.Integer, primary_key=True)
  # responsavel = db.Column(db.String(80), unique=False, nullable=False)
  document = db.Column(db.String(120), unique=False, nullable=False)
  data = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users'), lazy=True)

  def save(self):
  db.session.add(self)
  db.session.commit()    

  @classmethod
  def find_file_by_id(cls, id):
    return File.query.filter_by(id=id).first()

  def remove(self, id):
    doc = File.find_file_by_id(id = id)
    if doc:
      db.session.delete(doc)
      db.session.commit()
      return {'message': 'Arquivo deletado'}
    else
      return {'message': 'Arquivo nao encontrado'}  

  @classmethod
  def retrieve_all_files(cls):
    def to_json(arg):
      return {
        'id': arg.id,
        'document': arg.document,
        'data': arg.data,
        'user_id': arg.user_id
      }
  
    return {'arquivos': list(map(lambda x: to_json(x), File.query.all()))}
