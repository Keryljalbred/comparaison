from arango import ArangoClient
import time
import psutil

# Fonction pour mesurer les ressources
def measure_resources():
    process = psutil.Process()
    cpu_usage = process.cpu_percent()
    ram_usage = process.memory_info().rss / (1024 * 1024)  # Convertir en MB
    return cpu_usage, ram_usage

# Connexion à ArangoDB
client = ArangoClient()

# Nom de la base de données et de la collection
db_name = 'mydatabase'
collection_name = 'reviews'  # Utilisation de la collection reviews

# Connexion à la base de données
db = client.db(db_name, username='root', password='password')

# Vérifiez le nombre de documents dans la collection
document_count = db.collection(collection_name).count()
print(f"Nombre de documents dans la collection '{collection_name}': {document_count}")

# Démarrer la mesure du temps
start_time = time.time()

# Obtenir tous les documents de la collection
documents = db.collection(collection_name).all()

# Exporter les documents (par exemple, les imprimer ou les sauvegarder dans un fichier)
exported_documents = []
for doc in documents:
    exported_documents.append(doc)

# Fin de la mesure du temps
end_time = time.time()

# Mesurer les ressources
cpu_usage, ram_usage = measure_resources()

# Afficher les résultats
print(f"Documents exportés")
print(f"Temps d'exportation : {end_time - start_time:.4f} secondes")
print(f"Utilisation CPU : {cpu_usage:.4f}%")
print(f"Utilisation RAM : {ram_usage:.2f} MB")