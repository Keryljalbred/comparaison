import time
import psutil
import pandas as pd
from pymongo import MongoClient
from tqdm import tqdm

# Récupère la mémoire utilisée par le processus mongod (en MB)
def get_mongodb_ram_usage():
    for proc in psutil.process_iter(attrs=["pid", "name", "memory_info"]):
        if "mongod" in proc.info["name"]:
            return proc.info["memory_info"].rss / 1024 / 1024  # Convertir en MB
    return 0.0

# Récupère l'utilisation CPU de ce script uniquement
def get_script_cpu():
    process = psutil.Process()
    return process.cpu_percent(interval=1)

# Importer un fichier CSV dans une collection MongoDB
def import_csv_to_mongo(filename, collection_name):
    # Connexion MongoDB
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    db = client["benchmark"]
    collection = db[collection_name]

    print(f"\n--- Importation : {filename} --> {collection_name} ---")

    # Lecture CSV
    df = pd.read_csv(filename)
    records = df.to_dict(orient='records')

    start_time = time.time()
    start_cpu = get_script_cpu()
    start_mem = get_mongodb_ram_usage()

    # Insertion avec barre de progression
    batch_size = 1000
    for i in tqdm(range(0, len(records), batch_size), desc=f"Insertion {collection_name}"):
        collection.insert_many(records[i:i + batch_size])

    end_time = time.time()
    end_cpu = get_script_cpu()
    end_mem = get_mongodb_ram_usage()

    # Résultats
    stats = {
        "collection": collection_name,
        "time_seconds": round(end_time - start_time, 2),
        "cpu_percent": round(end_cpu - start_cpu, 2),
        "ram_mb": round(end_mem - start_mem, 2),
        "documents_inserted": len(records)
    }

    return stats

if __name__ == "__main__":
    # Import des deux datasets
    amazon_stats = import_csv_to_mongo("../amazon_reviews.csv", "amazon_reviews")
    books_stats = import_csv_to_mongo("../google_books.csv", "google_books")

    # Résumé
    print("\n✅ Statistiques d'importation MongoDB :")
    print(amazon_stats)
    print(books_stats)

    # Sauvegarde JSON
    from utils import save_stats_to_json, timestamp

    all_stats = {
        "timestamp": timestamp(),
        "database": "MongoDB",
        "import": {
            "amazon_reviews": amazon_stats,
            "google_books": books_stats
        }
    }

    save_stats_to_json(all_stats, "../results/mongo_stats.json")
