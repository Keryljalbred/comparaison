import riak
import csv
import time
import psutil
from collections.abc import Iterable

# Connexion à Riak
client = riak.RiakClient(pb_port=8087, protocol='pbc')

# Importation des données
start_time = time.time()
process = psutil.Process()
cpu_before = process.cpu_percent()
ram_before = process.memory_info().rss

with open('google_books.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            rating = float(row['rating']) if row['rating'] else 0.0
            price = float(row['price']) if row['price'] else 0.0
            voters = int(row['voters'].replace(',', '').strip()) if row['voters'] else 0
            page_count = int(row['page_count'].replace(',', '').strip()) if row['page_count'] else 0

            obj = client.bucket('books').new(row['ISBN'], data={
                'title': row['title'],
                'author': row['author'],
                'rating': rating,
                'voters': voters,
                'price': price,
                'currency': row['currency'],
                'description': row['description'],
                'publisher': row['publisher'],
                'page_count': page_count,
                'generes': row['generes'],
                'language': row['language'],
                'published_date': row['published_date']
            })
            obj.store()
        except Exception as e:
            print(f"Erreur lors de l'importation de la ligne avec ISBN {row.get('ISBN', 'inconnu')} : {e}")

end_time = time.time()
cpu_after = process.cpu_percent()
ram_after = process.memory_info().rss

print("Temps d'importation dans Riak: {:.2f} secondes".format(end_time - start_time))
print(f"Consommation CPU avant : {cpu_before}%, après : {cpu_after}%")
print(f"Consommation RAM avant : {ram_before / (1024 * 1024):.2f} MB, après : {ram_after / (1024 * 1024):.2f} MB")
