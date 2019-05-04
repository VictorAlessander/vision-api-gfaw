from main import db
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  # @classmethod
  # def find_by_username(cls):
  #   def to_json(arg):
  #     return {
  #       'id': arg.id,
  #       'username': arg.username,
  #       'password': arg.password
  #     }

  #   return {'users': list(map(lambda x: to_json(x), User.query.all()))}

  @classmethod
  def user_already_exists(cls, user):
    return True if User.query.filter(User.username == user) else False

  @staticmethod
  def generate_hash(password):
    return sha256.hash(password)

  @staticmethod
  def verify_hash(password, hash):
    return sha256.verify(password, hash)

  @classmethod
  def authenticate(cls, user, passwd):
    login = User.query.filter(User.username == user).filter(User.password == passwd)

    if login:
      return True
    
    return False