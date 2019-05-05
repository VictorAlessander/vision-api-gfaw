from flask_restful import reqparse, Resource
from models import Emissor


class EmissorResource(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser()

    self.parser.add_argument(
      'nome',
      required=True,
      location='json',
      help='Nome do emissor nao pode estar vazio'
    )

    self.parser.add_argument(
      'servidor',
      required=True,
      location='json',
      help='Servidor do emissor nao pode estar vazio'
    )

    self.parser.add_argument(
      'nome_base',
      required=True,
      location='json',
      help='Nome da base do emissor nao pode estar vazio'
    )

    self.parser.add_argument(
      'usuario_db',
      required=True,
      location='json',
      help='Usuario do emissor nao pode estar vazio'
    )

    self.parser.add_argument(
      'senha_db',
      required=True,
      location='json',
      help='Senha do emissor nao pode estar vazio'
    )

  def get(self):
    return Emissor.retrieve_all_emissores()

  def post(self):
    data = self.parser.parse_args()

    new_emissor = Emissor(
      nome=data['nome'],
      servidor=data['servidor'],
      nome_base=data['nome_base'],
      usuario_db=data['usuario_db'],
      senha_db=data['senha_db']
    )

    try:
      new_emissor.save()
      return {'message': 'Emissor salvo com sucesso'}
    except Exception as err:
      print(err)
      return {'message': 'Algo esta incorreto'}, 500

  def put(self):
    data = self.parser.parse_args()

    emissor = Emissor.get_emissor_by_id(data['id'])

    if emissor:
      emissor.nome = data['nome']
      emissor.servidor = data['servidor']
      emissor.nome_base = data['nome_base']
      emissor.usuario_db = data['usuario_db']
      emissor.senha_db = data['senha_db']

      try:
        emissor.save()
        return {'message': 'Emissor salvo com sucesso'}
      except Exception as err:
        print(err)
        return {'message': 'Algo esta incorreto'}, 500
    else:
      return {'message': 'Emissor nao encontrado'}

  def delete(self):
    data = self.parser.parse_args()

    Emissor.remove(data['id'])