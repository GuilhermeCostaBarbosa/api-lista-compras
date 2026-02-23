from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Lista_Compras
from db import db
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'lista.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Rota para listar os itens do DB via JSON
@app.route('/api/itens', methods=['GET'])
def get_itens():
    itens = db.session.query(Lista_Compras).all()
    print(itens)
    return jsonify([item.to_json() for item in itens])

# Rota para pegar item pelo ID
@app.route('/api/itens/<int:id>', methods=['GET'])
def get_item(id):
    item = db.session.query(Lista_Compras).filter_by(id=id).first()
    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404
    return jsonify(item.to_json()), 200


# Rota para cadastrar novos produtos a lista, recebe o json pelo front
@app.route('/api/itens', methods=['POST'])
def create_item():
        dados = request.json
        if not dados or 'produto' not in dados:
             return jsonify({'error': 'Nome é obrigatório'}), 400

        produto = dados.get('produto')
        quantidade = dados.get('quantidade', 1) 

        novo_produto = Lista_Compras(produto=produto, quantidade=quantidade)
        db.session.add(novo_produto)
        db.session.commit()
        return jsonify(novo_produto.to_json()), 201

# Rota para editar dados já existentes
@app.route('/api/itens/<int:id>', methods=['PUT'])
def update_item(id):
    item = db.session.query(Lista_Compras).filter_by(id=id).first()

    if not item:
        return jsonify({'Erro: Item não encontrado'}), 404
     
    dados = request.json

    if 'produto' in dados:
        item.produto = dados.get('produto')

    if 'quantidade' in dados:
        item.quantidade = dados.get('quantidade')

    db.session.commit()
    return jsonify(item.to_json()), 200
    
# Rota para deletar um item da lista, recebe resposta do front
@app.route('/api/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = db.session.query(Lista_Compras).filter_by(id=id).first()

    if not item:
        return jsonify({'error': 'item não encontrado'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deletado com sucesso'})


if __name__ == '__main__':
    app.run(debug=True)