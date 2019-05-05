from flask_restful import reqparse, Resource
from models import Gmud
from flask import request


class GmudResource(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser()

  def get(self):
    if 'id' in request.args:
      gmud = Gmud.get_gmud_by_id(request.args['id'])

      return gmud if gmud else {'message': 'Gmud nao encontrada'}
    else:
      return Gmud.retrieve_all_gmuds()

  def post(self):
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
      type=bool,
      help='Status da gmud'
    )

    self.parser.add_argument(
      'versionamento',
      required=False,
      location='json',
      help='Versionamento da gmud'
    )

    self.parser.add_argument(
      'plano_execucao',
      required=True,
      location='json',
      help='Plano de execucao da gmud nao pode estar vazio'
    )

    self.parser.add_argument(
      'plano_reversao',
      required=True,
      location='json',
      help='Plano de reversao da gmud nao pode estar vazio'
    )

    self.parser.add_argument(
      'evidencias',
      required=True,
      location='json',
      help='Evidencias da gmud nao pode estar vazio'
    )

    self.parser.add_argument(
      'referencia_externa',
      required=False,
      location='json',
      help='Referencia externa (em construcao)'
    )

    self.parser.add_argument(
      'emissor_id',
      required=True,
      location='json',
      help='Id do emissor nao pode estar vazio'
    )

    data = self.parser.parse_args()

    new_gmud = Gmud(
      numero=data['numero'],
      descricao=data['descricao'],
      responsavel=data['responsavel'],
      status=data['status'],
      versionamento=data['versionamento'],
      plano_execucao=data['plano_execucao'],
      plano_reversao=data['plano_reversao'],
      evidencias=data['evidencias'],
      referencia_externa=data['referencia_externa'],
      emissor_id=data['emissor_id']
    )

    try:
      new_gmud.save()
      return {'message': 'Gmud criada com sucesso'}
    except Exception as err:
      print(err)
      return {'message': 'Algo esta incorreto'}

  def put(self):
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
      type=bool,
      default=False,
      help='Status da gmud'
    )

    self.parser.add_argument(
      'versionamento',
      required=False,
      location='json',
      help='Versionamento da gmud'
    )

    self.parser.add_argument(
      'plano_execucao',
      required=True,
      location='json',
      help='Plano de execucao da gmud nao pode estar vazio'
    )

    self.parser.add_argument(
      'plano_reversao',
      required=True,
      location='json',
      help='Plano de reversao da gmud nao pode estar vazio'
    )

    self.parser.add_argument(
      'evidencias',
      required=True,
      location='json',
      help='Evidencias da gmud nao pode estar vazio'
    )

    self.parser.add_argument(
      'referencia_externa',
      required=False,
      location='json',
      help='Referencia externa (em construcao)'
    )

    self.parser.add_argument(
      'emissor_id',
      required=True,
      location='json',
      help='Id do emissor nao pode estar vazio'
    )

    data = self.parser.parse_args()

    if 'id' in request.args:
      gmud = Gmud.get_gmud_by_id(request.args['id'])

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
        gmud.emissor_id = data['emissor_id']

        try:
          gmud.save()
          return {'message': 'Gmud atualizada com sucesso'}
        except Exception as err:
          print(err)
          return {'message': 'Algo esta incorreto'}
      else:
        return {'message': 'Gmud nao encontrada'}
    else:
      return {'message': 'BAD REQUEST'}, 400

  def delete(self):
    if 'id' in request.args:
      try:
        Gmud.remove(request.args['id'])
      except Exception as err:
        print(err)
        return {'message': 'Algo esta incorreto'}
    else:
      return {'message': 'BAD REQUEST'}, 400