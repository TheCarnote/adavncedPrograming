# -*- coding: utf-8 -*-
"""
Algorithmes de recherche dans le rayon X
"""

import networkx as nx
from typing import List
import numpy as np
from collections import deque
import heapq
from generate_graph import compute_weighted_distance


def search_naive(graph: nx.Graph, ad_id: str, radius_X: float) -> List[str]:
    """
    Recherche naïve O(N) : teste tous les nœuds
    """
    ad_data = graph.nodes[ad_id]
    ad_features = np.array(ad_data['features'])
    Y_vector = np.array(ad_data.get('Y', [1.0] * len(ad_features)))
    
    nodes_found = []
    
    for node_id, node_data in graph.nodes(data=True):
        if node_data['node_type'] != 'regular':
            continue
        
        node_features = np.array(node_data['features'])
        distance = compute_weighted_distance(ad_features, node_features, Y_vector)
        
        if distance <= radius_X:
            nodes_found.append(node_id)
    
    return nodes_found


def search_bfs(graph: nx.Graph, ad_id: str, radius_X: float) -> List[str]:
    """
    BFS (Breadth-First Search) O(E) : parcours en largeur
    """
    ad_data = graph.nodes[ad_id]
    ad_features = np.array(ad_data['features'])
    Y_vector = np.array(ad_data.get('Y', [1.0] * len(ad_features)))
    
    nodes_found = []
    visited = set()
    queue = deque([ad_id])
    visited.add(ad_id)
    
    while queue:
        current = queue.popleft()
        
        # Vérifier les voisins
        for neighbor in graph.neighbors(current):
            if neighbor in visited:
                continue
            
            visited.add(neighbor)
            neighbor_data = graph.nodes[neighbor]
            
            if neighbor_data['node_type'] != 'regular':
                queue.append(neighbor)
                continue
            
            neighbor_features = np.array(neighbor_data['features'])
            distance = compute_weighted_distance(ad_features, neighbor_features, Y_vector)
            
            if distance <= radius_X:
                nodes_found.append(neighbor)
                queue.append(neighbor)
    
    return nodes_found


def search_dijkstra(graph: nx.Graph, ad_id: str, radius_X: float) -> List[str]:
    """
    Dijkstra O(E log V) : recherche avec priorité sur les distances
    """
    ad_data = graph.nodes[ad_id]
    ad_features = np.array(ad_data['features'])
    Y_vector = np.array(ad_data.get('Y', [1.0] * len(ad_features)))
    
    nodes_found = []
    distances = {ad_id: 0.0}
    priority_queue = [(0.0, ad_id)]
    visited = set()
    
    while priority_queue:
        current_dist, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Si c'est un nœud régulier, vérifier la distance
        if graph.nodes[current]['node_type'] == 'regular':
            node_features = np.array(graph.nodes[current]['features'])
            distance = compute_weighted_distance(ad_features, node_features, Y_vector)
            
            if distance <= radius_X:
                nodes_found.append(current)
        
        # Explorer les voisins
        for neighbor in graph.neighbors(current):
            if neighbor in visited:
                continue
            
            edge_weight = graph[current][neighbor].get('weight', 1.0)
            new_dist = current_dist + edge_weight
            
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor))
    
    return nodes_found


def search_hybrid(graph: nx.Graph, ad_id: str, radius_X: float) -> List[str]:
    """
    Méthode hybride : choisit automatiquement la meilleure méthode
    """
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    
    # Heuristique : si graphe dense, utiliser BFS, sinon Dijkstra
    density = num_edges / (num_nodes * (num_nodes - 1) / 2)
    
    if density > 0.5 or num_nodes < 1000:
        return search_bfs(graph, ad_id, radius_X)
    else:
        return search_dijkstra(graph, ad_id, radius_X)