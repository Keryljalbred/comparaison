import matplotlib.pyplot as plt
import numpy as np

# Données d'exemple
operations = ['Create', 'Read', 'Update', 'Delete']
neo4j_times = [0.9508, 0.1984, 0.0746, 0.0584]  # Temps en secondes pour Neo4j
arangodb_times = [0.0174, 0.0061, 0.0081, 0.0064]  # Temps en secondes pour ArangoDB

# Position des barres
x = np.arange(len(operations))

# Largeur des barres
width = 0.35

# Création du graphique
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, neo4j_times, width, label='Neo4j', color='blue')
bars2 = ax.bar(x + width/2, arangodb_times, width, label='ArangoDB', color='orange')

# Ajout des labels et titre
ax.set_ylabel('Temps d\'exécution (secondes)')
ax.set_title('Comparaison des opérations CRUD entre Neo4j et ArangoDB')
ax.set_xticks(x)
ax.set_xticklabels(operations)
ax.legend()

# Affichage des valeurs sur les barres
for bar in bars1 + bars2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 4), ha='center', va='bottom')

# Affichage du graphique
plt.tight_layout()
plt.show()