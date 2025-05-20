from arango import ArangoClient
import time
import psutil
import csv

# Connexion à ArangoDB
client = ArangoClient()
db = client.db('mydatabase', username='root', password='password')  

# Mesurer le temps d'importation
start_time = time.time()
process = psutil.Process()
cpu_before = process.cpu_percent()
ram_before = process.memory_info().rss / (1024 * 1024)  # Convertir en MB


with open('amazon_reviews.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader) 
    for data in reader:
        
        if len(data) >= 3:
            try:
                db.collection('reviews').insert({
                    'id': data[0],
                    'text': data[1],
                    'rating': float(data[2])  
                })
            except ValueError:
                print(f"Erreur de conversion pour la ligne : {data}")
        else:
            print(f"Ligne mal formatée : {data}")

end_time = time.time()
cpu_after = process.cpu_percent()
ram_after = process.memory_info().rss / (1024 * 1024)  # Convertir en MB

print(f"Temps d'importation dans ArangoDB: {end_time - start_time} secondes")
print(f"Consommation CPU avant : {cpu_before}%, après : {cpu_after}%")
print(f"Consommation RAM avant : {ram_before:.2f} MB, après : {ram_after:.2f} MB")