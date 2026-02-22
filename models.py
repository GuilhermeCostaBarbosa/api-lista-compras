from db import db

class Lista_Compras(db.Model):
    __tablename__ = 'lista_compras'

    id = db.Column(db.Integer, primary_key=True)

    produto = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    comprado = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            "id": self.id,
            "produto": self.produto,
            "quantidade": self.quantidade,
            "comprado": self.comprado
        }