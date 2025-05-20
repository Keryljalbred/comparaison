from neo4j import GraphDatabase
import time
import psutil

# Connexion à Neo4j
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))  # Remplacez par votre mot de passe

def measure_resources():
    process = psutil.Process()
    cpu_usage = process.cpu_percent()
    ram_usage = process.memory_info().rss / (1024 * 1024)  # Convertir en MB
    return cpu_usage, ram_usage

# Create
start_time = time.time()
with driver.session() as session:
    session.run("CREATE (r:Review {id: '1', text: 'First review', rating: 5.0})")
end_time = time.time()
cpu_create, ram_create = measure_resources()
print(f"Create: Temps = {end_time - start_time:.4f} s, CPU = {cpu_create:.4f}%, RAM = {ram_create:.2f} MB")

# Read
# Read
start_time = time.time()
with driver.session() as session:
    result = session.run("MATCH (r:Review {id: '1'}) RETURN r")
    for record in result:
        # Afficher uniquement les propriétés du nœud
        print(record['r'].items())  # Affiche les propriétés sous forme de dictionnaire
end_time = time.time()
cpu_read, ram_read = measure_resources()
print(f"Read: Temps = {end_time - start_time:.4f} s, CPU = {cpu_read:.4f}%, RAM = {ram_read:.2f} MB")
# Update
start_time = time.time()
with driver.session() as session:
    session.run("MATCH (r:Review {id: '1'}) SET r.rating = 4.5")
end_time = time.time()
cpu_update, ram_update = measure_resources()
print(f"Update: Temps = {end_time - start_time:.4f} s, CPU = {cpu_update:.4f}%, RAM = {ram_update:.2f} MB")

# Delete
start_time = time.time()
with driver.session() as session:
    session.run("MATCH (r:Review {id: '1'}) DELETE r")
end_time = time.time()
cpu_delete, ram_delete = measure_resources()
print(f"Delete: Temps = {end_time - start_time:.4f} s, CPU = {cpu_delete:.4f}%, RAM = {ram_delete:.2f} MB")

driver.close()