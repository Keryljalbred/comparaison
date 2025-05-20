import matplotlib.pyplot as plt

# Données d'exemple
bases_de_donnees = ['Neo4j', 'ArangoDB']
temps_importation = [5.2, 3.8]  # Temps en secondes

# Création du graphique
plt.figure(figsize=(8, 5))
plt.bar(bases_de_donnees, temps_importation, color=['blue', 'orange'])
plt.ylabel('Temps d\'importation (secondes)')
plt.title('Comparaison des temps d\'importation entre Neo4j et ArangoDB')
plt.ylim(0, max(temps_importation) + 2)

# Affichage des valeurs sur les barres
for i, v in enumerate(temps_importation):
    plt.text(i, v + 0.1, str(v), ha='center')

# Affichage du graphique
plt.show()