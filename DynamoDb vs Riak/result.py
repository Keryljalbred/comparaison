import subprocess
import pandas as pd
import re
import psutil
import time

def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    return result.stdout

def extract_time(output):
    match = re.search(r"(\d+\.\d+|\d+) secondes", output)
    if match:
        return float(match.group(1))
    return None

def resource_usage():
    process = psutil.Process()
    cpu = process.cpu_percent()
    ram = process.memory_info().rss / (1024 * 1024)  # Convertir en MB
    return cpu, ram

def main():
    # Créer un tableau pour stocker les résultats
    data = {
        'Opération': ['Importation', 'CRUD (Create)', 'CRUD (Read)', 'CRUD (Update)', 'CRUD (Delete)', 'Exportation'],
        'DynamoDB (Temps)': [None] * 6,
        'DynamoDB (CPU/RAM)': [None] * 6,
        'Riak (Temps)': [None] * 6,
        'Riak (CPU/RAM)': [None] * 6,
    }

    # Importation
    dynamo_import_results = run_script('dynamo_import.py')
    data['DynamoDB (Temps)'][0] = extract_time(dynamo_import_results)
    data['DynamoDB (CPU/RAM)'][0] = resource_usage()

    # CRUD pour DynamoDB
    # Create
    run_script('dynamo_crud_create.py')
    data['DynamoDB (Temps)'][1] = None
    data['DynamoDB (CPU/RAM)'][1] = resource_usage()

    # Read
    run_script('dynamo_crud_read.py')
    data['DynamoDB (Temps)'][2] = None
    data['DynamoDB (CPU/RAM)'][2] = resource_usage()

    # Update
    run_script('dynamo_crud_update.py')
    data['DynamoDB (Temps)'][3] = None
    data['DynamoDB (CPU/RAM)'][3] = resource_usage()

    # Delete
    run_script('dynamo_crud_delete.py')
    data['DynamoDB (Temps)'][4] = None
    data['DynamoDB (CPU/RAM)'][4] = resource_usage()

    # Exportation
    dynamo_export_results = run_script('dynamo_export.py')
    data['DynamoDB (Temps)'][5] = extract_time(dynamo_export_results)
    data['DynamoDB (CPU/RAM)'][5] = resource_usage()

    # Importation Riak
    riak_import_results = run_script('riak_import.py')
    data['Riak (Temps)'][0] = extract_time(riak_import_results)
    data['Riak (CPU/RAM)'][0] = resource_usage()

    # CRUD pour Riak
    # Create
    run_script('riak_crud_create.py')
    data['Riak (Temps)'][1] = None
    data['Riak (CPU/RAM)'][1] = resource_usage()

    # Read
    run_script('riak_crud_read.py')
    data['Riak (Temps)'][2] = None
    data['Riak (CPU/RAM)'][2] = resource_usage()

    # Update
    run_script('riak_crud_update.py')
    data['Riak (Temps)'][3] = None
    data['Riak (CPU/RAM)'][3] = resource_usage()

    # Delete
    run_script('riak_crud_delete.py')
    data['Riak (Temps)'][4] = None
    data['Riak (CPU/RAM)'][4] = resource_usage()

    # Exportation Riak
    riak_export_results = run_script('riak_export.py')
    data['Riak (Temps)'][5] = extract_time(riak_export_results)
    data['Riak (CPU/RAM)'][5] = resource_usage()

    # Créer un DataFrame et afficher le tableau
    df = pd.DataFrame(data)
    print(df)

if __name__ == "__main__":
    main()