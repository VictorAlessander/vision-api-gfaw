from flask_restful import reqparse, Resource
from models import Gmud


class GmudResource(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser()

    self.parser.add_argument(
      'numero',
      required=True,
      location='json',
      help='Numero da gmud nao pode ser vazio'
    )

    self.parser.add_argument(
      'descricao',
      required=True,
      location='json',
      help='Descricao da gmud nao pode ser vazio'
    )

    self.parser.add_argument(
      'responsavel',
      required=True,
      location='json',
      help='Responsavel da gmud nao pode ser vazio'
    )

    self.parser.add_argument(
      'status',
      required=False,
      location='json',
      help='Status da gmud'
    )

    self.parser.add_argument(
      'versionamento',
      required=False,
      location='json',
      help='Versionamento da gmud'
    )

    self.parser.add_argument(
      'status'
    )

  def get(self):
    return Gmud.retrieve_all_gmuds()

  def post(self):
    data = self.parser.parse_args()

    new_gmud = Gmud(
      numero=data['numero'],
      descricao=data['descricao'],
      responsavel=data['responsavel'],
      status=data['status'],
      versionamento=['versionamento'],
      plano_execucao=['plano_execucao'],
      plano_reversao=data['plano_reversao'],
      evidencias=data['evidencias'],
      referencia_externa=data['referencia_externa']
    )

    try:
      new_gmud.save()
    except Exception as err:
      print(err)
      return {'message': 'Algo esta incorreto'}

  def put(self):
    data = self.parser.parse_args()

    gmud = Gmud.get_gmud_by_id(data['id'])

    if gmud:
      gmud.numero = data['numero']
      gmud.descricao = data['descricao']
      gmud.responsavel = data['responsavel']
      gmud.versionamento = data['versionamento']
      gmud.status = data['status']
      gmud.versionamento = data['versionamento']
      gmud.plano_execucao = data['plano_execucao']
      gmud.plano_reversao = data['plano_reversao']
      gmud.evidencias = data['evidencias']
      gmud.referencia_externa = data['referencia_externa']

      try:
        gmud.save()
      except Exception as err:
        print(err)
        return {'message': 'Algo esta incorreto'}
    else:
      return {'message': 'Gmud nao encontrada'}

  def delete(self):
    data = self.parser.parse_args()
