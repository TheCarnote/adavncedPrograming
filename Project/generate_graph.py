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
    
    print(f"✅ Chargement terminé:")
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
    
    print(f"✅ Nœuds réguliers ajoutés:")
    print(f"   - {len(node_ids)} nœuds")
    print(f"   - {edge_count} arêtes (K-NN, distance euclidienne)")
    
    return G


def add_ads_with_weighted_connections(G, ads_df, nodes_df):
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
    total_connections = 0
    
    for idx, row in ads_df.iterrows():
        ad_id = row['point_A']
        Y_vector_str = row['Y_vector']
        radius_D = row['D']
        
        # Parser le vecteur Y
        Y_vector = np.array([float(x) for x in Y_vector_str.split(';')])
        
        # Récupérer les features de l'ad (basé sur le node correspondant)
        node_number = ad_id.split('_')[1]
        node_idx = int(node_number) - 1  # node_1 -> index 0
        
        if node_idx >= len(nodes_features):
            print(f"⚠️  Warning: Ad {ad_id} hors limites, ignoré")
            continue
        
        ad_features = nodes_features[node_idx]
        
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
        
        total_connections += connections_count
        
        # Afficher les 5 premiers ads
        if idx < 5:
            print(f"   {ad_id}: {connections_count} connexions (D={radius_D:.2f})")
    
    print(f"✅ Ads ajoutés:")
    print(f"   - {total_ads} ads")
    print(f"   - {total_connections} arêtes (distance pondérée d_Y ≤ D)")
    print(f"   - Moyenne: {total_connections/total_ads:.1f} connexions par ad")
    
    return G


def build_graph(nodes_df, ads_df, k=10):
    """
    Construit le graphe complet:
    1. Nodes réguliers connectés par K-NN
    2. Ads connectés aux nodes par distance pondérée
    """
    print("="*80)
    print("🔨 CONSTRUCTION DU GRAPHE")
    print("="*80)
    
    G = nx.Graph()
    
    # 1. Ajouter les nœuds réguliers + connexions K-NN
    G = add_regular_nodes_with_knn(G, nodes_df, k)
    
    # 2. Ajouter les ads + connexions pondérées
    G = add_ads_with_weighted_connections(G, ads_df, nodes_df)
    
    # Statistiques globales
    print(f"\n📊 STATISTIQUES DU GRAPHE:")
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
    print(f"\n💾 Sauvegarde du graphe...")
    
    pickle_path = os.path.join(script_dir, "advertising_graph.pkl")
    with open(pickle_path, 'wb') as f:
        pickle.dump(G, f)
    
    print(f"   ✅ Graphe sauvegardé: {pickle_path}")
    
    return pickle_path


def load_graph(pickle_path):
    """
    Charge le graphe depuis le fichier pickle
    """
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)
    return G


# ==================== ÉTAPE 3 : RECHERCHE DANS LE RAYON X ====================

def search_naive(G, ad_id, X):
    """
    STRATÉGIE NAÏVE: Parcours exhaustif de tous les nœuds réguliers
    Complexité: O(N) où N = nombre de nœuds réguliers
    
    ✅ Avantages: Toujours complet, trouve tous les nœuds
    ❌ Inconvénients: Lent, n'utilise pas la structure du graphe
    """
    if ad_id not in G:
        print(f"❌ Ad {ad_id} introuvable dans le graphe")
        return []
    
    ad_data = G.nodes[ad_id]
    ad_features = ad_data['features']
    Y_vector = ad_data['Y_vector']
    
    nodes_found = []
    nodes_checked = 0
    
    # Parcourir TOUS les nœuds réguliers
    for node_id, node_data in G.nodes(data=True):
        if node_data.get('node_type') != 'regular':
            continue
        
        nodes_checked += 1
        node_features = node_data['features']
        distance = compute_weighted_distance(ad_features, node_features, Y_vector)
        
        if distance <= X:
            nodes_found.append((node_id, distance))
    
    # Trier par distance croissante
    nodes_found.sort(key=lambda x: x[1])
    
    print(f"   📊 Nœuds vérifiés: {nodes_checked}")
    
    return nodes_found


