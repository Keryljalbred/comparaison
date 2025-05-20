from arango import ArangoClient
import time
import psutil

# Connexion à ArangoDB
client = ArangoClient()

# Nom de la base de données
db_name = 'mydatabase'

# Vérifier si la base de données existe déjà
if db_name not in client.db('_system', username='root', password='password').databases():
    client.db('_system', username='root', password='password').create_database(db_name)

# Connexion à la base de données
db = client.db(db_name, username='root', password='password')

# Nouveau nom de la collection
collection_name = 'reviews'  
if collection_name not in [collection['name'] for collection in db.collections()]:
    db.create_collection(collection_name)
    print(f"La collection '{collection_name}' a été créée.")
else:
    print(f"La collection '{collection_name}' existe déjà.")

def measure_resources():
    process = psutil.Process()
    cpu_usage = process.cpu_percent()
    ram_usage = process.memory_info().rss / (1024 * 1024)  # Convertir en MB
    return cpu_usage, ram_usage

# Create or Update
start_time = time.time()
document_id = '1'

# Vérifiez si le document existe
existing_document = db.collection(collection_name).get(document_id)

if existing_document:
    print("Le document existe déjà, mise à jour en cours.")
else:
    # Insérer un nouveau document
    existing_document = db.collection(collection_name).insert({
        '_key': document_id,
        'text': 'First review',
        'rating': float(5.0)  
    })
    print("Document inséré.")

end_time = time.time()
cpu_create_update, ram_create_update = measure_resources()
print(f"Create/Update: Temps = {end_time - start_time:.4f} s, CPU = {cpu_create_update:.4f}%, RAM = {ram_create_update:.2f} MB")

# Read
start_time = time.time()
document = db.collection(collection_name).get(document_id)
print(f"Read: Document = {document}")
end_time = time.time()
cpu_read, ram_read = measure_resources()
print(f"Read: Temps = {end_time - start_time:.4f} s, CPU = {cpu_read:.4f}%, RAM = {ram_read:.2f} MB")

# Update again
start_time = time.time()
if document and isinstance(document, dict) and '_key' in document:
    try:
        document_key = document['_key']  # utiliser _key
        print(f"Clé du document : {document_key}")
        update_data = {'rating': float(4.5)}
        print(f"Données de mise à jour : {update_data}")

        if isinstance(update_data, dict):
            print(f"Appel à update avec clé: {document_key} et données: {update_data}")
            db.collection(collection_name).update({'_key': document_key, **update_data})
            print("Document mis à jour.")
        else:
            print("Les données de mise à jour ne sont pas dans le bon format.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")
else:
    print("Le document n'existe pas, mise à jour impossible.")
end_time = time.time()
cpu_update, ram_update = measure_resources()
print(f"Update: Temps = {end_time - start_time:.4f} s, CPU = {cpu_update:.4f}%, RAM = {ram_update:.2f} MB")

# Delete
start_time = time.time()
db.collection(collection_name).delete(document_id)
end_time = time.time()
cpu_delete, ram_delete = measure_resources()
print(f"Delete: Temps = {end_time - start_time:.4f} s, CPU = {cpu_delete:.4f}%, RAM = {ram_delete:.2f} MB")