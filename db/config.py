
def configure(app):

  user = 'postgres_user'
  passwd = 'postgres_password'
  host = '192.168.10.201'
  port = 5432
  database = 'visiondb'

  app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{passwd}@{host}:{port}/{database}'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  return app