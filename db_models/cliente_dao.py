from pymongo import MongoClient
from config_vars import MONGODB_CONNECTION

class Cliente:
    # Conexión a MongoDB y a la colección 'clientes'
    client = MongoClient(MONGODB_CONNECTION)
    db = client['FuturisFit']
    collection = db['clientes']

    # Métodos de inserción y eliminación
    @classmethod
    def insertar_cliente(cls, _id, nombre, apellido, fecha_nacimiento, email, telefono, rutinas=None, maquinas=None):
        """
        Agregar un nuevo cliente a la colección.
        """
        cliente_data = {
            "_id": _id,
            "nombre": nombre,
            "apellido": apellido,
            "fecha_nacimiento": fecha_nacimiento,
            "email": email,
            "telefono": telefono,
            "rutinas": rutinas if rutinas is not None else [],
            "maquinas": maquinas if maquinas is not None else []
        }
        return cls.collection.insert_one(cliente_data)

    @classmethod
    def eliminar_cliente(cls, condicion):
        """
        Eliminar un cliente de la colección usando una condición (ID o email).
        """
        resultado = cls.collection.delete_one(condicion)
        return resultado.deleted_count

    # Métodos de consulta
    @classmethod
    def consultar_cliente_por_id(cls, _id):
        """
        Obtener un cliente por su ID.
        """
        return cls.collection.find_one({"_id": _id})

    @classmethod
    def consultar_cliente_por_nombre(cls, nombre):
        """
        Obtener un cliente por su nombre.
        """
        return cls.collection.find_one({"nombre": nombre})

    @classmethod
    def consultar_clientes(cls):
        """
        Obtener todos los clientes de la colección.
        """
        return list(cls.collection.find({}))

    @classmethod
    def consultar_clientes_por_email(cls, email):
        """
        Obtener clientes por email.
        """
        return cls.collection.find_one({"email": email})

    @classmethod
    def consultar_clientes_por_apellido(cls, apellido):
        """
        Obtener una lista de clientes por apellido.
        """
        clientes = cls.collection.find({"apellido": apellido})
        for cliente in clientes:
            print(f"ID: {cliente['_id']}, Nombre: {cliente['nombre']}, Apellido: {cliente['apellido']}, Email: {cliente['email']}, Teléfono: {cliente['telefono']}")

    # Método de actualización
    @classmethod
    def actualizar_cliente(cls, _id, nombre=None, apellido=None, fecha_nacimiento=None, email=None, telefono=None):
        """
        Actualizar los datos de un cliente.
        """
        update_data = {}
        if nombre:
            update_data["nombre"] = nombre
        if apellido:
            update_data["apellido"] = apellido
        if fecha_nacimiento:
            update_data["fecha_nacimiento"] = fecha_nacimiento
        if email:
            update_data["email"] = email
        if telefono:
            update_data["telefono"] = telefono

        resultado = cls.collection.update_one({"_id": _id}, {"$set": update_data})
        return resultado.modified_count

    # Métodos para incluir las rutinas y máquinas
    @classmethod
    def asignar_rutina(cls, cliente_id, rutina_id):
        """
        Asignar una rutina a un cliente.
        """
        resultado = cls.collection.update_one(
            {"_id": cliente_id},
            {"$addToSet": {"rutinas": rutina_id}}  # Añadir rutina si no existe
        )
        return resultado.modified_count

    @classmethod
    def asignar_maquina(cls, cliente_id, maquina_id):
        """
        Asignar una máquina a un cliente.
        """
        resultado = cls.collection.update_one(
            {"_id": cliente_id},
            {"$addToSet": {"maquinas": maquina_id}}  # Añadir máquina si no existe
        )
        return resultado.modified_count

    @classmethod
    def consultar_clientes_y_rutinas_maquinas(cls):
        """
        Consultar todos los clientes junto con sus rutinas y máquinas.
        """
        clientes = cls.collection.find({})
        for cliente in clientes:
            print(f"Cliente: {cliente['nombre']} {cliente['apellido']} (ID: {cliente['_id']})")
            print("  Rutinas:", cliente.get("rutinas", []))
            print("  Máquinas:", cliente.get("maquinas", []))
            print()  # Nueva línea para separar clientes
