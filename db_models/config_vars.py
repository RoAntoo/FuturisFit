from pymongo import MongoClient
from pymongo.errors import ConfigurationError

MONGO_URI = "mongodb+srv://super_duper:hola@cluster0.0dncs2d.mongodb.net/mi_proyecto?retryWrites=true&w=majority"
DATABASE_NAME = "FuturisFit"
MONGODB_CONNECTION = MONGO_URI

def get_database():
    """
    Funcion para obtener una conexión a la base de datos MongoDB.
    """
    try:
        client = MongoClient(MONGO_URI)

        db = client[DATABASE_NAME]
        
        print(f"Conexion a la base de datos {DATABASE_NAME}: EXITOSA")
        
        return db
    except ConnectionError as e:
		
        print(f"Error de conexión a MongoDB: {e}")
        
        return None

def close_connection(client):
    """
    Funcion para cerrar la conexión a MongoDB.
    """
    client.close()
    print("Conexión a MongoDB cerrada.")
