import json
import pandas as pd
from datetime import datetime

# Charger les fichiers JSON
def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Création tableau comparatif
def generate_comparison_table(mongo_stats, arango_stats):
    datasets = ["amazon_reviews", "google_books"]
    rows = []

    for dataset in datasets:
        mongo_data = mongo_stats["import"][dataset]
        arango_data = arango_stats["import"][dataset]

        rows.append({
            "Dataset": dataset,
            "MongoDB Time (s)": mongo_data["time_seconds"],
            "ArangoDB Time (s)": arango_data["time_seconds"],
            "MongoDB CPU (%)": mongo_data["cpu_percent"],
            "ArangoDB CPU (%)": arango_data["cpu_percent"],
            "MongoDB RAM (MB)": mongo_data["ram_mb"],
            "ArangoDB RAM (MB)": arango_data["ram_mb"]
        })

    df = pd.DataFrame(rows)
    return df

def save_table(df, filename):
    df.to_csv(filename, index=False)
    print(f"✅ Tableau exporté en CSV : {filename}")

if __name__ == "__main__":
    # Chargement des fichiers JSON
    mongo_stats = load_json("../results/mongo_stats.json")
    arango_stats = load_json("../results/arango_stats.json")

    # Génération tableau
    df = generate_comparison_table(mongo_stats, arango_stats)

    # Affichage
    print("\n📊 Tableau comparatif des performances d'importation :")
    print(df.to_string(index=False))

    # Export CSV
    save_table(df, "../results/comparaison_import1.xlsx")
