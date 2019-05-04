from flask_restful import reqparse, Resource


class GmudResource(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser()

    self.parser.add_argument(
      'numero',
      required=True,
      location='json',
      help='Numero da gmud nao pode estar vazio'
    )

    self.parser.add_argument(
      'descricao',
      required=True,
      location='json'
      help='Descricao nao pode ser vazio'
    )

    self.parser.add_argument(
      'responsavel',
      required=True,
      location='json',
      help='Responsavel nao pode ser vazio'
    )