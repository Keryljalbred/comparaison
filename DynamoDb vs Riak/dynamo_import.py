import boto3
import csv
import time
import psutil
from decimal import Decimal, InvalidOperation
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Connexion à DynamoDB
try:
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')  # Remplacez par votre région
    table = dynamodb.Table('Books')
except (NoCredentialsError, PartialCredentialsError):
    print("Erreur : Impossible de localiser les informations d'identification AWS.")
    exit(1)

# Importation des données
start_time = time.time()
process = psutil.Process()
cpu_before = process.cpu_percent()
ram_before = process.memory_info().rss

try:
    with open('google_books.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                table.put_item(
                    Item={
                        'ISBN': row['ISBN'],
                        'title': row['title'],
                        'author': row['author'],
                        'rating': Decimal(row['rating']),
                        'voters': int(row['voters'].replace(',', '')), 
                        'price': Decimal(row['price']),
                        'currency': row['currency'],
                        'description': row['description'],
                        'publisher': row['publisher'],
                        'page_count': int(row['page_count']),
                        'generes': row['generes'],  
                        'language': row['language'],
                        'published_date': row['published_date']
                    }
                )
            except (InvalidOperation, ValueError) as e:
                print(f"Erreur de conversion pour la ligne : {row} - {e}")
except FileNotFoundError:
    print("Erreur : Le fichier 'google_books.csv' est introuvable.")
    exit(1)
except Exception as e:
    print(f"Erreur lors de l'importation des données : {e}")
    exit(1)

end_time = time.time()
cpu_after = process.cpu_percent()
ram_after = process.memory_info().rss

print(f"Temps d'importation dans DynamoDB: {end_time - start_time} secondes")
print(f"Consommation CPU avant : {cpu_before}%, après : {cpu_after}%")
print(f"Consommation RAM avant : {ram_before / (1024 * 1024)} MB, après : {ram_after / (1024 * 1024)} MB")