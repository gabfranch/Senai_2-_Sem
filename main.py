from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('clientes')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_clinicavetbd'

mybd = SQLAlchemy(app)

class Clientes(mybd.Model):
    __tablename__ = 'tb_clientes'
    id_cliente = mybd.Column(mybd.Integer, primary_key=True)
    nome = mybd.Column(mybd.String(255))
    endereco = mybd.Column(mybd.String(255))
    telefone = mybd.Column(mybd.String(15))

    def to_json(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "endereco": self.endereco,
            "telefone": self.telefone
        }


# Metodo 1 - Create
@app.route('/clinica/clientes', methods=['POST'])
def create_cliente():
    requisition = request.get_json()
    
    try:
        cliente = Clientes(
            id_cliente = requisition['id_cliente'],
            nome = requisition['nome'],
            endereco = requisition['endereco'],
            telefone = requisition['telefone']
        )

        mybd.session.add(cliente)
        mybd.session.commit()

        return response(201, 'cliente', cliente.to_json(), 'Cliente criado! :]')
    
    except Exception as e:
        print('Deu erro! ;-; ', e)

        return response(400, 'cliente', {}, 'Ora, bolas! :C')


# Metodo 2 - Read
@app.route('/clinica/clientes', methods=['GET'])
def read_cliente():
    try:
        selected_clientes = Clientes.query.all()
        clientes_json = [cliente.to_json() for cliente in selected_clientes]

        return response(200, 'cliente', clientes_json, 'Clientes lidos! :D')

    except Exception as e:
        print('Deu erro! ;-; ', e)

        return response(400, 'cliente', {}, 'Ora, bolas! :C')


# Metodo 2.1 - Read (by ID)
@app.route('/clinica/clientes/<id_cliente_pam>', methods=['GET'])
def read_cliente_by_id(id_cliente_pam):

    try:
        selected_client = Clientes.query.filter_by(id_cliente = id_cliente_pam).first()
        cliente_json = selected_client.to_json()
        
        return response(200, 'cliente', cliente_json, 'Cliente lido! :)')
    
    except Exception as e:
        print('Deu erro! ;-; ', e)

        return response(400, 'cliente', {}, 'Ora, bolas! :C')


# Metodo 3 - Update
@app.route('/clinica/clientes/<id_cliente_pam>', methods=['PUT'])
def update_cliente(id_cliente_pam):
    cliente = Clientes.query.filter_by(id_cliente = id_cliente_pam).first()
    requisition = request.get_json()

    try:
        columns = ['nome', 'endereco', 'telefone']

        for column in columns:
            match column:
                case 'nome':
                    cliente.nome = requisition['nome']
                case 'endereco':
                    cliente.endereco = requisition['endereco']
                case 'telefone':
                    cliente.telefone = requisition['telefone']
                case _:
                    continue

        mybd.session.add(cliente)
        mybd.session.commit()

        return response(200, 'cliente', cliente.to_json(), 'Cliente atualizado! UvU')

    except Exception as e:
        print('Deu erro! ;-; ', e)

        return response(400, 'cliente', {}, 'Ora, bolas! :C')


# Metodo 4 - Delete
@app.route('/clinica/clientes/<id_cliente_pam>', methods=['DELETE'])
def delete_cliente(id_cliente_pam):
    selected_cliente = Clientes.query.filter_by(id_cliente = id_cliente_pam).first()

    try:
        mybd.session.delete(selected_cliente)
        mybd.session.commit()

        return response(200, 'cliente', selected_cliente.to_json(), 'Cliente deletado! Q-Q')

    except Exception as e:
        print('Deu erro! ;-; ', e)

        return response(400, 'cliente', {}, 'Ora, bolas! :C')
    

