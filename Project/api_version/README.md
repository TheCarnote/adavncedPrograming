# 🔍 API de Recherche dans un Graphe Publicitaire

## 📋 Description

Cette API FastAPI permet de construire et d'interroger un graphe publicitaire basé sur des algorithmes de recherche optimisés. Le système utilise des nœuds réguliers (utilisateurs) connectés par similarité K-NN et des annonces publicitaires avec des rayons de recherche personnalisés.

### Fonctionnalités principales
- **Construction automatique de graphes** avec algorithme K-NN
- **4 algorithmes de recherche** : Naïve, BFS, Dijkstra, Hybrid
- **Distance pondérée personnalisée** basée sur les caractéristiques publicitaires
- **API REST complète** avec documentation Swagger intégrée
- **Génération de rapports CSV** pour l'analyse des performances
- **Upload dynamique de données** via interface web

## 🚀 Installation et Configuration

### Prérequis
- **Python 3.8+** (testé avec Python 3.13)
- **pip** (gestionnaire de packages Python)

### Installation rapide
```bash
# 1. Naviguer vers le dossier du projet
cd api_version

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le serveur
python main.py
```

Le serveur démarre sur **http://localhost:8000**

### Vérification de l'installation
```bash
# Test rapide des dépendances
python -c "import fastapi, pandas, numpy, networkx, sklearn; print('✅ Installation réussie')"

# Accès à la documentation
# Ouvrir http://localhost:8000/docs dans le navigateur
```

## 📊 Format des Données

### Structure attendue des fichiers

#### Fichier Nodes (`adsSim_data_nodes.csv`)
```csv
node_id,feature_0,feature_1,feature_2,...,feature_49
N1,45.23,67.89,12.34,...,89.56
N2,34.56,78.90,23.45,...,90.67
N3,56.78,89.01,34.56,...,01.23
```

**Spécifications :**
- **51 colonnes** : `node_id` + 50 features numériques
- **Features** : Caractéristiques comportementales (âge, revenus, affinités...)
- **Valeurs** : Nombres réels entre 0 et 100
- **Format** : CSV standard avec virgule comme séparateur

#### Fichier Ads (`queries_structured.csv`)
```csv
ad_id,point_A,Y_vector,D
A1,0.1234;0.5678;0.9012;...,0.123456,15.789
A2,0.2345;0.6789;0.0123;...,0.234567,23.456
A3,0.3456;0.7890;0.1234;...,0.345678,18.234
```

