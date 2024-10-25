from pymongo import MongoClient
from config_vars import MONGODB_CONNECTION

class Rutina:
    client = MongoClient(MONGODB_CONNECTION)
    db = client['FuturisFit']
    collection = db['rutinas']

    @classmethod
    def insertar_rutina(cls, _id, id_cliente, nombre_rutina, objetivo, tipo_intensidad, cantidad_series_rep, tiempo_descanso):
        """
        Agregar una nueva rutina a la colección.
        """
        if not all([_id, id_cliente, nombre_rutina, objetivo, tipo_intensidad, cantidad_series_rep, tiempo_descanso]):
            print("Error: Todos los campos son obligatorios.")
            return None
        
        rutina_data = {
            "_id": _id,
            "id_cliente": id_cliente,
            "nombre_rutina": nombre_rutina,
            "objetivo": objetivo,
            "tipo_intensidad": tipo_intensidad,
            "cantidad_series_rep": cantidad_series_rep,
            "tiempo_descanso": tiempo_descanso
        }
        try:
            return cls.collection.insert_one(rutina_data)
        except Exception as e:
            print(f"Error al insertar rutina: {e}")
            return None


    

    @classmethod
    def consultar_rutina_por_id(cls, _id):
        """
        Obtener una rutina por su ID.
        """
        return cls.collection.find_one({"_id": _id})

    @classmethod
    def consultar_rutinas_por_cliente(cls, id_cliente):
        """
        Obtener todas las rutinas de un cliente por su ID.
        """
        return list(cls.collection.find({"id_cliente": id_cliente}))

    @classmethod
    def consultar_rutinas(cls):
        """
        Obtener todas las rutinas de la colección.
        """
        return list(cls.collection.find({}))

    @classmethod
    def actualizar_rutina(cls, _id, nombre_rutina=None, objetivo=None, tipo_intensidad=None, cantidad_series_rep=None, tiempo_descanso=None):
        """
        Actualizar los datos de una rutina.
        """
        update_data = {}
        if nombre_rutina:
            update_data["nombre_rutina"] = nombre_rutina
        if objetivo:
            update_data["objetivo"] = objetivo
        if tipo_intensidad:
            update_data["tipo_intensidad"] = tipo_intensidad
        if cantidad_series_rep:
            update_data["cantidad_series_rep"] = cantidad_series_rep
        if tiempo_descanso:
            update_data["tiempo_descanso"] = tiempo_descanso

        try:
            resultado = cls.collection.update_one({"_id": _id}, {"$set": update_data})
            return resultado.modified_count
        except Exception as e:
            print(f"Error al actualizar rutina: {e}")
            return None

    @classmethod
    def insertar_varias_rutinas(cls, rutinas):
        """
        Agregar varias rutinas a la colección.
        :param rutinas: lista de diccionarios, cada uno representando una rutina.
        :return: número de rutinas insertadas.
        """
        if not rutinas or not all(['id_cliente' in r and 'nombre_rutina' in r for r in rutinas]):
            print("Error: Todos los campos son obligatorios.")
            return 0
    
        insertados = 0
        for rutina_data in rutinas:
            try:
                result = cls.collection.insert_one(rutina_data)
                insertados += 1
            except Exception as e:
                print(f"Error al insertar rutina: {e}")
        
        return insertados

    
    
    @classmethod
    def eliminar_rutina(cls, _id):
        """
        Eliminar una rutina de la colección por su ID.
        """
        try:
            resultado = cls.collection.delete_one({"_id": _id})
            return resultado.deleted_count
        except Exception as e:
            print(f"Error al eliminar rutina: {e}")
            return None
