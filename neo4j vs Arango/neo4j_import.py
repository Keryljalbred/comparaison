from neo4j import GraphDatabase
import time
import psutil
import csv

# Connexion à Neo4j
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))  # Remplacez par votre mot de passe

# Mesurer le temps d'importation
start_time = time.time()
process = psutil.Process()
cpu_before = process.cpu_percent()
ram_before = process.memory_info().rss / (1024 * 1024)  # Convertir en MB

# Exemple d'importation de données
with driver.session() as session:
    with open('amazon_reviews.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        for data in reader:
            # Vérifier que la ligne contient suffisamment d'éléments
            if len(data) >= 3:
                try:
                    session.run("CREATE (r:Review {id: $id, text: $text, rating: $rating})",
                                 id=data[0], text=data[1], rating=float(data[2]))
                except ValueError:
                    print(f"Erreur de conversion pour la ligne : {data}")
            else:
                print(f"Ligne mal formatée : {data}")

end_time = time.time()
cpu_after = process.cpu_percent()
ram_after = process.memory_info().rss / (1024 * 1024)  # Convertir en MB

print(f"Temps d'importation dans Neo4j: {end_time - start_time} secondes")
print(f"Consommation CPU avant : {cpu_before}%, après : {cpu_after}%")
print(f"Consommation RAM avant : {ram_before:.2f} MB, après : {ram_after:.2f} MB")

driver.close()