**Spécifications :**
- **ad_id** : Identifiant unique de l'annonce (ex: A1, A2...)
- **point_A** : 50 valeurs séparées par `;` (coordonnées dans l'espace des features)
- **Y_vector** : Coefficient de pondération numérique (0.0 à 1.0)
- **D** : Rayon de recherche (distance maximale pour la recherche)

## 🔧 API Endpoints

### 🏠 `GET /` - Page d'accueil
Informations générales sur l'API et liste des endpoints disponibles.

### 📤 `POST /upload-files` - Upload des données
Upload des fichiers CSV pour alimenter le système.

**Paramètres :**
```bash
curl -X POST "http://localhost:8000/upload-files" \
  -F "nodes_file=@adsSim_data_nodes.csv" \
  -F "ads_file=@queries_structured.csv"
```

**Réponse :**
```json
{
  "message": "Fichiers uploadés avec succès",
  "nodes_file": "adsSim_data_nodes.csv",
  "ads_file": "queries_structured.csv",
  "nodes_count": 1000,
  "ads_count": 100
}
```

### 🏗️ `POST /build-graph` - Construction du graphe
Construit le graphe K-NN à partir des données uploadées.

**Corps de la requête :**
```json
{
  "k": 15
}
```

```bash
curl -X POST "http://localhost:8000/build-graph" \
  -H "Content-Type: application/json" \
  -d '{"k": 15}'
```

**Réponse :**
```json
{
  "message": "Graphe construit avec succès (K=15)",
  "stats": {
    "total_nodes": 1100,
    "regular_nodes": 1000,
    "ad_nodes": 100,
    "total_edges": 15000,
    "k_value": 15,
    "build_time": 3.456
  }
}
```

### 📊 `GET /stats` - Statistiques du graphe
Obtient les métriques détaillées du graphe construit.

```bash
curl -X GET "http://localhost:8000/stats"
```

**Réponse :**
```json
{
  "total_nodes": 1100,
  "regular_nodes": 1000,
  "ad_nodes": 100,
  "total_edges": 15000,
  "average_degree": 27.27,
  "density": 0.0247,
  "build_time": 3.456,
  "memory_usage": "245MB"
}
```

### 📈 `GET /graph-data` - Données de visualisation
Récupère les données formatées pour la visualisation 3D.

**Paramètres :**
- `fx`, `fy`, `fz` (optionnels) : Indices des features pour les axes X, Y, Z

```bash
curl -X GET "http://localhost:8000/graph-data?fx=0&fy=1&fz=2"
```

### 🔍 `POST /search` - Recherche ciblée
Recherche les nœuds dans le rayon D d'une annonce spécifique.

**Corps de la requête :**
```json
{
  "ad_id": "A1",
  "method": "hybrid"
}
```

**Méthodes disponibles :**
- `naive` : Parcours exhaustif O(N)
- `bfs` : Parcours en largeur O(E)  
- `dijkstra` : Parcours avec priorité O(E log V)
- `hybrid` : Sélection automatique selon le contexte

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"ad_id": "A1", "method": "hybrid"}'
```

**Réponse :**
```json
{
  "ad_id": "A1",
  "radius_D": 15.789,
  "method_used": "hybrid",
  "strategy_chosen": "bfs",
  "nodes_found": [
    {"node_id": "N1", "distance": 12.345},
    {"node_id": "N2", "distance": 14.678}
  ],
  "total_nodes": 2,
  "elapsed_time": 0.045,
  "nodes_checked": 234
}
```

### 🔍 `POST /search-all` - Recherche globale
Effectue une recherche pour toutes les annonces et génère un rapport CSV.

**Paramètres :**
- `method` (optionnel, défaut="hybrid") : Algorithme à utiliser

```bash
curl -X POST "http://localhost:8000/search-all?method=bfs"
```

**Réponse :**
```json
{
  "message": "Recherche globale terminée",
  "method_used": "bfs",
  "ads_processed": 100,
  "total_nodes_found": 2547,
  "elapsed_time": 15.234,
  "average_time_per_ad": 0.152,
  "csv_file": "search_all_results_bfs.csv",
  "csv_path": "/full/path/to/search_all_results_bfs.csv"
}
```

**Format du CSV généré :**
```csv
ad_id,distance_D,nombre_nodes,liste_nodes
A1,15.789,3,N1:12.345;N2:14.678;N3:15.123
A2,23.456,5,N4:18.901;N5:20.234;N6:21.567;N7:22.890;N8:23.123
```

## ⚡ Algorithmes et Performance

### Distance pondérée
La formule de distance utilisée est :
```
d_Y(A, B) = √(Σ y_k × (f_Ak - f_Bk)²)
```

**Où :**
- `Y` : Coefficient de pondération de l'annonce
- `f_Ak`, `f_Bk` : Valeurs des features k pour les points A et B
- `k` : Indice des 50 features (0 à 49)

### Comparaison des algorithmes

| Algorithme | Complexité | Mémoire | Cas optimal | Précision |
|------------|------------|---------|-------------|-----------|
| **Naive** | O(N) | O(1) | Petits graphes (< 1000) | 100% |
| **BFS** | O(E) | O(V) | Recherches locales | 85-95% |
| **Dijkstra** | O(E log V) | O(V) | Graphes moyens | 90-98% |
| **Hybrid** | Adaptatif | Adaptatif | Usage général | 90-99% |

### Stratégie Hybrid (recommandée)
L'algorithme hybrid sélectionne automatiquement la meilleure méthode :

```python
# Logique de sélection
if num_nodes < 1000:
    return naive_search()
elif num_nodes < 3000:
    return bfs_search()
else:
    return dijkstra_search()
```

### Construction K-NN
- **Principe** : Chaque nœud est connecté à ses K plus proches voisins
- **Métrique** : Distance euclidienne dans l'espace des 50 features
- **Paramètre K** : Compromis entre densité du graphe et performance
  - K faible (5-8) : Graphe épars, recherche rapide mais moins précise
  - K élevé (15-25) : Graphe dense, recherche plus lente mais plus complète

## 🧪 Tests et Génération de Données

### Génération de données de test
```bash
# Générer des jeux de données synthétiques
python generate_data.py
```

**Fichiers générés :**
- `adsSim_data_nodes_generated.csv` : 1000 nœuds avec features aléatoires
- `queries_structured_generated.csv` : 100 annonces avec rayons variables

### Workflow de test complet
```bash
# 1. Générer les données
python generate_data.py

