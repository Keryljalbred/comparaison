import riak
import time
import psutil

client = riak.RiakClient(pb_port=8087, protocol='pbc')
bucket = client.bucket('books')
process = psutil.Process()

def measure(action, func):
    cpu_before = process.cpu_percent(interval=None)
    ram_before = process.memory_info().rss
    start = time.time()

    func()

    end = time.time()
    cpu_after = process.cpu_percent(interval=None)
    ram_after = process.memory_info().rss
    print(f"{action} - Temps: {end - start:.4f}s | CPU: {cpu_after:.4f}% | RAM: {(ram_after - ram_before) / (1024 * 1024):.4f} MB")

isbn_test = 'test-123'

# CREATE
measure("CREATE", lambda: bucket.new(isbn_test, data={
    'title': 'Test Book',
    'author': 'John Doe',
    'rating': 4.5
}).store())

# READ
measure("READ", lambda: bucket.get(isbn_test).data)

# UPDATE
measure("UPDATE", lambda: (lambda o: (o.data.update({'rating': 5.0}), o.store()))(bucket.get(isbn_test)))

# DELETE
measure("DELETE", lambda: bucket.get(isbn_test).delete())
