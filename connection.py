from pymongo import MongoClient

# Reemplaza con tus credenciales y datos de conexión
uri = "mongodb+srv://super_duper:hola@cluster0.0dncs2d.mongodb.net/mi_proyecto?retryWrites=true&w=majority"  # o tu URI de conexión
client = MongoClient(uri)

try:
    # Prueba de conexión
    client.admin.command('ping')
    print("Conexión exitosa a MongoDB!")

    # Accede a una base de datos y colección
    db = client["nombre_de_tu_base_de_datos"]
    collection = db["nombre_de_tu_coleccion"]

    # Contar documentos
    count = collection.count_documents({})
    print(f"Documentos en la colección: {count}")

except Exception as e:
    print(f"Error en la conexión: {e}")
finally:
    client.close()
