
def configure(app):
  app.config['SQLALCHEMY_DATABASE_URI'] = '172.17.0.2:5432'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  return app