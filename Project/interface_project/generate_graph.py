# -*- coding: utf-8 -*-
"""
Module de construction du graphe publicitaire
"""

import pandas as pd
import numpy as np
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import pickle
import os


def load_data():
    """Charge les fichiers CSV"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        nodes_path = os.path.join(script_dir, "adsSim_data_nodes.csv")
        ads_path = os.path.join(script_dir, "queries_structured.csv")
        
        nodes_df = pd.read_csv(nodes_path)
        ads_df = pd.read_csv(ads_path)
        
        print(f"Noeuds: {len(nodes_df)}, colonnes: {nodes_df.columns.tolist()}")
        print(f"Ads: {len(ads_df)}, colonnes: {ads_df.columns.tolist()}")
        
        return nodes_df, ads_df
        
    except Exception as e:
        print(f"Erreur chargement: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def compute_weighted_distance(features_A, features_B, Y_vector):
    """Calcule la distance pondérée: d_Y(A,B) = sqrt(sum(y_k * (f_Ak - f_Bk)^2))"""
    A = np.array(features_A, dtype=np.float64)
    B = np.array(features_B, dtype=np.float64)
    Y = np.array(Y_vector, dtype=np.float64)
    
    diff = A - B
    weighted_squared_diff = Y * (diff ** 2)
    distance = np.sqrt(np.sum(weighted_squared_diff))
    return float(distance)


def add_regular_nodes_with_knn(G, nodes_df, k=10):
    """Ajoute les nœuds réguliers avec K-NN (distance euclidienne simple)"""
    
    # Extraire les colonnes de features
    feature_cols = [col for col in nodes_df.columns if col.startswith('feature')]
    print(f"Features noeuds ({len(feature_cols)}): {feature_cols[:5]}...")
    
    features_matrix = nodes_df[feature_cols].values.astype(np.float64)
    node_ids = nodes_df['node_id'].values
    
    # Ajouter les nœuds
    for i, node_id in enumerate(node_ids):
        G.add_node(
            node_id,
            node_type='regular',
            features=features_matrix[i].tolist()
        )
    
    # K-NN
    k_actual = min(k + 1, len(nodes_df))
    nbrs = NearestNeighbors(n_neighbors=k_actual, algorithm='ball_tree', metric='euclidean')
    nbrs.fit(features_matrix)
    distances, indices = nbrs.kneighbors(features_matrix)
    
    # Ajouter les arêtes
    edge_count = 0
    for i in range(len(node_ids)):
        for j in range(1, k_actual):  # Ignorer le premier (lui-même)
            neighbor_idx = indices[i][j]
            distance = float(distances[i][j])
            
            G.add_edge(node_ids[i], node_ids[neighbor_idx], 
                      edge_type='node_node',
                      weight=distance)
            edge_count += 1
    
    print(f"Noeuds reguliers: {len(node_ids)}, aretes K-NN: {edge_count}")


def add_ads_with_weighted_connections(G, ads_df, nodes_df):
    """Ajoute les ads avec connexions pondérées (distance d_Y ≤ D)"""
    
    # Extraire les features des nœuds
    feature_cols = [col for col in nodes_df.columns if col.startswith('feature')]
    nodes_features = nodes_df[feature_cols].values.astype(np.float64)
    node_ids = nodes_df['node_id'].values
    
    print(f"Ajout des ads avec connexions ponderees...")
    
    total_ads = 0
    total_connections = 0
    
    for idx, row in ads_df.iterrows():
        ad_id = row['point_A']  # Ex: 'ads_1'
        Y_vector_str = row['Y_vector']  # String "0.0014;0.0054;..."
        radius_D = float(row['D'])
        
        # PARSER le vecteur Y depuis la chaîne
        Y_vector = np.array([float(x) for x in Y_vector_str.split(';')], dtype=np.float64)
        
        # Récupérer les features de l'ad (basé sur le node correspondant)
        # Ex: 'ads_1' -> node_1 -> index 0
        node_number = int(ad_id.split('_')[1])
        node_idx = node_number - 1  # node_1 -> index 0
        
        if node_idx >= len(nodes_features):
            print(f"Warning: Ad {ad_id} hors limites, ignore")
            continue
        
        ad_features = nodes_features[node_idx]
        
        # Ajouter l'ad au graphe
        G.add_node(ad_id,
                   node_type='ad',
                   features=ad_features.tolist(),
                   Y=Y_vector.tolist(),
                   radius_D=radius_D)
        
        total_ads += 1
        connections_count = 0
        
        # Connecter aux nœuds où d_Y ≤ D
        for i, node_id in enumerate(node_ids):
            node_features = nodes_features[i]
            
            # Calculer la distance pondérée
            distance = compute_weighted_distance(ad_features, node_features, Y_vector)
            
            if distance <= radius_D:
                G.add_edge(ad_id, node_id,
                          edge_type='ad_node',
                          weight=distance)
                connections_count += 1
        
        total_connections += connections_count
        
        # Log pour les 5 premiers
        if idx < 5:
            print(f"  {ad_id}: {connections_count} connexions (D={radius_D:.2f})")
    
    print(f"Ads ajoutes: {total_ads}, connexions: {total_connections}")
    print(f"Moyenne: {total_connections/total_ads:.1f} connexions par ad")


def build_graph(nodes_df, ads_df, k=10):
    """Construit le graphe complet"""
    G = nx.Graph()
    
    print(f"Construction graphe K={k}")
    
    # 1. Nœuds réguliers + K-NN
    add_regular_nodes_with_knn(G, nodes_df, k=k)
    
    # 2. Ads + connexions pondérées
    add_ads_with_weighted_connections(G, ads_df, nodes_df)
    
    print(f"Graphe final: {G.number_of_nodes()} noeuds, {G.number_of_edges()} aretes")
    
    # Stats
    regular_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'regular']
    ad_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'ad']
    
    print(f"  - Noeuds reguliers: {len(regular_nodes)}")
    print(f"  - Noeuds ads: {len(ad_nodes)}")
    
    return G


def save_graph(G, script_dir):
    """Sauvegarde le graphe"""
    output_path = os.path.join(script_dir, "advertising_graph.pkl")
    with open(output_path, 'wb') as f:
        pickle.dump(G, f)
    print(f"Sauvegarde: {output_path}")


def load_graph(pickle_path):
    """Charge un graphe"""
    with open(pickle_path, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    nodes_df, ads_df = load_data()
    if nodes_df is not None:
        graph = build_graph(nodes_df, ads_df, k=10)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_graph(graph, script_dir)
        print("OK!")