def search_bfs(G, ad_id, X):
    """
    STRATÉGIE BFS: Parcours par arêtes du graphe
    Complexité: O(E) où E = nombre d'arêtes explorées
    
    ✅ Avantages: Plus rapide si X ≈ D, utilise la structure du graphe
    ❌ Inconvénients: Peut manquer des nœuds si X >> D
    """
    if ad_id not in G:
        print(f"❌ Ad {ad_id} introuvable dans le graphe")
        return []
    
    ad_data = G.nodes[ad_id]
    ad_features = ad_data['features']
    Y_vector = ad_data['Y_vector']
    
    nodes_found = []
    visited = set()
    queue = [ad_id]
    visited.add(ad_id)
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
            # Calculer la distance pondérée DIRECTE (pas par le graphe)
            neighbor_features = G.nodes[neighbor]['features']
            distance = compute_weighted_distance(ad_features, neighbor_features, Y_vector)
            
            if distance <= X:
                nodes_found.append((neighbor, distance))
                # Continuer l'exploration depuis ce nœud
                queue.append(neighbor)
    
    # Trier par distance croissante
    nodes_found.sort(key=lambda x: x[1])
    
    print(f"   📊 Nœuds vérifiés: {nodes_checked}")
    
    return nodes_found


def search_dijkstra(G, ad_id, X):
    """
    STRATÉGIE DIJKSTRA MODIFIÉE: Parcours optimisé avec file de priorité
    Utilise une heap pour explorer d'abord les nœuds les plus proches
    
    ✅ Avantages: Plus efficace que BFS, explore d'abord les nœuds prometteurs
    ❌ Inconvénients: Toujours limité par la structure du graphe
    
    Complexité: O(E log V) où E = arêtes explorées, V = nœuds visités
    """
    if ad_id not in G:
        print(f"❌ Ad {ad_id} introuvable dans le graphe")
        return []
    
    ad_data = G.nodes[ad_id]
    ad_features = ad_data['features']
    Y_vector = ad_data['Y_vector']
    
    nodes_found = []
    visited = set()
    # File de priorité: (distance_directe, node_id)
    heap = [(0, ad_id)]
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
            # Calculer la distance pondérée DIRECTE depuis l'ad
            neighbor_features = G.nodes[neighbor]['features']
            distance = compute_weighted_distance(ad_features, neighbor_features, Y_vector)
            
            if distance <= X:
                nodes_found.append((neighbor, distance))
                # Ajouter à la heap avec sa distance directe (priorité)
                heapq.heappush(heap, (distance, neighbor))
    
    # Trier par distance croissante
    nodes_found.sort(key=lambda x: x[1])
    
    print(f"   📊 Nœuds vérifiés: {nodes_checked}")
    
    return nodes_found


def search_hybrid(G, ad_id, X):
    """
    STRATÉGIE HYBRIDE OPTIMISÉE: Choisit automatiquement la meilleure stratégie
    
    Logique:
    - Si X ≤ D * 0.8  → Dijkstra (explore zone restreinte efficacement)
    - Si D * 0.8 < X ≤ D * 1.5 → BFS (bon compromis)
    - Si X > D * 1.5  → Naïve (doit explorer largement de toute façon)
    
    ✅ Avantages: Combine les avantages de toutes les stratégies
    """
    if ad_id not in G:
        print(f"❌ Ad {ad_id} introuvable dans le graphe")
        return []
    
    ad_data = G.nodes[ad_id]
    radius_D = ad_data['radius_D']
    
    # Choisir la stratégie selon le ratio X/D
    ratio = X / radius_D
    
    if ratio <= 0.8:
        print(f"   🎯 Stratégie choisie: DIJKSTRA (X ≤ 0.8*D, recherche locale)")
        return search_dijkstra(G, ad_id, X)
    elif ratio <= 1.5:
        print(f"   🎯 Stratégie choisie: BFS (0.8*D < X ≤ 1.5*D, zone modérée)")
        return search_bfs(G, ad_id, X)
    else:
        print(f"   🎯 Stratégie choisie: NAÏVE (X > 1.5*D, recherche large)")
        return search_naive(G, ad_id, X)


