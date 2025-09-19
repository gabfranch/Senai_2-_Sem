# SQL_ALCHEMY
# pip install flask_sqlalchemy
# Permite a conexao da API com o Banco de Dados
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('carros')

# Rastrear as modificações realizadas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Configuração de conexão com o banco
# %40 -> @
# 1- Usuario (root) 2- Senha (Senai%40134) 3- 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_carro'

mybd = SQLAlchemy(app)

# Classe para definir o modelo dos dados que correspondem a tabela do banco de dados
class Carros(mybd.Model):
    __tablename__ = "tb_carro"
    id_carro = mybd.Column(mybd.Integer, primary_key=True)
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    ano = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.String(100))
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.String(100))

    # Esse metodo vai ser usado para converter o objeto em json
    def to_json(self):
        return {
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "valor": float(self.valor),
            "cor": self.cor,
            "numero_vendas": self.numero_vendas
        }


# Metodo 1 - GET
@app.route('/carros', methods=['GET'])
def seleciona_carro():
    carros_selecionados = Carros.query.all()
    # Executa uma consulta no banco de dados (SELECT * FROM tb_carros)
    carros_json = [carro.to_json() for carro in carros_selecionados]
    
    return gera_resposta(200, carros_json,"phoop, phoop")

# Metodo 2 - GET (POR ID)
@app.route('/carros/<id_carro_pam>', methods=['GET'])
def seleciona_carro_por_id(id_carro_pam):
    carro_selecionado = Carros.query.filter_by(id_carro = id_carro_pam).first()
    # SELECT * FROM tb_carro WHERE id_carro = 5
    carro_json = carro_selecionado.to_json()

    return gera_resposta(200, carro_json, 'fon, fon =D')


# Metodo 3 - POST
@app.route('/carros', methods=['POST'])
def criar_carro():
    requisicao = request.get_json()
    try:
        carro = Carros(
            id_carro = requisicao['id_carro'],
            marca = requisicao['marca'],
            modelo = requisicao['modelo'],
            valor = requisicao['valor'],
            ano = requisicao['ano'],
            cor = requisicao['cor'],
            numero_vendas = requisicao['numero_vendas']
        )
        
        mybd.session.add(carro) # Adiciona ao banco
        mybd.session.commit() # Salva

        return gera_resposta(201, carro.to_json(), 'Show de bola!')

    except Exception as e:
        print('Erro', e)

        return gera_resposta(400, {}, 'Ora, bolas!')

# Metodo 4 - DELETE
@app.route('/carros/<id_carro_pam>', methods=['DELETE'])
def deleta_carro(id_carro_pam):
    carro_selecionado = Carros.query.filter_by(id_carro = id_carro_pam).first()
    
    try:
        mybd.session.delete(carro_selecionado)
        mybd.session.commit()

        return gera_resposta(200, carro_selecionado.to_json(), 'Você deleteu um carro ;-;')

    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, 'Você falhou ._.')

# Metodo 5 - PUT
@app.route('/carros/<id_carro_pam>', methods=['PUT'])
def atualiza_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()
    requisicao = request.get_json()
    
    try:
        if('marca' in requisicao):
            carro.marca = requisicao['marca']

        if('modelo' in requisicao):
            carro.modelo = requisicao['modelo']
        
        if('ano' in requisicao):
            carro.ano = requisicao['ano']

        if('valor' in requisicao):
            carro.valor = requisicao['valor']

        if('cor' in requisicao):
            carro.cor = requisicao['cor']

        if('numero_vendas' in requisicao):
            carro.numero_vendas = requisicao['numero_vendas']

        mybd.session.add(carro)
        mybd.session.commit()

        return gera_resposta(200, carro.to_json(), "Carro atualizado! O.O")
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, 'Erro ao atualizar! T-T')

            


# Resposta Padrão
    # - status (200, 201)
    # nome do conteudo
    # conteudo
    # mensagem (opcional)
def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body['Lista de Carros'] = conteudo
    if (mensagem):
        body['palavra gamer'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')
    # Dumps - Converte o dicionario criado (body) em Json (json.dumps)

app.run(port=5000, host='localhost', debug=True)