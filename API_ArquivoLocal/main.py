# pip install flask

from flask import Flask, request, make_response, jsonify
from bd import carros

# módulo do Flask vai subir a nossa API localmente
# Vamos instanciar o modulo Flask na nossa variavel app
app = Flask('carros')

# METODO 1 - VISUALIZAÇÃO DE DADOS (GET)
@app.route('/carrinho', methods=['GET'])
def get_carros():
    return carros

# METODO 1 PARTE 2 - VISUALIZAÇÃO DE DADOS POR ID (GET)
@app.route('/carrinho/<int:id>', methods=['GET'])
def get_carro_por_id(id):
    for carro in carros:
        if carro.get('id') == id:
            return jsonify(carro)


# METODO 2 - CRIAR NOVOS REGISTROS (POST)
# verificar os dados que estão passados na requisição e armazenar na nossa base
@app.route('/carrinho', methods=['POST'])
def criar_carro():
    carro = request.json
    carros.append(carro)
    return make_response(
        jsonify(
            mensagem = 'Carro cadastrado com sucesso!',
            carrinho = carro
        )
    )

# METODO 3 - DELETAR REGISTROS (DELETE)
@app.route('/carrinho/<int:id>', methods=['DELETE'])
def excluir_carro(id):
     for carro in carros:
        if carro.get('id') == id:
            del carro
            return jsonify (
                { 'mensagem': 'Carro excluído!' }
            )
        
# METODO 4 - EDITAR OS REGISTROS (PUT)
@app.route('/carrinho/<int:id>', methods=['PUT'])
def editar_carro(id):
    carro_alterado = request.get_json()
    for indice, carro in enumerate(carros):
        if carro.get('id') == id:
            carros[indice].update(carro_alterado)
            return jsonify(carros[indice])
            

app.run(port=5000, host='localhost', debug=True)