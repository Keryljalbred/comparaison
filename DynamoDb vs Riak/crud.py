import matplotlib.pyplot as plt
import numpy as np

# Données
operations = ['Create', 'Read', 'Update', 'Delete']
dynamo_time = [0.602997, 0.018058, 0.015015, 0.031985]
riak_time   = [0.0131,    0.0031,   0.0078,   0.0095]

dynamo_cpu = [82.90, 0.00, 0.00, 0.00]
riak_cpu   = [98.40, 0.00, 0.00, 0.00]

dynamo_ram = [3.117, 0.059, 0.039, 0.020]
riak_ram   = [0.5742, 0.078, 0.039, 0.039]

x = np.arange(len(operations))
width = 0.35

# --- Graphe 1 : Temps d'exécution ---
plt.figure(figsize=(10, 5))
bars1 = plt.bar(x - width/2, dynamo_time, width, label='DynamoDB', color='skyblue')
bars2 = plt.bar(x + width/2, riak_time, width, label='Riak', color='orange')

# Ajouter les valeurs au-dessus des barres
for bar in bars1 + bars2:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.002, f'{yval:.3f}', ha='center', va='bottom', fontsize=9)

plt.ylabel('Temps (secondes)')
plt.title('Comparaison du temps d\'exécution CRUD')
plt.xticks(x, operations)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- Graphe 2 : CPU et RAM ---
fig, ax1 = plt.subplots(figsize=(10, 6))

bar_width = 0.2
x = np.arange(len(operations))

cpu_dynamo = ax1.bar(x - bar_width, dynamo_cpu, bar_width, label='CPU DynamoDB', color='blue')
cpu_riak   = ax1.bar(x, riak_cpu, bar_width, label='CPU Riak', color='red')

ax1.set_ylabel('CPU (%)')
ax1.set_ylim(0, max(max(dynamo_cpu), max(riak_cpu)) + 20)
ax1.set_xticks(x)
ax1.set_xticklabels(operations)

# Ajouter les valeurs CPU
for bar in cpu_dynamo + cpu_riak:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.1f}', ha='center', va='bottom', fontsize=9)

# Deuxième axe pour la RAM
ax2 = ax1.twinx()
ram_dynamo = ax2.bar(x + bar_width, dynamo_ram, bar_width, label='RAM DynamoDB', color='green')
ram_riak   = ax2.bar(x + 2 * bar_width, riak_ram, bar_width, label='RAM Riak', color='purple')
ax2.set_ylabel('RAM (MB)')

# Ajouter les valeurs RAM
for bar in ram_dynamo + ram_riak:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, f'{yval:.2f}', ha='center', va='bottom', fontsize=9)

# Combiner les légendes
lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, loc='upper center', ncol=4)

plt.title('Comparaison de la consommation CPU et RAM par opération CRUD')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