def search_in_radius_X(G, ad_id, X, strategy='hybrid'):
    """
    Recherche tous les nœuds réguliers à distance pondérée ≤ X d'un ad
    
    Parameters:
    - ad_id: identifiant de l'ad (ex: 'ads_1')
    - X: rayon de recherche
    - strategy: 'naive', 'bfs', 'dijkstra', ou 'hybrid' (recommandé)
    
    Returns:
    - Liste de tuples (node_id, distance) triée par distance
    - Durée de l'exécution
    """
    start_time = time.time()
    
    if strategy == 'naive':
        nodes_found = search_naive(G, ad_id, X)
    elif strategy == 'bfs':
        nodes_found = search_bfs(G, ad_id, X)
    elif strategy == 'dijkstra':
        nodes_found = search_dijkstra(G, ad_id, X)
    elif strategy == 'hybrid':
        nodes_found = search_hybrid(G, ad_id, X)
    else:
        raise ValueError(f"Stratégie inconnue: {strategy}. Utilisez 'naive', 'bfs', 'dijkstra' ou 'hybrid'")
    
    duration = time.time() - start_time
    
    return nodes_found, duration


# ==================== INTERFACE INTERACTIVE ====================

def select_heuristics():
    """
    Permet à l'utilisateur de sélectionner les heuristiques à tester
    """
    print("\n" + "="*80)
    print("🎯 SÉLECTION DES HEURISTIQUES À TESTER")
    print("="*80)
    
    available_heuristics = {
        '1': ('naive', 'Naïve - Parcours exhaustif (O(N))'),
        '2': ('bfs', 'BFS - Parcours par arêtes (O(E))'),
        '3': ('dijkstra', 'Dijkstra - File de priorité (O(E log V))'),
        '4': ('hybrid', 'Hybride - Choix automatique')
    }
    
    print("\n📋 Heuristiques disponibles:")
    for key, (name, description) in available_heuristics.items():
        print(f"   {key}. {description}")
    
    print("\n💡 Vous pouvez sélectionner plusieurs heuristiques (ex: 1,2,4)")
    print("   Ou appuyez sur Entrée pour tester TOUTES les heuristiques")
    
    selection = input("\n🔍 Votre sélection: ").strip()
    
    if not selection:
        # Tester toutes les heuristiques
        selected = list(available_heuristics.keys())
        print(f"\n✅ Toutes les heuristiques seront testées")
    else:
        # Parser la sélection
        selected = [s.strip() for s in selection.split(',')]
        # Valider
        selected = [s for s in selected if s in available_heuristics]
        
        if not selected:
            print("⚠️  Sélection invalide, toutes les heuristiques seront testées")
            selected = list(available_heuristics.keys())
    
    # Convertir en noms d'heuristiques
    selected_heuristics = [(available_heuristics[s][0], available_heuristics[s][1]) 
                           for s in selected]
    
    print(f"\n✅ Heuristiques sélectionnées:")
    for name, description in selected_heuristics:
        print(f"   • {description}")
    
    return selected_heuristics


