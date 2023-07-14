from pymongo import MongoClient

class MongoConn:
    def __init__(self):
        try:
            self.cliente = MongoClient("mongodb://localhost:27017")
            self.base_de_datos = self.cliente["empresa"]
            self.coleccion = self.base_de_datos["trabajadores"]
        except Exception as e:
            print(e)

    def insertar_data(self, doc: dict):
        self.coleccion.insert_one(doc)

    def actualizar_data(self, filtro: dict, valores: dict):
        self.coleccion.update_one(filtro, valores)

    def encontrar_data(self, doc: dict):
        return self.coleccion.find_one(doc)
    
    def encontrar_multiple_data(self, doc: dict):
        return self.coleccion.find(doc)
    
    def encontrar_data_aggregate(self, doc: dict):
        return self.coleccion.aggregate(doc)