import matplotlib.pyplot as plt
import numpy as np

# Données d'exemple
bases_de_donnees = ['Dynamo', 'Riak']
temps_importation = [20.9409, 4.98]  # Temps en secondes
cpu_avant = [0.0, 0.0]  # Consommation CPU avant
cpu_apres = [26.8, 15.7]  # Consommation CPU après
ram_avant = [49.582, 39.27]  # RAM avant en MB
ram_apres = [54.0625, 39.27]  # RAM après en MB

# Graphique 1 : Temps d'importation
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.bar(bases_de_donnees, temps_importation, color=['blue', 'orange'])
plt.ylabel('Temps d\'importation (secondes)')
plt.title('Comparaison du temps d\'importation entre Dynamo et Riak')

# Graphique 2 : Consommation CPU et RAM
x = np.arange(len(bases_de_donnees))  # Position des barres
width = 0.2  # Largeur des barres

plt.subplot(1, 2, 2)
plt.bar(x - width, cpu_avant, width, label='CPU Avant (%)', color='lightblue')
plt.bar(x, cpu_apres, width, label='CPU Après (%)', color='blue')
plt.bar(x + width, ram_avant, width, label='RAM Avant (MB)', color='lightgreen')
plt.bar(x + 2*width, ram_apres, width, label='RAM Après (MB)', color='green')

plt.ylabel('Consommation')
plt.title('Comparaison de la consommation CPU et RAM')
plt.xticks(x + width, bases_de_donnees)
plt.legend()

# Affichage des graphiques
plt.tight_layout()
plt.show()