def interactive_search(G):
    """
    Interface interactive pour rechercher des nœuds dans un rayon X
    """
    print("\n" + "="*80)
    print("🔍 RECHERCHE INTERACTIVE DANS LE RAYON X")
    print("="*80)
    
    # Lister les ads disponibles
    ad_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'ad']
    
    print(f"\n📋 {len(ad_nodes)} ads disponibles dans le graphe")
    print(f"   Exemples: {', '.join(ad_nodes[:5])}")
    
    # Sélectionner les heuristiques à tester
    selected_heuristics = select_heuristics()
    
    while True:
        print("\n" + "-"*80)
        
        # Demander l'ad
        ad_id = input("🎯 Entrez l'ID de l'ad (ex: ads_1) ou 'q' pour quitter: ").strip()
        
        if ad_id.lower() == 'q':
            print("👋 Au revoir!")
            break
        
        if ad_id not in G:
            print(f"❌ Ad '{ad_id}' introuvable. Réessayez.")
            continue
        
        # Afficher les infos de l'ad
        ad_data = G.nodes[ad_id]
        print(f"\n📊 Informations sur {ad_id}:")
        print(f"   - Rayon D (construction): {ad_data['radius_D']:.2f}")
        print(f"   - Connexions directes: {G.degree(ad_id)}")
        
        # Demander le rayon X
        try:
            X = float(input("📏 Entrez le rayon de recherche X: ").strip())
        except ValueError:
            print("❌ Rayon invalide. Réessayez.")
            continue
        
        # Tester toutes les heuristiques sélectionnées
        print(f"\n🔍 Test des {len(selected_heuristics)} heuristique(s) sélectionnée(s)...")
        print("="*80)
        
        results = []
        
        for strategy_name, strategy_description in selected_heuristics:
            print(f"\n📍 Test de: {strategy_description}")
            print("-"*80)
            
            nodes_found, duration = search_in_radius_X(G, ad_id, X, strategy_name)
            
            results.append({
                'name': strategy_name,
                'description': strategy_description,
                'nodes_found': len(nodes_found),
                'duration_ms': duration * 1000,
                'nodes': nodes_found
            })
            
            print(f"   ✅ Nœuds trouvés: {len(nodes_found)}")
            print(f"   ⏱️  Temps: {duration*1000:.2f} ms")
        
        # Afficher le résumé comparatif
        print("\n" + "="*80)
        print("📊 RÉSUMÉ COMPARATIF")
        print("="*80)
        print(f"{'Heuristique':<30} {'Nœuds trouvés':<15} {'Temps (ms)':<15}")
        print("-"*80)
        
        for result in results:
            print(f"{result['description']:<30} {result['nodes_found']:<15} {result['duration_ms']:<15.2f}")
        
        print("-"*80)
        print(f"Ratio X/D: {X/ad_data['radius_D']:.2f}")
        
        # Afficher le top 10 du meilleur résultat (celui avec le plus de nœuds)
        best_result = max(results, key=lambda x: x['nodes_found'])
        
        if best_result['nodes_found'] > 0:
            print(f"\n🏆 Meilleure heuristique: {best_result['description']}")
            print(f"   Top 10 nœuds les plus proches:")
            for i, (node_id, dist) in enumerate(best_result['nodes'][:10], 1):
                print(f"      {i:2d}. {node_id:15s} - Distance: {dist:.4f}")
        else:
            print("\n   ⚠️  Aucune heuristique n'a trouvé de nœud dans ce rayon.")


# ==================== FONCTION PRINCIPALE ====================

def main():
    """
    Fonction principale
    """
    print("="*80)
    print("🚀 PROJET: GRAPHE PUBLICITAIRE PONDÉRÉ")
    print("="*80)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Charger les données
    nodes_df, ads_df = load_data()
    
    # 2. Construire le graphe
    G = build_graph(nodes_df, ads_df, k=10)
    
    # 3. Sauvegarder le graphe
    pickle_path = save_graph(G, script_dir)
    
    # 4. Recherche interactive
    interactive_search(G)
    
    print("\n" + "="*80)
    print("✅ PROGRAMME TERMINÉ")
    print("="*80)


if __name__ == "__main__":
    main()