# 2. Lancer le serveur (terminal 1)
python main.py

# 3. Dans un nouveau terminal : tests
# Upload des données
curl -X POST "http://localhost:8000/upload-files" \
  -F "nodes_file=@adsSim_data_nodes_generated.csv" \
  -F "ads_file=@queries_structured_generated.csv"

# Construction du graphe
curl -X POST "http://localhost:8000/build-graph?k=10"

# Vérification des statistiques
curl -X GET "http://localhost:8000/stats"

# Test de recherche simple
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"ad_id": "A1", "method": "hybrid"}'

# Benchmark complet (génère 4 fichiers CSV)
curl -X POST "http://localhost:8000/search-all?method=naive"
curl -X POST "http://localhost:8000/search-all?method=bfs"  
curl -X POST "http://localhost:8000/search-all?method=dijkstra"
curl -X POST "http://localhost:8000/search-all?method=hybrid"
```

### Analyse des résultats
Les fichiers `search_all_results_{method}.csv` permettent de :
- **Comparer les performances** entre algorithmes
- **Analyser la distribution** des résultats par annonce
- **Identifier les cas problématiques** (trop/pas assez de résultats)
- **Optimiser les paramètres** K et rayons D

## 🐛 Résolution de Problèmes

### Erreurs courantes et solutions

#### 🚫 "Aucun graphe chargé"
**Cause :** Tentative de recherche avant construction du graphe
```bash
# Solution : respecter l'ordre
curl -X POST "http://localhost:8000/upload-files" -F "nodes_file=@..." -F "ads_file=@..."
curl -X POST "http://localhost:8000/build-graph"
curl -X POST "http://localhost:8000/search" -d '{"ad_id": "A1", "method": "hybrid"}'
```

#### 📊 "Erreur de format CSV - Nodes"
**Causes possibles :**
- Nombre incorrect de colonnes (doit être exactement 51)
- Features non numériques
- Valeurs manquantes (NaN)

**Vérification :**
```python
import pandas as pd
df = pd.read_csv('adsSim_data_nodes.csv')
print(f"Colonnes: {df.shape[1]} (doit être 51)")
print(f"Types: {df.dtypes}")
print(f"NaN: {df.isnull().sum().sum()}")
```

#### 📈 "Erreur de format CSV - Ads"  
**Causes possibles :**
- Nombre incorrect de colonnes (doit être exactement 4)
- point_A sans exactement 50 valeurs séparées par `;`
- Y_vector ou D non numériques

**Validation :**
```python
df = pd.read_csv('queries_structured.csv')
# Vérifier point_A
first_point = df.iloc[0]['point_A']
coords = first_point.split(';')
print(f"Coordonnées dans point_A: {len(coords)} (doit être 50)")
```

#### 🔍 "Ad {ad_id} introuvable"
**Cause :** Utilisation d'un ID inexistant
```bash
# Lister les IDs disponibles
curl -X GET "http://localhost:8000/stats" | grep -o '"ad_ids":\[[^]]*\]'
```

#### ⚡ Performance lente
**Solutions selon le contexte :**
- **K trop élevé** : Réduire à 8-12 pour de gros graphes
- **Méthode inadaptée** : Utiliser `bfs` pour recherches locales
- **Mémoire insuffisante** : Limiter à 5000 nœuds sur 8GB RAM

### Logs et debugging
Le serveur affiche des logs détaillés :
```
🔍 RECHERCHE DANS LE RAYON D
============================================================
Ad: A1
Rayon D: 15.789
Méthode: hybrid
   → Stratégie choisie: BFS (graphe moyen)
    Nœuds vérifiés: 234
