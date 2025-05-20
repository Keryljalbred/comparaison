import time
import psutil
from pymongo import MongoClient
from utils import save_stats_to_json, timestamp

# RAM utilisée par mongod (en MB)
def get_mongo_ram_usage():
    for proc in psutil.process_iter(attrs=["name", "memory_info"]):
        if "mongod" in proc.info["name"]:
            return proc.info["memory_info"].rss / 1024 / 1024
    return 0.0

# CPU utilisé par le script
def get_script_cpu():
    process = psutil.Process()
    return process.cpu_percent(interval=1)

def run_crud_mongo():
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    db = client["benchmark"]
    collection = db["amazon_reviews"]

    sample_doc = {
        "reviewerID": "TEST123",
        "asin": "B000TEST",
        "reviewText": "This is a test review.",
        "overall": 5.0
    }

    stats = {}

    # CREATE
    start = time.time(); cpu1 = get_script_cpu(); ram1 = get_mongo_ram_usage()
    collection.insert_one(sample_doc)
    cpu2 = get_script_cpu(); ram2 = get_mongo_ram_usage(); end = time.time()
    stats["create"] = {
        "time": round(end - start, 4),
        "cpu": round(cpu2 - cpu1, 2),
        "ram": round(ram2 - ram1, 2)
    }

    # READ
    start = time.time(); cpu1 = get_script_cpu(); ram1 = get_mongo_ram_usage()
    doc = collection.find_one({"reviewerID": "TEST123"})
    cpu2 = get_script_cpu(); ram2 = get_mongo_ram_usage(); end = time.time()
    stats["read"] = {
        "time": round(end - start, 4),
        "cpu": round(cpu2 - cpu1, 2),
        "ram": round(ram2 - ram1, 2)
    }

    # UPDATE
    start = time.time(); cpu1 = get_script_cpu(); ram1 = get_mongo_ram_usage()
    collection.update_one({"reviewerID": "TEST123"}, {"$set": {"overall": 4.0}})
    cpu2 = get_script_cpu(); ram2 = get_mongo_ram_usage(); end = time.time()
    stats["update"] = {
        "time": round(end - start, 4),
        "cpu": round(cpu2 - cpu1, 2),
        "ram": round(ram2 - ram1, 2)
    }

    # DELETE
    start = time.time(); cpu1 = get_script_cpu(); ram1 = get_mongo_ram_usage()
    collection.delete_one({"reviewerID": "TEST123"})
    cpu2 = get_script_cpu(); ram2 = get_mongo_ram_usage(); end = time.time()
    stats["delete"] = {
        "time": round(end - start, 4),
        "cpu": round(cpu2 - cpu1, 2),
        "ram": round(ram2 - ram1, 2)
    }

    result = {
        "timestamp": timestamp(),
        "database": "MongoDB",
        "collection": "amazon_reviews",
        "crud_stats": stats
    }

    save_stats_to_json(result, "../results/mongo_crud.json")
    print("\n✅ CRUD MongoDB terminé :")
    for k, v in stats.items():
        print(f"{k.upper()}: {v}")

if __name__ == "__main__":
    run_crud_mongo()
