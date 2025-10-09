import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import pickle

def load_graph(pickle_path):
    """
    Charge le graphe depuis le fichier pickle
    """
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)
    return G


def compute_weighted_distance(features_A, features_v, Y_vector):
    """
    Calcule la distance pondérée entre deux nœuds:
    d_Y(A, v) = √(Σ y_k × (f_Ak - f_vk)²)
    """
    diff = features_A - features_v
    weighted_squared_diff = Y_vector * (diff ** 2)
    return np.sqrt(np.sum(weighted_squared_diff))


def compute_2d_weighted_distance(features_A_2d, features_v_2d, Y_vector_2d):
    """
    Calcule la distance pondérée entre deux nœuds en utilisant seulement 2 features:
    d_Y(A, v) = √(y_i × (f_Ai - f_vi)² + y_j × (f_Aj - f_vj)²)
    """
    diff = features_A_2d - features_v_2d
    weighted_squared_diff = Y_vector_2d * (diff ** 2)
    return np.sqrt(np.sum(weighted_squared_diff))


def find_nodes_in_radius(G, node_A_id, Y_vector, radius_D):
    """
    Trouve tous les nœuds du graphe dont la distance pondérée 
    au nœud A est ≤ radius_D
    """
    if node_A_id not in G:
        print(f"❌ Le nœud {node_A_id} n'existe pas dans le graphe")
        return []
    
    # Récupérer les features du nœud A
    features_A = G.nodes[node_A_id]['features']
    
    # Calculer les distances pour tous les nœuds
    nodes_in_radius = []
    for node_v_id in G.nodes():
        if node_v_id == node_A_id:
            continue  # Ignorer le nœud lui-même
        
        features_v = G.nodes[node_v_id]['features']
        distance = compute_weighted_distance(features_A, features_v, Y_vector)
        
        if distance <= radius_D:
            nodes_in_radius.append((node_v_id, distance))
    
    # Trier par distance croissante
    nodes_in_radius.sort(key=lambda x: x[1])
    
    return nodes_in_radius


def find_nodes_in_radius_2d(G, node_A_id, feature_1_idx, feature_2_idx, Y_vector_2d, radius_D):
    """
    Trouve tous les nœuds du graphe dont la distance pondérée 2D
    au nœud A est ≤ radius_D (utilise seulement 2 features)
    """
    if node_A_id not in G:
        print(f"❌ Le nœud {node_A_id} n'existe pas dans le graphe")
        return []
    
    # Récupérer les 2 features du nœud A
    features_A = G.nodes[node_A_id]['features']
    features_A_2d = np.array([features_A[feature_1_idx], features_A[feature_2_idx]])
    
    # Calculer les distances pour tous les nœuds
    nodes_in_radius = []
    for node_v_id in G.nodes():
        if node_v_id == node_A_id:
            continue  # Ignorer le nœud lui-même
        
        features_v = G.nodes[node_v_id]['features']
        features_v_2d = np.array([features_v[feature_1_idx], features_v[feature_2_idx]])
        
        distance = compute_2d_weighted_distance(features_A_2d, features_v_2d, Y_vector_2d)
        
        if distance <= radius_D:
            nodes_in_radius.append((node_v_id, distance))
    
    # Trier par distance croissante
    nodes_in_radius.sort(key=lambda x: x[1])
    
    return nodes_in_radius


