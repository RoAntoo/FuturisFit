from pymongo import MongoClient
from config_vars import MONGODB_CONNECTION
from db_models.cliente_dao import Cliente
from db_models.rutina_dao import Rutina
from db_models.maquina_dao import Maquina
from db_models.historial_cliente_dao import HistorialCliente

class Fit:
    def __init__(self):
        print("Conectando a MongoDB...")
        self.client = MongoClient(MONGODB_CONNECTION)

        self.db = self.client['FuturisFit']
        print("Conexión establecida a MongoDB.")

        # Inicializamos las colecciones
        Cliente.collection = self.db['clientes']
        Rutina.collection = self.db['rutinas']
        HistorialCliente.collection = self.db['historial_cliente']
        Maquina.collection = self.db['maquinas']

    # Operaciones sobre clientes
    @staticmethod
    def registrar_cliente(_id, nombre, apellido, fecha_nacimiento, email, telefono):
        
        """Registrar un nuevo cliente con validaciones."""
        
        if not all([_id, nombre, apellido, fecha_nacimiento, email, telefono]):
            print("Error: Todos los campos son obligatorios.")
            return

        if Cliente.consultar_cliente_por_id(_id):
            print(f"Error: Ya existe un cliente con ID {_id}.")
            return

        if Cliente.consultar_clientes_por_email(email):
            print(f"Error: Ya existe un cliente con el email {email}.")
            return

        Cliente.insertar_cliente(_id, nombre, apellido, fecha_nacimiento, email, telefono)
        print(f"Cliente {_id} registrado exitosamente.")

    @staticmethod
    def listar_clientes():
        """Listar todos los clientes."""
        clientes = Cliente.consultar_clientes()
        if clientes:
            for cliente in clientes:
                print(f"ID: {cliente['_id']}, Nombre: {cliente['nombre']}, Apellido: {cliente['apellido']}, Email: {cliente['email']}, Teléfono: {cliente['telefono']}")
        else:
            print("No se encontraron clientes registrados.")

    @staticmethod
    def buscar_cliente_por_nombre(nombre):
        """Buscar cliente por nombre."""
        cliente = Cliente.consultar_cliente_por_nombre(nombre)
        if cliente:
            print(f"Cliente encontrado: ID: {cliente['_id']}, Nombre: {cliente['nombre']}, Apellido: {cliente['apellido']}, Email: {cliente['email']}")
        else:
            print("Cliente no encontrado.")

    @staticmethod
    def eliminar_cliente_mailnombre(_id=None, email=None):
        """Eliminar un cliente de la colección por su ID o email."""
        if _id:
            resultado = Cliente.eliminar_cliente({"_id": _id})
        elif email:
            resultado = Cliente.eliminar_cliente({"email": email})
        else:
            print("Error: Debes proporcionar un ID o un email para eliminar un cliente.")
            return

        if resultado > 0:
            print("Cliente eliminado con éxito.")
        else:
            print("No se encontró ningún cliente con el ID o email proporcionado.")

    # Operaciones sobre rutinas
    @staticmethod
    def asignar_rutina_a_cliente(id_rutina, id_cliente, nombre_rutina, objetivo, tipo_intensidad, cantidad_series_rep, tiempo_descanso):
        """Asignar una rutina a un cliente con validaciones."""
        if not all([id_rutina, id_cliente, nombre_rutina, objetivo, tipo_intensidad, cantidad_series_rep, tiempo_descanso]):
            print("Error: Todos los campos son obligatorios.")
            return

        if not Cliente.consultar_cliente_por_id(id_cliente):
            print(f"Error: No existe el cliente con ID {id_cliente}.")
            return

        if Rutina.consultar_rutina_por_id(id_rutina):
            print(f"Error: Ya existe una rutina con ID {id_rutina}.")
            return

        Rutina.insertar_rutina(id_rutina, id_cliente, nombre_rutina, objetivo, tipo_intensidad, cantidad_series_rep, tiempo_descanso)
        print(f"Rutina {nombre_rutina} asignada al cliente {id_cliente}.")

    @staticmethod
    def listar_rutinas_por_cliente(id_cliente):
        """Listar todas las rutinas de un cliente."""
        if not Cliente.consultar_cliente_por_id(id_cliente):
            print(f"Error: No existe el cliente con ID {id_cliente}.")
            return

        rutinas = Rutina.consultar_rutinas_por_cliente(id_cliente)
        if rutinas:
            for rutina in rutinas:
                print(f"ID: {rutina['_id']}, Nombre de Rutina: {rutina['nombre_Rutina']}, Objetivo: {rutina['objetivo']}")
        else:
            print(f"El cliente con ID {id_cliente} no tiene rutinas asignadas.")

    # Operaciones sobre máquinas
    @staticmethod
    def registrar_maquina(_id, nombre, tipo, estado, ubicacion, fecha_mantenimiento):
        """Registrar una nueva máquina con validaciones."""
        if not all([_id, nombre, tipo, estado, ubicacion, fecha_mantenimiento]):
            print("Error: Todos los campos son obligatorios.")
            return

        if Maquina.consultar_maquina_por_id(_id):
            print(f"Error: Ya existe una máquina con ID {_id}.")
            return

        Maquina.insertar_maquina(_id, nombre, tipo, estado, ubicacion, fecha_mantenimiento)
        print(f"Máquina {_id} registrada exitosamente.")

    @staticmethod
    def actualizar_estado_maquina(_id, estado):
        """Actualizar el estado de una máquina (Disponible, Ocupada, Mantenimiento) con validación."""
        if not Maquina.consultar_maquina_por_id(_id):
            print(f"Error: No se encontró la máquina con ID {_id}.")
            return

        resultado = Maquina.actualizar_maquina(_id, estado=estado)
        if resultado:
            print(f"Estado de la máquina {_id} actualizado a {estado}.")
        else:
            print("Error al actualizar el estado de la máquina.")

    # Operaciones sobre historial de actividades
    @staticmethod
    def registrar_historial_cliente(_id, id_cliente, fecha_actividad, actividad, duracion):
        """Registrar un historial de actividades de un cliente con validaciones."""
        if not all([_id, id_cliente, fecha_actividad, actividad, duracion]):
            print("Error: Todos los campos son obligatorios.")
            return

        if not Cliente.consultar_cliente_por_id(id_cliente):
            print(f"Error: No existe el cliente con ID {id_cliente}.")
            return

        HistorialCliente.insertar_historial(_id, id_cliente, fecha_actividad, actividad, duracion)
        print(f"Historial registrado para el cliente {id_cliente} en la fecha {fecha_actividad}.")

    @staticmethod
    def listar_historial_por_cliente(id_cliente):
        """Listar todo el historial de actividades de un cliente."""
        if not Cliente.consultar_cliente_por_id(id_cliente):
            print(f"Error: No existe el cliente con ID {id_cliente}.")
            return

        historiales = HistorialCliente.consultar_historial_por_cliente(id_cliente)
        if historiales:
            for historial in historiales:
                print(f"ID: {historial['_id']}, Fecha: {historial['fecha_Actividad']}, Actividad: {historial['actividad']}, Duración: {historial['duracion']} min")
        else:
            print(f"El cliente con ID {id_cliente} no tiene historial registrado.")

    # Métodos para asignar rutina y máquina a cliente
    @staticmethod
    def asignar_rutina_a_cliente(cliente_id, rutina_id):
        """Asignar una rutina a un cliente."""
        resultado = Cliente.asignar_rutina(cliente_id, rutina_id)
        if resultado > 0:
            print(f"Rutina {rutina_id} asignada al cliente {cliente_id} con éxito.")
        else:
            print(f"No se pudo asignar la rutina {rutina_id} al cliente {cliente_id}.")

    @staticmethod
    def asignar_maquina_a_cliente(cliente_id, maquina_id):
        """Asignar una máquina a un cliente."""
        resultado = Cliente.asignar_maquina(cliente_id, maquina_id)
        if resultado > 0:
            print(f"Máquina {maquina_id} asignada al cliente {cliente_id} con éxito.")
        else:
            print(f"No se pudo asignar la máquina {maquina_id} al cliente {cliente_id}.")

    @staticmethod      
    def listar_clientes_y_rutinas_maquinas(self):
        """
        Listar todos los clientes junto con sus rutinas y máquinas.
        """
        Cliente.consultar_clientes_y_rutinas_maquinas()
    # Consultas avanzadas
    @staticmethod
    def consultar_cliente_con_rutinas(id_cliente):
        """Obtener un cliente junto con sus rutinas."""
        resultado = Cliente.collection.aggregate([
            {
                "$match": {
                    "_id": id_cliente
                }
            },
            {
                "$lookup": {
                    "from": "rutinas",
                    "localField": "_id",
                    "foreignField": "ID_Cliente",
                    "as": "rutinas_cliente"
                }
            }
        ])

        for doc in resultado:
            print(f"Cliente: {doc['nombre']} {doc['apellido']}")
            print("Rutinas:")
            for rutina in doc['rutinas_cliente']:
                print(f"  - Rutina: {rutina['nombre_Rutina']}, Objetivo: {rutina['objetivo']}")