✅ 15 nœuds trouvés en 0.045s
============================================================
```

**Niveaux de logs :**
- 🔍 **INFO** : Opérations normales
- ⚠️ **WARNING** : Problèmes non bloquants
- ❌ **ERROR** : Erreurs nécessitant une action

## 📚 Architecture et Technologies

### Stack technique
- **[FastAPI](https://fastapi.tiangolo.com/)** : Framework web moderne et performant
- **[NetworkX](https://networkx.org/)** : Manipulation et analyse de graphes
- **[Scikit-learn](https://scikit-learn.org/)** : Algorithmes K-NN et machine learning  
- **[Pandas](https://pandas.pydata.org/)** : Traitement efficace des données tabulaires
- **[NumPy](https://numpy.org/)** : Calculs vectoriels haute performance

### Patterns de conception
- **Singleton** : GraphManager pour instance unique du graphe
- **Strategy** : Implémentation modulaire des algorithmes de recherche
- **Factory** : Sélection dynamique des méthodes selon le contexte
- **Observer** : Logs et métriques pour monitoring

### Optimisations techniques
- **Cache mémoire** : Le graphe persiste entre les requêtes
- **Structures optimisées** : Dictionnaires et sets pour lookups O(1)
- **Calculs vectorisés** : NumPy pour les opérations sur les features
- **Async I/O** : FastAPI pour la gestion concurrentielle des requêtes

## 🔗 Intégration et Extensions

### Frontend React (optionnel)
Une interface graphique est disponible dans `/js_python_version/frontend` :
- **Visualisation 3D** du graphe avec Force-Directed Layout
- **Interface de recherche** interactive
- **Métriques en temps réel** et monitoring
- **Upload de fichiers** par glisser-déposer

### API clients
```python
# Client Python exemple
import requests
import json

class GraphAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def search(self, ad_id, method="hybrid"):
        response = requests.post(
            f"{self.base_url}/search",
            json={"ad_id": ad_id, "method": method}
        )
        return response.json()
    
    def get_stats(self):
        return requests.get(f"{self.base_url}/stats").json()

# Usage
client = GraphAPIClient()
results = client.search("A1", "hybrid")
```

### Extensions possibles
- **Base de données** : PostgreSQL avec PostGIS pour persistance
- **Cache distribué** : Redis pour graphes partagés
- **Streaming** : Apache Kafka pour données temps réel
- **Monitoring** : Prometheus + Grafana pour métriques avancées
- **Authentification** : JWT pour sécurisation des endpoints

## 📈 Monitoring et Métriques

### Métriques de performance collectées
- **Temps de construction** du graphe
- **Temps de recherche** par algorithme
- **Nombre de nœuds vérifiés** (efficacité)
- **Utilisation mémoire** par opération
- **Taux de cache hit/miss**

### Endpoints de monitoring
```bash
# Santé du service
curl -X GET "http://localhost:8000/health"

# Métriques détaillées
curl -X GET "http://localhost:8000/metrics"

# Usage mémoire
curl -X GET "http://localhost:8000/memory-usage"
```

### Alertes recommandées
- **Temps de réponse > 5s** pour les recherches
- **Utilisation mémoire > 80%** du disponible
- **Erreur rate > 5%** sur 10 minutes
- **Graphe non chargé** depuis plus de 1h

## 📜 Licence et Contribution

### Informations projet
- **Institution** : ESME Sudria
- **Cours** : Advanced Python & Algorithms (A3MSI)
- **Année** : 2024-2025
- **Type** : Projet académique de recherche

### Contributeurs
- **Développement principal** : Architecture API et algorithmes
- **Optimisations** : Performance et structures de données
- **Documentation** : README et spécifications techniques
- **Tests** : Validation et benchmarking

### Roadmap future
- [ ] **Algorithmes avancés** : A*, recherche approximative (LSH)
- [ ] **Graphes dynamiques** : Mise à jour incrémentale
- [ ] **Parallélisation** : Multi-threading pour gros volumes
- [ ] **GPU computing** : CUDA pour calculs vectoriels
- [ ] **Graph Neural Networks** : ML avancé pour prédictions

---

## 🎯 Démarrage Rapide - Résumé

```bash
# 1. Installation
cd api_version && pip install -r requirements.txt

# 2. Génération de données de test  
python generate_data.py

# 3. Lancement du serveur
python main.py

# 4. Test complet (nouveau terminal)
curl -X POST "http://localhost:8000/upload-files" \
  -F "nodes_file=@adsSim_data_nodes_generated.csv" \
  -F "ads_file=@queries_structured_generated.csv"

curl -X POST "http://localhost:8000/build-graph?k=10"

curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"ad_id": "A1", "method": "hybrid"}'
```

**🌐 Interface web :** http://localhost:8000/docs  
**📊 Documentation :** Swagger UI intégrée  
**🔍 Tests interactifs :** Interface FastAPI native

Pour toute question technique, consulter les logs du serveur ou la documentation Swagger intégrée.