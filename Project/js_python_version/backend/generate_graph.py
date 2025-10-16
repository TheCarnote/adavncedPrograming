import pandas as pd
import numpy as np
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import time
import os
import pickle
import heapq

# ==================== ÉTAPE 1 : CHARGEMENT DES DONNÉES ====================

def load_data():
    """
    Charge les données des nœuds réguliers et des ads
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    nodes_path = os.path.join(script_dir, 'adsSim_data_nodes.csv')
    ads_path = os.path.join(script_dir, 'queries_structured.csv')
    
    if not os.path.exists(nodes_path):
        raise FileNotFoundError(f"Fichier introuvable: {nodes_path}")
    if not os.path.exists(ads_path):
        raise FileNotFoundError(f"Fichier introuvable: {ads_path}")
    
    nodes_df = pd.read_csv(nodes_path)
    ads_df = pd.read_csv(ads_path)
    
    print(f" Chargement terminé:")
    print(f"   - {len(nodes_df)} nœuds réguliers chargés")
    print(f"   - {len(ads_df)} ads chargés")
    
    return nodes_df, ads_df

# ==================== ÉTAPE 2 : CONSTRUCTION DU GRAPHE ====================

def compute_weighted_distance(features_A, features_B, Y_vector):
    """
    Calcule la distance pondérée entre deux nœuds:
    d_Y(A, B) = √(Σ y_k × (f_Ak - f_Bk)²)
    """
    diff = features_A - features_B
    weighted_squared_diff = Y_vector * (diff ** 2)
    return np.sqrt(np.sum(weighted_squared_diff))

def add_regular_nodes_with_knn(G, nodes_df, k=10):
    """
    Ajoute les nœuds réguliers au graphe et les connecte par K-NN
    (distance euclidienne simple sur les 50 features)
    """
    print(f"\n🔨 Ajout des nœuds réguliers avec K-NN (k={k})...")
    
    # Extraire les features
    feature_cols = [col for col in nodes_df.columns if col.startswith('feature')]
    X = nodes_df[feature_cols].values
    
    # 🔥 CORRECTION : Convertir en float et gérer les NaN
    try:
        X = X.astype(float)  # Forcer la conversion en float
        X = np.nan_to_num(X, nan=0.0)  # Remplacer NaN par 0.0
    except ValueError as e:
        print(f"❌ Erreur de conversion des features : {e}")
        print("   Vérifiez que les colonnes 'feature_*' contiennent uniquement des nombres.")
        raise
    
    node_ids = nodes_df['node_id'].values
    
    # Ajouter tous les nœuds réguliers avec leurs features
    for i, node_id in enumerate(node_ids):
        G.add_node(node_id, 
                   node_type='regular',
                   features=X[i])
    
    # K-NN pour connecter les nœuds réguliers
    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='ball_tree', metric='euclidean')
    nbrs.fit(X)
    distances, indices = nbrs.kneighbors(X)
    
    # Ajouter les arêtes (type 1: node ↔ node)
    edge_count = 0
    for i in range(len(node_ids)):
        for j in range(1, k+1):  # Ignorer le premier (lui-même)
            neighbor_idx = indices[i][j]
            distance = distances[i][j]
            
            G.add_edge(node_ids[i], node_ids[neighbor_idx], 
                      edge_type='node_node',
                      weight=distance)
            edge_count += 1
    
    print(f" Nœuds réguliers ajoutés:")
    print(f"   - {len(node_ids)} nœuds")
    print(f"   - {edge_count} arêtes (K-NN, distance euclidienne)")
    
    return G

def build_graph(nodes_df, k=10):
    """
    Construit le graphe complet avec seulement les nodes réguliers et K-NN.
    """
    print(f"\n🔨 Construction du graphe (K={k})...")
    
    G = nx.Graph()
    
    # Ajouter les nodes réguliers avec K-NN
    G = add_regular_nodes_with_knn(G, nodes_df, k=k)
    
    print(f"\n✅ Graphe construit : {G.number_of_nodes()} nodes, {G.number_of_edges()} arêtes")
    
    return G

# ==================== SAUVEGARDE DU GRAPHE ====================

def save_graph(G, script_dir):
    """
    Sauvegarde le graphe en pickle (format complet avec features)
    """
    print(f"\n Sauvegarde du graphe...")
    
    pickle_path = os.path.join(script_dir, "advertising_graph.pkl")
    with open(pickle_path, 'wb') as f:
        pickle.dump(G, f)
    
    print(f"    Graphe sauvegardé: {pickle_path}")
    
    return pickle_path

def load_graph(pickle_path):
    """
    Charge le graphe depuis le fichier pickle
    """
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)
    return G

# ==================== NOUVELLES FONCTIONS DE RECHERCHE ====================

def search_naive(G, start_node_id, Y_vector, radius_X):
    """
    STRATÉGIE NAÏVE: Parcours exhaustif de tous les nœuds réguliers depuis start_node_id.
    Complexité: O(N) où N = nombre de nœuds réguliers.
    """
    start_features = np.array(G.nodes[start_node_id]['features'])
    
    nodes_found = []
    nodes_checked = 0
    
    # Parcourir TOUS les nœuds réguliers
    for node_id, node_data in G.nodes(data=True):
        if node_data.get('node_type') != 'regular':
            continue
        
        nodes_checked += 1
        node_features = np.array(node_data['features'])
        distance = compute_weighted_distance(start_features, node_features, Y_vector)
        
        if distance <= radius_X:
            nodes_found.append((node_id, distance))
    
    # Trier par distance croissante
    nodes_found.sort(key=lambda x: x[1])
    
    print(f"    Nœuds vérifiés: {nodes_checked}")
    
    return nodes_found

def search_bfs(G, start_node_id, Y_vector, radius_X):
    """
    STRATÉGIE BFS: Parcours par arêtes du graphe depuis start_node_id.
    Complexité: O(E) où E = nombre d'arêtes explorées.
    """
    start_features = np.array(G.nodes[start_node_id]['features'])
    
    nodes_found = []
    visited = set()
    queue = [start_node_id]
    visited.add(start_node_id)
    nodes_checked = 0
    
    while queue:
        current = queue.pop(0)
        
        # Explorer les voisins
        for neighbor in G.neighbors(current):
            if neighbor in visited:
                continue
            
            visited.add(neighbor)
            
            # Vérifier si c'est un nœud régulier
            if G.nodes[neighbor].get('node_type') != 'regular':
                continue
            
            nodes_checked += 1
            # Calculer la distance pondérée DIRECTE depuis start_node_id
            neighbor_features = np.array(G.nodes[neighbor]['features'])
            distance = compute_weighted_distance(start_features, neighbor_features, Y_vector)
            
            if distance <= radius_X:
                nodes_found.append((neighbor, distance))
                # Continuer l'exploration depuis ce nœud
                queue.append(neighbor)
    
    # Trier par distance croissante
    nodes_found.sort(key=lambda x: x[1])
    
    print(f"    Nœuds vérifiés: {nodes_checked}")
    
    return nodes_found

def search_dijkstra(G, start_node_id, Y_vector, radius_X):
    """
    STRATÉGIE DIJKSTRA: Parcours optimisé avec file de priorité depuis start_node_id.
    Complexité: O(E log V) où E = arêtes explorées, V = nœuds visités.
    """
    start_features = np.array(G.nodes[start_node_id]['features'])
    
    nodes_found = []
    visited = set()
    # File de priorité: (distance_directe, node_id)
    heap = [(0, start_node_id)]
    nodes_checked = 0
    
    while heap:
        current_dist, current = heapq.heappop(heap)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Explorer les voisins
        for neighbor in G.neighbors(current):
            if neighbor in visited:
                continue
            
            # Vérifier si c'est un nœud régulier
            if G.nodes[neighbor].get('node_type') != 'regular':
                continue
            
            nodes_checked += 1
            # Calculer la distance pondérée DIRECTE depuis start_node_id
            neighbor_features = np.array(G.nodes[neighbor]['features'])
            distance = compute_weighted_distance(start_features, neighbor_features, Y_vector)
            
            if distance <= radius_X:
                nodes_found.append((neighbor, distance))
                # Ajouter à la heap avec sa distance directe (priorité)
                heapq.heappush(heap, (distance, neighbor))
    
    # Trier par distance croissante
    nodes_found.sort(key=lambda x: x[1])
    
    print(f"    Nœuds vérifiés: {nodes_checked}")
    
    return nodes_found

def search_hybrid(G, start_node_id, Y_vector, radius_X):
    """
    STRATÉGIE HYBRIDE: Choisit automatiquement la meilleure stratégie.
    Logique basée sur la taille du graphe.
    """
    num_nodes = G.number_of_nodes()
    
    if num_nodes < 1000:
        print(f"    Stratégie choisie: NAÏVE (graphe petit)")
        return search_naive(G, start_node_id, Y_vector, radius_X)
    elif num_nodes < 3000:
        print(f"    Stratégie choisie: BFS (graphe moyen)")
        return search_bfs(G, start_node_id, Y_vector, radius_X)
    else:
        print(f"    Stratégie choisie: DIJKSTRA (graphe grand)")
        return search_dijkstra(G, start_node_id, Y_vector, radius_X)