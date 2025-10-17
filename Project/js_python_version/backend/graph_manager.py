# -*- coding: utf-8 -*-
"""
Gestionnaire du graphe pour l'API
"""

import os
import pickle
import time
from typing import Dict, List, Tuple, Optional
import networkx as nx
import numpy as np

from generate_graph import (
    load_data,
    build_graph,
    compute_weighted_distance
)


class GraphManager:
    """Gestionnaire singleton du graphe"""
    
    def __init__(self):
        self.graph: Optional[nx.Graph] = None
        self.build_time: Optional[float] = None
        
        # Chemin vers le fichier pickle (dossier backend)
        self.backend_dir = os.path.dirname(os.path.abspath(__file__))
        self.graph_path = os.path.join(self.backend_dir, "advertising_graph.pkl")
        
        print(f" GraphManager initialisé")
        print(f"   Répertoire backend: {self.backend_dir}")
        print(f"   Chemin graphe: {self.graph_path}")
    
    def build_new_graph(self, k: int = 10) -> Dict:
        """Construit un nouveau graphe"""
        print(f" CONSTRUCTION DU GRAPHE (K={k})")
        
        start_time = time.time()
        
        # Charger les données
        print(" Chargement des fichiers CSV...")
        load_start = time.time()
        nodes_df, ads_df = load_data()
        load_time = time.time() - load_start
        print(f" Données chargées en {load_time:.3f}s")
        
        if nodes_df is None or ads_df is None:
            raise Exception("Impossible de charger les données CSV")
        
        # Construire le graphe
        print(f"\n  Construction du graphe avec K-NN={k}...")
        build_start = time.time()
        self.graph = build_graph(nodes_df, ads_df, k=k)
        build_time = time.time() - build_start
        print(f" Graphe construit en {build_time:.3f}s")
        
        # Sauvegarder
        print(f"\n Sauvegarde du graphe...")
        save_start = time.time()
        self._save_graph()
        save_time = time.time() - save_start
        print(f" Graphe sauvegardé en {save_time:.3f}s")
        
        total_time = time.time() - start_time
        self.build_time = total_time
        
        
        print(f" CONSTRUCTION TERMINÉE EN {total_time:.3f}s")
        
        
        stats = self._get_graph_stats()
        
        # Retourner les temps
        stats['build_time'] = total_time
        stats['load_time'] = load_time
        stats['construction_time'] = build_time
        stats['save_time'] = save_time
        
        return stats
    
    def load_existing_graph(self) -> Dict:
        """Charge un graphe existant"""
        
        print(f" CHARGEMENT DU GRAPHE EXISTANT")
        
        if not os.path.exists(self.graph_path):
            print(f" Fichier introuvable: {self.graph_path}")
            raise FileNotFoundError(f"Aucun graphe sauvegardé trouvé à {self.graph_path}")
        
        start_time = time.time()
        
        print(f" Chargement depuis: {self.graph_path}")
        with open(self.graph_path, 'rb') as f:
            self.graph = pickle.load(f)
        
        load_time = time.time() - start_time
        
        print(f" Graphe chargé en {load_time:.3f}s")
        
        
        stats = self._get_graph_stats()
        stats['load_time'] = load_time
        
        return stats
    
    def _save_graph(self):
        """Sauvegarde le graphe"""
        if self.graph is None:
            raise Exception("Aucun graphe à sauvegarder")
        
        print(f" Sauvegarde vers: {self.graph_path}")
        
        # S'assurer que le dossier existe
        os.makedirs(os.path.dirname(self.graph_path), exist_ok=True)
        
        with open(self.graph_path, 'wb') as f:
            pickle.dump(self.graph, f)
        
        print(f" Graphe sauvegardé: {self.graph_path}")
    
    def _get_graph_stats(self) -> Dict:
        """Retourne les statistiques du graphe"""
        if self.graph is None:
            return {
                'total_nodes': 0,
                'total_edges': 0,
                'ad_nodes': 0,
                'regular_nodes': 0,
                'num_features': 0,
                'ads': []
            }
        
        regular_nodes = [n for n, d in self.graph.nodes(data=True) 
                        if d.get('node_type') == 'regular']
        ad_nodes = [n for n, d in self.graph.nodes(data=True) 
                   if d.get('node_type') == 'ad']
        
        # Déterminer le nombre de features
        num_features = 0
        for node_id, node_data in self.graph.nodes(data=True):
            if 'features' in node_data:
                num_features = len(node_data['features'])
                break
        
        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'ad_nodes': len(ad_nodes),
            'regular_nodes': len(regular_nodes),
            'num_features': num_features,
            'ads': sorted(ad_nodes)
        }
    
    def get_graph_data(self, feature_indices: Tuple[int, int, int] = (0, 1, 2)) -> Dict:
        """
        Retourne les données du graphe pour la visualisation 3D
        
        Parameters:
        - feature_indices: tuple de 3 indices (x, y, z) pour les axes 3D
        
        Returns:
        - Dict avec 'nodes' et 'links' pour ForceGraph3D
        """
        if self.graph is None:
            raise Exception("Aucun graphe chargé")
        
        print(f"\n Préparation des données 3D (features {feature_indices})...")
        
        fx, fy, fz = feature_indices
        nodes = []
        
        for node_id, node_data in self.graph.nodes(data=True):
            features = node_data.get('features')
            node_type = node_data.get('node_type', 'regular')
            
            if features is None:
                print(f"  Warning: Nœud {node_id} sans features, ignoré")
                continue
            
            node_dict = {
                'id': node_id,
                'type': node_type,
                'x': float(features[fx]),
                'y': float(features[fy]),
                'z': float(features[fz])
            }
            
            # Ajouter le rayon D pour les ads
            if node_type == 'ad':
                radius_D = node_data.get('radius_D')
                if radius_D is not None:
                    node_dict['radius_D'] = float(radius_D)
            
            nodes.append(node_dict)
        
        # Créer les liens
        links = []
        for source, target, edge_data in self.graph.edges(data=True):
            links.append({
                'source': source,
                'target': target,
                'type': edge_data.get('edge_type', 'unknown'),
                'weight': float(edge_data.get('weight', 1.0))
            })
        
        print(f" Données préparées: {len(nodes)} nœuds, {len(links)} liens")
        
        return {
            'nodes': nodes,
            'links': links
        }

    def search_in_radius(self, ad_id: str, radius_X: float, method: str = 'hybrid') -> List[Tuple[str, float]]:
        """
        Recherche les nœuds dans le rayon X autour d'un ad
        
        Returns:
        - Liste de tuples (node_id, distance)
        """
        if self.graph is None:
            raise Exception("Aucun graphe chargé")
        
        if ad_id not in self.graph:
            raise Exception(f"Ad {ad_id} introuvable dans le graphe")
        
        ad_data = self.graph.nodes[ad_id]
        ad_features = ad_data['features']
        Y_vector = ad_data['Y_vector']
        
        print(f"\n🔍 Recherche autour de {ad_id}")
        print(f"   Rayon X: {radius_X:.4f}")
        print(f"   Méthode: {method}")
        
        nodes_found = []
        
        # Recherche selon la méthode
        if method == 'naive':
            nodes_found = self._search_naive(ad_features, Y_vector, radius_X)
        elif method == 'bfs':
            nodes_found = self._search_bfs(ad_id, ad_features, Y_vector, radius_X)
        elif method == 'dijkstra':
            nodes_found = self._search_dijkstra(ad_id, ad_features, Y_vector, radius_X)
        elif method == 'hybrid':
            # Choisir automatiquement la meilleure méthode
            radius_D = ad_data['radius_D']
            ratio = radius_X / radius_D
            
            if ratio <= 0.8:
                print(f"   → Dijkstra (X ≤ 0.8*D)")
                nodes_found = self._search_dijkstra(ad_id, ad_features, Y_vector, radius_X)
            elif ratio <= 1.5:
                print(f"   → BFS (0.8*D < X ≤ 1.5*D)")
                nodes_found = self._search_bfs(ad_id, ad_features, Y_vector, radius_X)
            else:
                print(f"   → Naive (X > 1.5*D)")
                nodes_found = self._search_naive(ad_features, Y_vector, radius_X)
        else:
            raise ValueError(f"Méthode inconnue: {method}")
        
        print(f"✅ {len(nodes_found)} nœuds trouvés")
        
        return nodes_found

    def _search_naive(self, ad_features, Y_vector, radius_X) -> List[Tuple[str, float]]:
        """Recherche naïve (parcours complet)"""
        nodes_found = []
        
        for node_id, node_data in self.graph.nodes(data=True):
            if node_data.get('node_type') != 'regular':
                continue
            
            node_features = node_data['features']
            distance = compute_weighted_distance(ad_features, node_features, Y_vector)
            
            if distance <= radius_X:
                nodes_found.append((node_id, distance))  # CHANGÉ : Retourner tuple (id, distance)
        
        # Trier par distance croissante
        nodes_found.sort(key=lambda x: x[1])
        
        return nodes_found

    def _search_bfs(self, ad_id, ad_features, Y_vector, radius_X) -> List[Tuple[str, float]]:
        """Recherche BFS"""
        nodes_found = []
        visited = set()
        queue = [ad_id]
        visited.add(ad_id)
        
        while queue:
            current = queue.pop(0)
            
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                visited.add(neighbor)
                
                if self.graph.nodes[neighbor].get('node_type') != 'regular':
                    continue
                
                neighbor_features = self.graph.nodes[neighbor]['features']
                distance = compute_weighted_distance(ad_features, neighbor_features, Y_vector)
                
                if distance <= radius_X:
                    nodes_found.append((neighbor, distance))  # CHANGÉ : Retourner tuple (id, distance)
                    queue.append(neighbor)
        
        # Trier par distance croissante
        nodes_found.sort(key=lambda x: x[1])
        
        return nodes_found

    def _search_dijkstra(self, ad_id, ad_features, Y_vector, radius_X) -> List[Tuple[str, float]]:
        """Recherche Dijkstra avec file de priorité"""
        import heapq
        
        nodes_found = []
        visited = set()
        heap = [(0, ad_id)]
        
        while heap:
            current_dist, current = heapq.heappop(heap)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                if self.graph.nodes[neighbor].get('node_type') != 'regular':
                    continue
                
                neighbor_features = self.graph.nodes[neighbor]['features']
                distance = compute_weighted_distance(ad_features, neighbor_features, Y_vector)
                
                if distance <= radius_X:
                    nodes_found.append((neighbor, distance))  # CHANGÉ : Retourner tuple (id, distance)
                    heapq.heappush(heap, (distance, neighbor))
        
        # Trier par distance croissante
        nodes_found.sort(key=lambda x: x[1])
        
        return nodes_found

# ...existing code...
# Singleton global
graph_manager = GraphManager()