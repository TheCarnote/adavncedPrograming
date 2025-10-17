import pandas as pd
import numpy as np
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import time
import os
import pickle
import heapq
from typing import List, Tuple

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
    # print(weighted_squared_diff)
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


def add_ads(G, ads_df, nodes_df):
    """
    Ajoute les ads au graphe et les connecte aux nœuds réguliers
    selon la distance pondérée d_Y ≤ D
    """
    print(f"\n🔨 Ajout des ads avec connexions pondérées...")
    
    # Extraire les features des nœuds réguliers
    feature_cols = [col for col in nodes_df.columns if col.startswith('feature')]
    nodes_features = nodes_df[feature_cols].values
    node_ids = nodes_df['node_id'].values
    
    total_ads = 0
    # total_connections = 0
    
    for idx, row in ads_df.iterrows():
        ad_id = row['point_A']
        A_vector_str = row['A_vector']
        Y_vector_str = row['Y_vector']
        radius_D = row['D']
        
        # Parser le vecteur Y
        Y_vector = np.array([float(x) for x in Y_vector_str.split(';')])
        
        
        # Récupérer les features de l'ad (basé sur le node correspondant)
        # node_number = ad_id.split('_')[1]
        # node_idx = int(node_number) - 1  # node_1 -> index 0
        
        # if node_idx >= len(nodes_features):
        #     print(f"  Warning: Ad {ad_id} hors limites, ignoré")
        #     continue
        
        ad_features = np.array([float(x) for x in A_vector_str.split(';')])
        
        # Ajouter l'ad au graphe
        G.add_node(ad_id,
                   node_type='ad',
                   features=ad_features,
                   Y_vector=Y_vector,
                   radius_D=radius_D)
        
        total_ads += 1
        connections_count = 0
        
        # Connecter l'ad aux nœuds réguliers si d_Y ≤ D
        for i, node_id in enumerate(node_ids):
            node_features = nodes_features[i]
            
            # Calculer la distance pondérée
            distance = compute_weighted_distance(ad_features, node_features, Y_vector)
            
            if distance <= radius_D:
                G.add_edge(ad_id, node_id,
                          edge_type='ad_node',
                          weight=distance)
                connections_count += 1
        
        # total_connections += connections_count
        
        # # Afficher les 5 premiers ads
        # if idx < 5:
        #     print(f"   {ad_id}: {connections_count} connexions (D={radius_D:.2f})")
    
    print(f" Ads ajoutés:")
    print(f"   - {total_ads} ads")
    # print(f"   - {total_connections} arêtes (distance pondérée d_Y ≤ D)")
    # print(f"   - Moyenne: {total_connections/total_ads:.1f} connexions par ad")
    
    return G


def build_graph(nodes_df, ads_df, k=10):
    """
    Construit le graphe complet:
    1. Nodes réguliers connectés par K-NN
    2. Ads connectés aux nodes par distance pondérée
    """
    
    print("🔨 CONSTRUCTION DU GRAPHE")
    
    
    G = nx.Graph()
    
    # 1. Ajouter les nœuds réguliers + connexions K-NN
    G = add_regular_nodes_with_knn(G, nodes_df, k)
    
    # 2. Ajouter les ads + connexions pondérées
    G = add_ads(G, ads_df, nodes_df)
    
    # Statistiques globales
    print(f"\n STATISTIQUES DU GRAPHE:")
    print(f"   - Total nœuds: {G.number_of_nodes()}")
    print(f"   - Total arêtes: {G.number_of_edges()}")
    
    regular_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'regular']
    ad_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'ad']
    
    print(f"   - Nœuds réguliers: {len(regular_nodes)}")
    print(f"   - Nœuds ads: {len(ad_nodes)}")
    
    # Vérifier la connectivité
    if nx.is_connected(G):
        print(f"   - Graphe connexe ✓")
    else:
        components = list(nx.connected_components(G))
        print(f"   - {len(components)} composantes connexes")
        print(f"   - Plus grande composante: {len(max(components, key=len))} nœuds")
    
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

    """
    STRATÉGIE HYBRIDE: Choisit automatiquement la meilleure stratégie.
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