def visualize_query_2d(G, node_A_id, Y_vector, radius_D, queries_df):
    """
    Visualise une requête en 2D en utilisant les 2 features les plus importantes
    selon le vecteur de pondération Y.
    
    L'ads (node_A) est placé à l'origine, et un cercle en pointillés montre la zone de rayon D.
    La distance est calculée UNIQUEMENT avec ces 2 features.
    """
    print(f"\n🎨 Création de la visualisation 2D pour {node_A_id}...")
    
    # 1. Trouver les 2 features les plus importantes (indices avec les plus grandes valeurs dans Y)
    top_2_indices = np.argsort(Y_vector)[-2:][::-1]  # Les 2 plus grandes valeurs
    feature_1_idx = top_2_indices[0]
    feature_2_idx = top_2_indices[1]
    
    # Créer un vecteur Y 2D avec seulement ces 2 features
    Y_vector_2d = np.array([Y_vector[feature_1_idx], Y_vector[feature_2_idx]])
    
    print(f"   Features sélectionnées: feature_{feature_1_idx+1} (poids: {Y_vector[feature_1_idx]:.4f})")
    print(f"                          feature_{feature_2_idx+1} (poids: {Y_vector[feature_2_idx]:.4f})")
    print(f"   🔍 Calcul des distances avec SEULEMENT ces 2 features")
    
    # 2. Récupérer les features du nœud A (origine)
    features_A = G.nodes[node_A_id]['features']
    origin_x = features_A[feature_1_idx]
    origin_y = features_A[feature_2_idx]
    
    # 3. Trouver les nœuds dans le rayon (en 2D uniquement)
    nodes_in_radius = find_nodes_in_radius_2d(G, node_A_id, feature_1_idx, feature_2_idx, Y_vector_2d, radius_D)
    nodes_in_radius_ids = set([n[0] for n in nodes_in_radius])
    
    print(f"   Nœuds dans le rayon D={radius_D} (distance 2D): {len(nodes_in_radius)}")
    
    # 4. Préparer les données pour la visualisation
    # Placer l'ads à l'origine (0, 0) en translatant tous les points
    all_nodes_x = []
    all_nodes_y = []
    colors = []
    sizes = []
    labels_to_show = {}
    
    # Ajouter le nœud A (ads) à l'origine
    all_nodes_x.append(0)
    all_nodes_y.append(0)
    colors.append('red')
    sizes.append(500)
    labels_to_show[0] = node_A_id
    
    # Ajouter tous les autres nœuds (translatés)
    for node_id in G.nodes():
        if node_id == node_A_id:
            continue
        
        features_v = G.nodes[node_id]['features']
        # Translater pour que l'ads soit à l'origine
        x = features_v[feature_1_idx] - origin_x
        y = features_v[feature_2_idx] - origin_y
        
        all_nodes_x.append(x)
        all_nodes_y.append(y)
        
        # Couleur: vert si dans le rayon, bleu sinon
        if node_id in nodes_in_radius_ids:
            colors.append('lightgreen')
            sizes.append(100)
        else:
            colors.append('lightblue')
            sizes.append(30)
    
    # 5. Créer la visualisation
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Dessiner tous les nœuds
    scatter = ax.scatter(all_nodes_x, all_nodes_y, 
                        c=colors, 
                        s=sizes, 
                        alpha=0.6,
                        edgecolors='black',
                        linewidths=0.5,
                        zorder=2)
    
    # Dessiner le cercle en pointillés représentant le rayon D
    # Maintenant c'est la vraie distance 2D pondérée
    # d = √(y₁ × (x-0)² + y₂ × (y-0)²) = D
    # Pour dessiner le cercle, on utilise l'équation de l'ellipse:
    # (x/a)² + (y/b)² = 1 où a = D/√y₁ et b = D/√y₂
    
    if Y_vector_2d[0] > 0 and Y_vector_2d[1] > 0:
        # Rayon selon chaque axe
        radius_x = radius_D / np.sqrt(Y_vector_2d[0])
        radius_y = radius_D / np.sqrt(Y_vector_2d[1])
        
        # Dessiner une ellipse (cercle dans l'espace pondéré)
        ellipse = patches.Ellipse((0, 0), 
                                 width=2*radius_x, 
                                 height=2*radius_y,
                                 fill=False, 
                                 edgecolor='red', 
                                 linewidth=2, 
                                 linestyle='--',
                                 label=f'Rayon D={radius_D} (distance 2D pondérée)',
                                 zorder=1)
        ax.add_patch(ellipse)
    else:
        # Fallback si les poids sont nuls
        circle = patches.Circle((0, 0), radius_D, 
                               fill=False, 
                               edgecolor='red', 
                               linewidth=2, 
                               linestyle='--',
                               label=f'Rayon D={radius_D}',
                               zorder=1)
        ax.add_patch(circle)
    
    # Ajouter une croix à l'origine (ads)
    ax.plot(0, 0, 'r+', markersize=20, markeredgewidth=3, zorder=3)
    
    # Ajouter des labels pour les nœuds importants
    # Label pour l'ads
    ax.annotate(node_A_id, 
               xy=(0, 0), 
               xytext=(10, 10),
               fontsize=10,
               fontweight='bold',
               color='darkred',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='red', alpha=0.8))
    
    # Labels pour les 10 nœuds les plus proches dans le rayon
    for i, (node_id, dist) in enumerate(nodes_in_radius[:10]):
        features_v = G.nodes[node_id]['features']
        x = features_v[feature_1_idx] - origin_x
        y = features_v[feature_2_idx] - origin_y
        
        ax.annotate(f"{node_id}\n(d={dist:.2f})", 
                   xy=(x, y),
                   xytext=(5, 5),
                   textcoords='offset points',
                   fontsize=7,
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', alpha=0.7))
    
    # Configuration des axes
    ax.set_xlabel(f'Feature {feature_1_idx+1} (poids: {Y_vector[feature_1_idx]:.4f})', fontsize=12)
    ax.set_ylabel(f'Feature {feature_2_idx+1} (poids: {Y_vector[feature_2_idx]:.4f})', fontsize=12)
    ax.set_title(f'Visualisation 2D de la requête: {node_A_id}\n' + 
                f'Distance calculée avec SEULEMENT les 2 features principales\n' +
                f'Rouge: ads (origine), Vert: nœuds dans le rayon (n={len(nodes_in_radius)}), Bleu: autres nœuds',
                fontsize=14, fontweight='bold')
    
    # Ajouter une grille
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
    
    # Légende
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=12, label='Ads (origine)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', markersize=10, label='Nœuds dans le rayon'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=8, label='Autres nœuds'),
        Line2D([0], [0], color='red', linestyle='--', linewidth=2, label=f'Rayon D={radius_D} (2D)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Ajuster les limites pour bien voir l'ellipse
    if Y_vector_2d[0] > 0 and Y_vector_2d[1] > 0:
        radius_x = radius_D / np.sqrt(Y_vector_2d[0])
        radius_y = radius_D / np.sqrt(Y_vector_2d[1])
        margin = max(radius_x, radius_y) * 1.5
    else:
        margin = radius_D * 1.5
    
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    
    # Aspect ratio égal pour une visualisation correcte
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    # Sauvegarder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, f'query_2d_{node_A_id}.png')
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✅ Visualisation 2D sauvegardée: {output_path}")
    plt.show()


def display_queries_summary(G, queries_df):
    """
    Affiche un résumé de toutes les requêtes avec le nombre de nœuds trouvés
    """
    print("\n📋 RÉSUMÉ DES REQUÊTES")
    print("="*80)
    print(f"{'Index':<8} {'ID Requête':<15} {'Nœud':<15} {'Rayon D':<10} {'Nœuds (50D)':<12} {'Nœuds (2D)':<12}")
    print("-"*80)
    
    for idx, row in queries_df.iterrows():
        ad_id = row['point_A']
        Y_vector_str = row['Y_vector']
        radius_D = row['D']
        
        Y_vector = np.array([float(x) for x in Y_vector_str.split(';')])
        node_number = ad_id.split('_')[1]
        node_A_id = f"node_{node_number}"
        
        # Trouver les 2 features principales
        top_2_indices = np.argsort(Y_vector)[-2:][::-1]
        feature_1_idx = top_2_indices[0]
        feature_2_idx = top_2_indices[1]
        Y_vector_2d = np.array([Y_vector[feature_1_idx], Y_vector[feature_2_idx]])
        
        # Compter les nœuds trouvés en 50D
        nodes_found_50d = find_nodes_in_radius(G, node_A_id, Y_vector, radius_D)
        
        # Compter les nœuds trouvés en 2D
        nodes_found_2d = find_nodes_in_radius_2d(G, node_A_id, feature_1_idx, feature_2_idx, Y_vector_2d, radius_D)
        
        print(f"{idx:<8} {ad_id:<15} {node_A_id:<15} {radius_D:<10.2f} {len(nodes_found_50d):<12} {len(nodes_found_2d):<12}")
    
    print("="*80)


def main():
    """
    Fonction principale pour visualiser une requête en 2D
    """
    print("="*80)
    print("🎨 VISUALISATION 2D D'UNE REQUÊTE PUBLICITAIRE")
    print("="*80)
    
    # Obtenir le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Charger le graphe
    pickle_path = os.path.join(script_dir, 'advertising_graph.pkl')
    if not os.path.exists(pickle_path):
        print(f"❌ Fichier graphe introuvable: {pickle_path}")
        print("   Veuillez d'abord exécuter generate_graph.py")
        return
    
    print(f"\n📂 Chargement du graphe depuis: {pickle_path}")
    G = load_graph(pickle_path)
    print(f"✅ Graphe chargé: {G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes")
    
    # 2. Charger les requêtes
    queries_path = os.path.join(script_dir, 'queries_structured.csv')
    queries_df = pd.read_csv(queries_path)
    print(f"✅ {len(queries_df)} requêtes chargées")
    
    # 3. Afficher le résumé des requêtes
    display_queries_summary(G, queries_df)
    
    # 4. Demander à l'utilisateur de choisir une requête
    while True:
        try:
            query_choice = input(f"\n🔍 Entrez l'index de la requête à visualiser (0-{len(queries_df)-1}) ou 'q' pour quitter: ")
            
            if query_choice.lower() == 'q':
                print("👋 Au revoir!")
                return
            
            query_idx = int(query_choice)
            
            if 0 <= query_idx < len(queries_df):
                break
            else:
                print(f"❌ Index invalide. Veuillez entrer un nombre entre 0 et {len(queries_df)-1}")
        except ValueError:
            print("❌ Entrée invalide. Veuillez entrer un nombre ou 'q' pour quitter.")
    
    # 5. Visualiser la requête choisie
    query = queries_df.iloc[query_idx]
    ad_id = query['point_A']
    Y_vector = np.array([float(x) for x in query['Y_vector'].split(';')])
    radius_D = query['D']
    node_A_id = f"node_{ad_id.split('_')[1]}"
    
    print(f"\n✅ Requête sélectionnée: {ad_id}")
    print(f"   Nœud: {node_A_id}")
    print(f"   Rayon D: {radius_D}")
    
    visualize_query_2d(G, node_A_id, Y_vector, radius_D, queries_df)
    
    print("\n" + "="*80)
    print("✅ VISUALISATION TERMINÉE !")
    print("="*80)


if __name__ == "__main__":
    main()