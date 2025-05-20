import json
import pandas as pd
from fpdf import FPDF

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
        rows.append([
            op.upper(),
            mongo_op["time"], arango_op["time"],
            mongo_op["cpu"], arango_op["cpu"],
            mongo_op["ram"], arango_op["ram"]
        ])

    columns = [
        "Operation",
        "MongoDB Time (s)", "ArangoDB Time (s)",
        "MongoDB CPU (%)", "ArangoDB CPU (%)",
        "MongoDB RAM (MB)", "ArangoDB RAM (MB)"
    ]

    df = pd.DataFrame(rows, columns=columns)
    return df

def generate_pdf(df, output_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Comparatif des performances CRUD: MongoDB vs ArangoDB", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 10)
    col_widths = [30, 30, 30, 30, 30, 30, 30]
    line_height = 10

    # Header
    for i, col in enumerate(df.columns):
        pdf.cell(col_widths[i], line_height, col, border=1, align="C")
    pdf.ln()

    # Rows
    pdf.set_font("Arial", "", 10)
    for _, row in df.iterrows():
        for i, item in enumerate(row):
            pdf.cell(col_widths[i], line_height, str(item), border=1, align="C")
        pdf.ln()

    pdf.output(output_file)
    print(f"\n📄 PDF généré : {output_file}")

if __name__ == "__main__":
    df = compare_crud()
    generate_pdf(df, "../results/comparaison_crud.pdf")
