import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
import_df = pd.read_csv("../results/comparaison_import1.xlsx")
crud_df = pd.read_csv("../results/comparaison_crud.csv")

# === GRAPHIQUE 1 : Importation - Temps ===
plt.figure(figsize=(10, 5))
plt.bar(import_df["Dataset"], import_df["MongoDB Time (s)"], label="MongoDB", width=0.4, align="edge")
plt.bar(import_df["Dataset"], import_df["ArangoDB Time (s)"], label="ArangoDB", width=-0.4, align="edge")
plt.ylabel("Temps (secondes)")
plt.title("⏱️ Temps d'importation par base de données")
plt.legend()
plt.tight_layout()
plt.savefig("../results/graph_import_time.png")
plt.close()

# === GRAPHIQUE 2 : CRUD - Temps par opération ===
plt.figure(figsize=(10, 5))
plt.bar(crud_df["Operation"], crud_df["MongoDB Time (s)"], label="MongoDB", width=0.4, align="edge")
plt.bar(crud_df["Operation"], crud_df["ArangoDB Time (s)"], label="ArangoDB", width=-0.4, align="edge")
plt.ylabel("Temps (secondes)")
plt.title("⚙️ Temps d'exécution des opérations CRUD")
plt.legend()
plt.tight_layout()
plt.savefig("../results/graph_crud_time.png")
plt.close()

print("✅ Graphiques générés :")
print("- ../results/graph_import_time.png")
print("- ../results/graph_crud_time.png")
