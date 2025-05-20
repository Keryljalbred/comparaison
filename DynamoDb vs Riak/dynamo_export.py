import boto3
import time
import psutil

# Connexion à DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3') 
table = dynamodb.Table('Books')

# Mesurer le temps d'exportation
start_time = time.time()
process = psutil.Process()
cpu_before = process.cpu_percent()
ram_before = process.memory_info().rss

# Exportation des données
response = table.scan()
items = response['Items']

# Afficher les éléments exportés
for item in items:
    print(item)

# Mesurer la fin de l'exportation
end_time = time.time()
cpu_after = process.cpu_percent()
ram_after = process.memory_info().rss

print(f"Temps d'exportation dans DynamoDB: {end_time - start_time} secondes")
print(f"Consommation CPU avant : {cpu_before}%, après : {cpu_after}%")
print(f"Consommation RAM avant : {ram_before / (1024 * 1024)} MB, après : {ram_after / (1024 * 1024)} MB")