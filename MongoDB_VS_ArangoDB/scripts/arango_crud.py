import time
import psutil
from pyArango.connection import Connection
from utils import save_stats_to_json, timestamp

# Utilisation RAM du processus arangod (en MB)
def get_arangodb_ram_usage():
    for proc in psutil.process_iter(attrs=["name", "memory_info"]):
        if "arangod" in proc.info["name"]:
            return proc.info["memory_info"].rss / 1024 / 1024
    return 0.0

# CPU utilisé par le script
def get_script_cpu():
    process = psutil.Process()
    return process.cpu_percent(interval=1)

def run_crud_arango():
    conn = Connection(arangoURL="http://localhost:8529", username="root", password="rootpassword")
    db = conn["benchmark"]
    col = db["amazon_reviews"]

    sample_doc = {
        "_key": "TEST123",
        "reviewerID": "TEST123",
        "asin": "B000TEST",
        "reviewText": "This is a test review.",
        "overall": "5.0"
    }

    stats = {}

    # CREATE
    start = time.time(); cpu1 = get_script_cpu(); ram1 = get_arangodb_ram_usage()
    col.createDocument(sample_doc).save()
    cpu2 = get_script_cpu(); ram2 = get_arangodb_ram_usage(); end = time.time()
    stats["create"] = {
        "time": round(end - start, 4),
        "cpu": round(cpu2 - cpu1, 2),
        "ram": round(ram2 - ram1, 2)
    }

    # READ
    start = time.time(); cpu1 = get_script_cpu(); ram1 = get_arangodb_ram_usage()
    doc = col.fetchDocument("TEST123")
    cpu2 = get_script_cpu(); ram2 = get_arangodb_ram_usage(); end = time.time()
    stats["read"] = {
        "time": round(end - start, 4),
        "cpu": round(cpu2 - cpu1, 2),
        "ram": round(ram2 - ram1, 2)
    }

    # UPDATE
    start = time.time(); cpu1 = get_script_cpu(); ram1 = get_arangodb_ram_usage()
    doc["overall"] = "4.0"
    doc.save()
    cpu2 = get_script_cpu(); ram2 = get_arangodb_ram_usage(); end = time.time()
    stats["update"] = {
        "time": round(end - start, 4),
        "cpu": round(cpu2 - cpu1, 2),
        "ram": round(ram2 - ram1, 2)
    }

    # DELETE
    start = time.time(); cpu1 = get_script_cpu(); ram1 = get_arangodb_ram_usage()
    doc.delete()
    cpu2 = get_script_cpu(); ram2 = get_arangodb_ram_usage(); end = time.time()
    stats["delete"] = {
        "time": round(end - start, 4),
        "cpu": round(cpu2 - cpu1, 2),
        "ram": round(ram2 - ram1, 2)
    }

    result = {
        "timestamp": timestamp(),
        "database": "ArangoDB",
        "collection": "amazon_reviews",
        "crud_stats": stats
    }

    save_stats_to_json(result, "../results/arango_crud.json")
    print("\n✅ CRUD ArangoDB terminé :")
    for k, v in stats.items():
        print(f"{k.upper()}: {v}")

if __name__ == "__main__":
    run_crud_arango()
