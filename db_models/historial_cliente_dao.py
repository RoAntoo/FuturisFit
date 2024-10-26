from pymongo import MongoClient
from config_vars import MONGODB_CONNECTION

class HistorialCliente:
    client = MongoClient(MONGODB_CONNECTION)
    db = client['Gimnasio']
    collection = db['historial_cliente'] 

    @classmethod
    def insertar_historial(cls, _id, id_cliente, fecha_actividad, actividad, duracion):
        """
        Agregar un nuevo historial de cliente a la colección.
        """
        
        historial_data = {
            "_id": _id,
            "ID_Cliente": id_cliente,
            "fecha_Actividad": fecha_actividad,
            "actividad": actividad,
            "duracion": duracion
        }
        
        return cls.collection.insert_one(historial_data)

    @classmethod
    def consultar_historial_por_id(cls, _id):
        """
        Obtener un historial por su ID.
        """
        return cls.collection.find_one({"_id": _id})

    @classmethod
    def consultar_historial_por_cliente(cls, id_cliente):
        """
        Obtener todos los historiales de un cliente por su ID.
        """
        return list(cls.collection.find({"ID_Cliente": id_cliente}))

    @classmethod
    def consultar_historial_por_fecha(cls, fecha_actividad):
        """
        Obtener los historiales por fecha de actividad.
        """
        return list(cls.collection.find({"fecha_Actividad": fecha_actividad}))

    @classmethod
    def consultar_historiales(cls):
        """
        Obtener todos los historiales de la colección.
        """
        return list(cls.collection.find({}))

    @classmethod
    def actualizar_historial(cls, _id, fecha_actividad=None, actividad=None, duracion=None):
        """
        Actualizar los datos de un historial.
        """
        update_data = {}
        if fecha_actividad:
            update_data["fecha_Actividad"] = fecha_actividad
        if actividad:
            update_data["actividad"] = actividad
        if duracion:
            update_data["duracion"] = duracion

        resultado = cls.collection.update_one({"_id": _id}, {"$set": update_data})
        return resultado.modified_count

    @classmethod
    def eliminar_historial(cls, _id):
        """
        Eliminar un historial de la colección por su ID.
        """
        resultado = cls.collection.delete_one({"_id": _id})
        return resultado.deleted_count
