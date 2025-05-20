import time
import psutil
import pandas as pd
from pyArango.connection import Connection
from tqdm import tqdm
from utils import save_stats_to_json, timestamp

# Récupère la mémoire utilisée par le processus arangod (en MB)
def get_arangodb_ram_usage():
    for proc in psutil.process_iter(attrs=["pid", "name", "memory_info"]):
        if "arangod" in proc.info["name"]:
            return proc.info["memory_info"].rss / 1024 / 1024
    return 0.0

# Récupère l'utilisation CPU du script Python
def get_script_cpu():
    process = psutil.Process()
    return process.cpu_percent(interval=1)

# Fonction d'import
def import_csv_to_arango(filename, collection_name, db):
    print(f"\n--- Importation : {filename} --> {collection_name} ---")

    # Lecture du CSV
    df = pd.read_csv(filename).fillna("").astype(str)
    records = df.to_dict(orient='records')

    # Création collection si absente
    if not db.hasCollection(collection_name):
        db.createCollection(name=collection_name)

    collection = db[collection_name]

    start_time = time.time()
    start_cpu = get_script_cpu()
    start_mem = get_arangodb_ram_usage()

    # Insertion par batchs
    batch_size = 1000
    for i in tqdm(range(0, len(records), batch_size), desc=f"Insertion {collection_name}"):
        batch = records[i:i+batch_size]
        for doc in batch:
            collection.createDocument(doc).save()

    end_time = time.time()
    end_cpu = get_script_cpu()
    end_mem = get_arangodb_ram_usage()

    stats = {
        "collection": collection_name,
        "time_seconds": round(end_time - start_time, 2),
        "cpu_percent": round(end_cpu - start_cpu, 2),
        "ram_mb": round(end_mem - start_mem, 2),
        "documents_inserted": len(records)
    }

    return stats

if __name__ == "__main__":
    # Connexion ArangoDB
    conn = Connection(arangoURL="http://localhost:8529", username="root", password="rootpassword")

    # Création BDD si elle n'existe pas
    if not conn.hasDatabase("benchmark"):
        conn.createDatabase(name="benchmark")
    db = conn["benchmark"]

    # Import des jeux de données
    amazon_stats = import_csv_to_arango("../amazon_reviews.csv", "amazon_reviews", db)
    books_stats = import_csv_to_arango("../google_books.csv", "google_books", db)

    # Résumé
    all_stats = {
        "timestamp": timestamp(),
        "database": "ArangoDB",
        "import": {
            "amazon_reviews": amazon_stats,
            "google_books": books_stats
        }
    }

    save_stats_to_json(all_stats, "../results/arango_stats.json")

    print("\n✅ Statistiques d'importation ArangoDB :")
    print(amazon_stats)
    print(books_stats)
