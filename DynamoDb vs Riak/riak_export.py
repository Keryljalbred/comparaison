import riak
import time
import psutil

# Connexion à Riak
client = riak.RiakClient(pb_port=8087, protocol='pbc')
bucket = client.bucket('books')

# Mesurer le temps d'exportation
start_time = time.time()
process = psutil.Process()
cpu_before = process.cpu_percent()
ram_before = process.memory_info().rss

# Exportation des données
keys = bucket.get_keys()
items = []

for key in keys:
    obj = bucket.get(key)
    items.append(obj.data)

# Afficher les éléments exportés
for item in items:
    print(item)

# Mesurer la fin de l'exportation
end_time = time.time()
cpu_after = process.cpu_percent()
ram_after = process.memory_info().rss

print(f"Temps d'exportation dans Riak: {end_time - start_time} secondes")
print(f"Consommation CPU avant : {cpu_before}%, après : {cpu_after}%")
print(f"Consommation RAM avant : {ram_before / (1024 * 1024)} MB, après : {ram_after / (1024 * 1024)} MB")