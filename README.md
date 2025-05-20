# 📊 Études de Benchmarking de Bases de Données NoSQL

Ce projet a pour objectif de comparer les performances de différentes bases de données NoSQL selon plusieurs critères : temps d'exécution des opérations, consommation de ressources (CPU/RAM) et efficacité en lecture/écriture/export. Les benchmarks sont réalisés à l’aide de jeux de données réels et variés.

---

## 🔬 Objectifs

- Évaluer les performances des bases NoSQL selon des opérations courantes : **importation**, **CRUD**, **export**.
- Mesurer les **temps d'exécution** et la **consommation CPU/RAM**.
- Utiliser des jeux de données volumineux pour tester les limites de chaque système.
- Produire des **tableaux comparatifs** clairs accompagnés de **synthèses et discussions**.

---

## 📁 Jeux de Données Utilisés

- [Amazon Reviews Dataset (2023)](https://registry.opendata.aws/amazon-reviews/)
- [Google Books Dataset](https://console.cloud.google.com/marketplace/details/googledatasetsearch/books)

---

## 📌 Études de Benchmarking Réalisées

### 1. MongoDB vs ArangoDB

- **Langage de requêtes :** MongoDB Query Language (MQL), AQL (ArangoDB)
- **Mesures :**
  - Importation des documents (temps, CPU/RAM)
  - Opérations CRUD (temps, CPU/RAM)
  - Export des documents (temps, CPU/RAM)
- **Résultat :**
  - Tableau comparatif
  - Discussion sur les cas d’usage appropriés

---

### 2. MongoDB vs RavenDB

- **Langage de requêtes :** MQL, RQL (Raven Query Language)
- **Mesures identiques**
- **Résultat :**
  - Tableau de comparaison et analyse critique des performances

---

### 3. Cassandra vs HBase

- **Langage de requêtes :** CQL vs HQL (HBase Shell / APIs)
- **Focus sur :**
  - Scalabilité horizontale
  - Temps d’écriture/lecture
  - Usage CPU et mémoire en cluster

---

### 4. Neo4j vs Bases de Données Graphes Alternatives

- **Bases comparées :**
  - Neo4j, OrientDB, ArangoDB (mode graphe), JanusGraph, Titan
- **Langage de requêtes :** Cypher vs Gremlin/AQL
- **Mesures :**
  - Temps de traversée de graphe
  - Requêtes multi-hop
  - Consommation mémoire

---

### 5. Amazon DynamoDB vs Riak

- **Langage/API :** DynamoDB SDK, Riak HTTP/Protocol Buffers
- **Focus sur :**
  - Rapidité des opérations key-value
  - Résilience et disponibilité
  - Exportation/backup

---

## ⚙️ Méthodologie

- Scripts en **Python** ou **JavaScript** selon la base
- Mesure du temps avec `time`, `timeit`, ou `perf_counter`
- Utilisation de `psutil` et `top`/`htop` pour la RAM/CPU
- Import via drivers natifs ou fichiers JSON/CSV
- Export en CSV/JSON

---

## 📊 Résultats

Chaque étude produit :

- Un tableau récapitulatif des performances
- Une discussion sur les forces/faiblesses de chaque SGBD
- Des recommandations selon le cas d’usage (IoT, logs, graphes sociaux, etc.)

---


---

## 🧠 Conclusion

Ce projet vise à offrir une vue complète et réaliste des performances des bases de données NoSQL modernes selon différents scénarios d'utilisation. Les résultats obtenus peuvent aider à **choisir la bonne base de données** en fonction du contexte métier et technique.

---

## 📚 Auteurs

- Projet réalisé dans le cadre d’un cours en architecture Big Data et NoSQL.


