from neo4j import GraphDatabase
import time
import psutil

# Fonction pour mesurer les ressources
def measure_resources():
    process = psutil.Process()
    cpu_usage = process.cpu_percent()
    ram_usage = process.memory_info().rss / (1024 * 1024)  # Convertir en MB
    return cpu_usage, ram_usage

# Connexion à Neo4j
uri = "bolt://localhost:7687"  
username = "neo4j"              
password = "password"            

driver = GraphDatabase.driver(uri, auth=(username, password))

# Démarrer la mesure du temps
start_time = time.time()

# Exporter les documents (nœuds dans cet exemple)
with driver.session() as session:
    result = session.run("MATCH (n) RETURN n")
    exported_nodes = [record["n"] for record in result]

# Fin de la mesure du temps
end_time = time.time()

# Mesurer les ressources
cpu_usage, ram_usage = measure_resources()

# Afficher les résultats
print(f"Nœuds exportés : {len(exported_nodes)}")
print(f"Temps d'exportation : {end_time - start_time:.4f} secondes")
print(f"Utilisation CPU : {cpu_usage:.4f}%")
print(f"Utilisation RAM : {ram_usage:.2f} MB")

# Fermer le driver
driver.close()