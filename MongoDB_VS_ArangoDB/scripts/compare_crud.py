import json
import pandas as pd

def load_stats(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def compare_crud():
    mongo_data = load_stats("../results/mongo_crud.json")
    arango_data = load_stats("../results/arango_crud.json")

    operations = ["create", "read", "update", "delete"]
    rows = []

    for op in operations:
        mongo_op = mongo_data["crud_stats"][op]
        arango_op = arango_data["crud_stats"][op]
        rows.append({
            "Operation": op.upper(),
            "MongoDB Time (s)": mongo_op["time"],
            "ArangoDB Time (s)": arango_op["time"],
            "MongoDB CPU (%)": mongo_op["cpu"],
            "ArangoDB CPU (%)": arango_op["cpu"],
            "MongoDB RAM (MB)": mongo_op["ram"],
            "ArangoDB RAM (MB)": arango_op["ram"],
        })

    df = pd.DataFrame(rows)
    print("\n📊 COMPARAISON CRUD MongoDB vs ArangoDB")
    print(df.to_string(index=False))

    # Export optionnel
    df.to_csv("../results/comparaison_crud.csv", index=False)
    print("\n✅ Exporté vers '../results/comparaison_crud.csv'")

if __name__ == "__main__":
    compare_crud()
