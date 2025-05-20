import boto3
import time
import psutil
from decimal import Decimal
from botocore.exceptions import ClientError

# Connexion à DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
table = dynamodb.Table('Books')

# Préparation (convertir float en Decimal)
item = {
    'ISBN': '9999999999999',
    'title': 'Test Book',
    'author': 'John Doe',
    'rating': Decimal('4.7'),
    'voters': 123,
    'price': Decimal('19.99'),
    'currency': 'USD',
    'description': 'A test book for benchmarking.',
    'publisher': 'TestPub',
    'page_count': 300,
    'generes': 'Fiction',
    'language': 'en',
    'published_date': '2024-01-01'
}

process = psutil.Process()

# CREATE
cpu_before = process.cpu_percent(interval=None)
ram_before = process.memory_info().rss
start = time.time()
table.put_item(Item=item)
end = time.time()
cpu_after = process.cpu_percent(interval=None)
ram_after = process.memory_info().rss
print(f"[CREATE] Temps: {end - start:.6f} sec | CPU: {cpu_after:.2f}% | RAM: {(ram_after - ram_before) / (1024 * 1024):.3f} MB")

# READ
cpu_before = process.cpu_percent(interval=None)
ram_before = process.memory_info().rss
start = time.time()
response = table.get_item(Key={'ISBN': '9999999999999'})
end = time.time()
cpu_after = process.cpu_percent(interval=None)
ram_after = process.memory_info().rss
print(f"[READ]   Temps: {end - start:.6f} sec | CPU: {cpu_after:.2f}% | RAM: {(ram_after - ram_before) / (1024 * 1024):.3f} MB")

# UPDATE
cpu_before = process.cpu_percent(interval=None)
ram_before = process.memory_info().rss
start = time.time()
table.update_item(
    Key={'ISBN': '9999999999999'},
    UpdateExpression='SET price = :p',
    ExpressionAttributeValues={':p': Decimal('24.99')}
)
end = time.time()
cpu_after = process.cpu_percent(interval=None)
ram_after = process.memory_info().rss
print(f"[UPDATE] Temps: {end - start:.6f} sec | CPU: {cpu_after:.2f}% | RAM: {(ram_after - ram_before) / (1024 * 1024):.3f} MB")

# DELETE
cpu_before = process.cpu_percent(interval=None)
ram_before = process.memory_info().rss
start = time.time()
table.delete_item(Key={'ISBN': '9999999999999'})
end = time.time()
cpu_after = process.cpu_percent(interval=None)
ram_after = process.memory_info().rss
print(f"[DELETE] Temps: {end - start:.6f} sec | CPU: {cpu_after:.2f}% | RAM: {(ram_after - ram_before) / (1024 * 1024):.3f} MB")
