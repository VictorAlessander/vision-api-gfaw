from main import db
from passlib.hash import pbkdf2_sha256 as sha256
import datetime


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  documents = db.relationship('File', backref='user', lazy=True)

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
  descricao = db.Column(db.String(120), unique=False, nullable=False)
  responsavel = db.Column(db.String(80), unique=False, nullable=False)
  data = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
  status = db.Column(db.Boolean)
  versionamento = db.Column(db.Text, unique=False, nullable=True)
  plano_execucao = db.Column(db.String(100), unique=False, nullable=False)
  plano_reversao = db.Column(db.String(100), unique=False, nullable=False)
  evidencias = db.Column(db.String(120), unique=False, nullable=False)
  referencia_externa = db.Column(db.String(120), unique=True, nullable=False)
  emissor_id = db.Column(db.Integer, db.ForeignKey('emissores.id'), nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def remove(cls, id):
    gmud = Gmud.get_gmud_by_id(id)
    db.session.delete(gmud)
    db.session.commit()

  @classmethod
  def get_gmud_by_id(cls, id):
    return Gmud.query.filter_by(id=id).first()

  @classmethod
  def retrieve_all_gmuds(cls):
    def to_json(arg):
      return {
        'id': arg.id,
        'numero': arg.numero,
        'responsavel': arg.responsavel,
        'data': str(arg.data),
        'status': arg.status,
        'versionamento': arg.versionamento,
        'plano_execucao': arg.plano_execucao,
        'plano_reversao': arg.plano_reversao,
        'evidencias': arg.evidencias,
        'referencia_externa': arg.referencia_externa,
        'emissor_id': arg.emissor_id
      }
  
    return {'gmuds': list(map(lambda x: to_json(x), Gmud.query.all()))}


class Emissor(db.Model):

  __tablename__ = 'emissores'

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False, unique=True)
  servidor = db.Column(db.String(100), nullable=False, unique=False)
  nome_base = db.Column(db.String(80), nullable=False, unique=True)
  usuario_db = db.Column(db.String(90), nullable=False, unique=False)
  senha_db = db.Column(db.String(100), nullable=False, unique=False)
  gmuds = db.relationship('Gmud', backref='emissor', lazy=True)


  def save(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def remove(cls, id):
    emissor = Emissor.get_emissor_by_id(id)
    db.session.delete(emissor)
    db.session.commit()

  @classmethod
  def get_emissor_by_id(cls, id):
    return Emissor.query.filter_by(id=id).first()

  @classmethod
  def retrieve_all_emissores(cls):
    def to_json(arg):
      return {
        'id': arg.id,
        'nome': arg.nome,
        'servidor': arg.servidor,
        'nome_base': arg.nome_base,
        'usuario_db': arg.usuario_db,
        'senha_db': arg.senha_db
      }

    return {'emissores': list(map(lambda x: to_json(x), Emissor.query.all()))}


class File(db.Model):

  __tablename__ = 'files'

  id = db.Column(db.Integer, primary_key=True)
  document = db.Column(db.String(120), unique=False, nullable=False)
  data = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  extension = db.Column(db.String(8), nullable=False)

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
    else:
      return {'message': 'Arquivo nao encontrado'} 

  @classmethod
  def retrieve_all_files(cls):
    def to_json(arg):
      return {
        'id': arg.id,
        'document': arg.document,
        'data': arg.data,
        'user_id': arg.user_id,
        'extension': arg.extension
      }
  
    return {'arquivos': list(map(lambda x: to_json(x), File.query.all()))}