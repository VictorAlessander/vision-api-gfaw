from flask_restful import reqparse, Resource
from flask import request
from models import File


class FileResource(Resource):


  def __init__(self):

    self.parser = reqparse.RequestParser()

    self.parser.add_argument(
      'document',
      required=True,
      location='json',
      help='Cade o arquivo?'
    )

    self.parser.add_argument(
      'user_id',
      required=True, 
      location='json',
      help='Id do usuario responsavel do documento nao pode ser vazio'
    )

  def post(self):
    data = self.parser.parse_args()

    new_file = File(
      document=data['document'],
      user_id=data['user_id']
    )

    try:
      new_file.save()
    except Exception as err:
      print(err)
      return {'message': 'DEU RUIM'}

  def get(self):
    if 'id' in requests.args:
      return File.find_file_by_id(request.args['id'])
    else:
      return File.retrieve_all_files()

  def put(self):
    data = self.parser.parse_args()

    doc = File.get_file_by_id(data['id'])

    if doc:
      doc.document = data['document']
      doc.user_id = data['user_id']
      try:
        doc.save()
      except Exception as err:
        print(err)
        return {'message': 'DEU RUIM'}
    else:
      return {'message': 'Arquivo nao encontrado'}  

  def delete(self):
    if 'id' in requests.args:
      try:
        File.remove(requests.args['id'])
      except Exception as err:
        print(err)
        return {'message': 'DEU RUIM'}, 500
    else:
      return {'message': 'BAD REQUEST'}, 400