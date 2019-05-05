from main import ma

class EmissorSchema(ma.Schema):
  class Meta:
    fields = ('id', 'nome', 'servidor', 'nome_base', 'usuario_db', 'senha_db')


class GmudSchema(ma.Schema):
  class Meta:
    fields: (
      'id', 'numero', 'descricao', 'responsavel', 'status',
      'versionamento', 'plano_execucao', 'plano_reversao',
      'evidencias', 'referencia_externa', 'emissor_id')


emissor_schema = EmissorSchema()
gmud_schema = GmudSchema()