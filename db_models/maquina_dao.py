import sys
import os
from pymongo import MongoClient
from config_vars import MONGODB_CONNECTION
from datetime import datetime, timedelta

class Maquina:
    
    client = MongoClient(MONGODB_CONNECTION)
    db = client['FuturisFit']
    collection = db['maquinas']

    @classmethod
    def insertar_maquina(cls, _id, nombre, tipo, estado, ubicacion, fecha_mantenimiento):
        """
        Agregar una nueva máquina a la colección.
        """
        if not all([_id, nombre, tipo, estado, ubicacion, fecha_mantenimiento]):
            print("Error: Todos los campos son obligatorios.")
            return None
        
        maquina_data = {
            "_id": _id,
            "nombre": nombre,
            "tipo": tipo,
            "estado": estado,
            "ubicacion": ubicacion,
            "fecha_mantenimiento": fecha_mantenimiento
        }
        try:
            return cls.collection.insert_one(maquina_data)
        except Exception as e:
            print(f"Error al insertar máquina: {e}")
            return None

    @classmethod
    def consultar_maquina_por_nombre(cls, nombre):
        """
        Obtener una máquina por su nombre.
        """
        return cls.collection.find_one({"nombre": nombre})

    @classmethod
    def consultar_maquina_por_id(cls, _id):
        """
        Obtener una máquina por su ID.
        """
        return cls.collection.find_one({"_id": _id})

    @classmethod
    def consultar_maquinas_por_tipo(cls, tipo):
        """
        Obtener una lista de máquinas por tipo (Cardio, Fuerza, etc.)
        """
        maquinas = cls.collection.find({"tipo": tipo})
        return list(maquinas)

    @classmethod
    def consultar_maquinas(cls):
        """
        Obtener todas las máquinas de la colección.
        """
        return list(cls.collection.find({}))

    @classmethod
    def consultar_maquinas_por_estado(cls, estado):
        """
        Obtener una lista de máquinas por estado (Disponible, Ocupada, Mantenimiento).
        """
        maquinas = cls.collection.find({"estado": estado})
        return list(maquinas)

    @classmethod
    def consultar_maquinas_por_ubicacion(cls, ubicacion):
        """
        Obtener una lista de máquinas por ubicación en el gimnasio.
        """
        maquinas = cls.collection.find({"ubicacion": ubicacion})
        return list(maquinas)

    @classmethod
    def consultar_maquinas_que_requieren_mantenimiento(cls):
        """
        Obtener máquinas que requieren mantenimiento (más de 6 meses sin mantenimiento).
        """
        seis_meses_atras = datetime.now() - timedelta(days=6*30)
        maquinas = cls.collection.find({"fecha_mantenimiento": {"$lt": seis_meses_atras}})
        return list(maquinas)

    @classmethod
    def actualizar_maquina(cls, _id, nombre=None, tipo=None, estado=None, ubicacion=None, fecha_mantenimiento=None):
        """
        Actualizar los datos de una máquina.
        """
        update_data = {}
        if nombre:
            update_data["nombre"] = nombre
        if tipo:
            update_data["tipo"] = tipo
        if estado:
            update_data["estado"] = estado
        if ubicacion:
            update_data["ubicacion"] = ubicacion
        if fecha_mantenimiento:
            update_data["fecha_mantenimiento"] = fecha_mantenimiento

        try:
            resultado = cls.collection.update_one({"_id": _id}, {"$set": update_data})
            return resultado.modified_count
        except Exception as e:
            print(f"Error al actualizar máquina: {e}")
            return None

    @classmethod
    def eliminar_maquina(cls, _id):
        """
        Eliminar una máquina de la colección por su ID.
        """
        try:
            resultado = cls.collection.delete_one({"_id": _id})
            return resultado.deleted_count
        except Exception as e:
            print(f"Error al eliminar máquina: {e}")
            return None