class Pets(mybd.Model):
    __tablename__ = 'tb_pets'
    id_pet = mybd.Column(mybd.Integer, primary_key=True, autoincrement=True)
    nome = mybd.Column(mybd.String(100)) 
    tipo = mybd.Column(mybd.String(100))
    raca = mybd.Column(mybd.String(100))
    data_nascimento = mybd.Column(mybd.String(100)) 
    id_clienteF = mybd.Column(mybd.Integer, mybd.ForeignKey("tb_clientes.id_cliente"), nullable=False)
    idade = mybd.Column(mybd.String(100))

    def to_json(self):
        return {
            "id_pet": self.id_pet,
            "nome": self.nome,
            "tipo": self.tipo,
            "raca": self.raca,
            "data_nascimento": str(self.data_nascimento),
            "id_clienteF": self.id_clienteF,
            "idade": self.idade
        }
    

# Metodo 1 - Create

@app.route('/clinica/pets', methods=['POST'])
def create_pet():
    requisition = request.get_json()

    try:
        pet = Pets(
            id_pet = requisition['id_pet'],
            nome = requisition['nome'],
            tipo = requisition['tipo'],
            raca = requisition['raca'],
            data_nascimento = requisition['data_nascimento'],
            id_clienteF = requisition['id_clienteF'],
            idade = requisition['idade']
        )

        mybd.session.add(pet)
        mybd.session.commit()

        return response(201, 'pet', pet.to_json(), 'Pet criado! :]')

    except Exception as e:
        print('Deu erro! ;-;', e)

        return response(400, 'pet', {}, 'Ora, bolas! :C')
    
# Metodo 2 - Read

@app.route('/clinica/pets', methods=['GET'])
def read_pet():
    try:
        selected_pets = Pets.query.all()
        pets_json = [pet.to_json() for pet in selected_pets]

        return response(200, 'pet', pets_json, 'Pets lidos! :D')

    except Exception as e:
        print('Deu erro! ;-;', e)

        return response(400, 'pet', {}, 'Ora, bolas! :C')
    

# Metodo 2.1 - Read (by ID)

@app.route('/clinica/pets/<id_pet_pam>', methods=['GET'])
def read_pet_by_id(id_pet_pam):
    try:
        selected_pet = Pets.query.filter_by(id_pet = id_pet_pam).first()
        pet_json = selected_pet.to_json()

        return response(200, 'pet', pet_json, 'Pet lido! :)')
    
    except Exception as e:
        print('Deu erro! ;-; ', e)

        return response(400, 'pet', {}, 'Ora, bolas! :C')
    

# Metodo 3 - Update

@app.route('/clinica/pets/<id_pet_pam>', methods=['PUT'])
def update_pet(id_pet_pam):
    pet = Pets.query.filter_by(id_pet = id_pet_pam).first()
    requisition = request.get_json()

    try:
        columns = ['nome', 'tipo', 'raca', 'data_nascimento', 'id_clienteF', 'idade']

        for column in columns:
            match column:
                case 'nome':
                    pet.nome = requisition['nome']
                case 'tipo':
                    pet.tipo = requisition['tipo']
                case 'raca':
                    pet.raca = requisition['raca']
                case 'data_nascimento':
                    pet.data_nascimento = requisition['data_nascimento']
                case 'id_clienteF':
                    pet.id_clienteF = requisition['id_clienteF']
                case 'idade':
                    pet.idade = requisition['idade']

        mybd.session.add(pet)
        mybd.session.commit()

        return response(200, 'pet', pet.to_json(), 'Pet atualizado! UvU')
    
    except Exception as e:
        print('Deu erro! ;-; ', e)

        return response(400, 'pet', {}, 'Ora, bolas! :C')


# Metodo 4 - Delete

@app.route('/clinica/pets/<id_pet_pam>', methods=['DELETE'])
def delete_pet(id_pet_pam):
    selected_pet = Pets.query.filter_by(id_pet = id_pet_pam).first()

    try:
        mybd.session.delete(selected_pet)
        mybd.session.commit()

        return response(200, 'pet', selected_pet.to_json(), 'Pet deletado! Q-Q')
    
    except Exception as e:
        print('Deu erro! ;-;', e)

        return response(400, 'pet', {}, 'Ora, bolas! :C')


# Resposta
def response(status, content, payload, message=False):
    body = {}
    body[content] = payload
    
    if message:
        body['mensagem'] = message

    return Response(json.dumps(body), status=status, mimetype='application/json')


app.run(port=5000, host='localhost', debug=True)

