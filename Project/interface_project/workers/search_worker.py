# -*- coding: utf-8 -*-
"""
Worker thread pour effectuer une recherche dans le graphe
"""

from PyQt5.QtCore import QThread, pyqtSignal
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import Timer
import numpy as np
from collections import deque


class SearchWorker(QThread):
    """
    Thread worker pour effectuer une recherche dans le rayon X
    """
    
    # Signaux
    progress = pyqtSignal(str)           # Message de progression
    finished = pyqtSignal(list, float)   # (liste des noeuds trouves, temps)
    error = pyqtSignal(str)              # Message d'erreur
    
    def __init__(self, graph, ad_id, radius, method='hybrid'):
        """
        Args:
            graph: Graphe NetworkX
            ad_id: ID de l'ad de reference
            radius: Rayon X de recherche
            method: Methode de recherche ('naive', 'bfs', 'dijkstra', 'hybrid')
        """
        super().__init__()
        self.graph = graph
        self.ad_id = ad_id
        self.radius = radius
        self.method = method
        self._is_cancelled = False
    
    def run(self):
        """Execute la recherche"""
        
        timer = Timer()
        timer.start()
        
        try:
            # Verifier que l'ad existe
            if self.ad_id not in self.graph.nodes():
                self.error.emit("Ad {0} introuvable dans le graphe".format(self.ad_id))
                return
            
            self.progress.emit("Recherche en cours avec methode: {0}...".format(self.method))
            
            # Recuperer les features et Y de l'ad
            ad_data = self.graph.nodes[self.ad_id]
            ad_features = np.array(ad_data['features'])
            ad_Y = np.array(ad_data.get('Y', np.ones(len(ad_features))))
            
            # Choisir la methode
            if self.method == 'naive':
                nodes_found = self._search_naive(ad_features, ad_Y)
            elif self.method == 'bfs':
                nodes_found = self._search_bfs(ad_features, ad_Y)
            elif self.method == 'dijkstra':
                nodes_found = self._search_dijkstra(ad_features, ad_Y)
            else:  # hybrid
                nodes_found = self._search_hybrid(ad_features, ad_Y)
            
            timer.stop()
            
            if not self._is_cancelled:
                self.finished.emit(nodes_found, timer.elapsed())
            
        except Exception as e:
            import traceback
            error_msg = "Erreur lors de la recherche: {0}\n{1}".format(
                str(e), traceback.format_exc())
            self.error.emit(error_msg)
    
    def _compute_weighted_distance(self, features_A, features_B, Y_vector):
        """Calcule la distance ponderee entre deux vecteurs"""
        diff = features_A - features_B
        weighted_diff = Y_vector * diff
        distance = np.linalg.norm(weighted_diff)
        return distance
    
    def _search_naive(self, ad_features, ad_Y):
        """Recherche naive O(N)"""
        nodes_found = []
        
        for node_id, node_data in self.graph.nodes(data=True):
            if self._is_cancelled:
                break
            
            # Skip les ads
            if node_data.get('node_type') == 'ad':
                continue
            
            node_features = np.array(node_data['features'])
            distance = self._compute_weighted_distance(ad_features, node_features, ad_Y)
            
            if distance <= self.radius:
                nodes_found.append(node_id)
        
        return nodes_found
    
    def _search_bfs(self, ad_features, ad_Y):
        """Recherche BFS O(E)"""
        nodes_found = []
        visited = set()
        queue = deque([self.ad_id])
        visited.add(self.ad_id)
        
        while queue and not self._is_cancelled:
            current = queue.popleft()
            
            # Explorer les voisins
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                visited.add(neighbor)
                neighbor_data = self.graph.nodes[neighbor]
                
                # Skip les ads
                if neighbor_data.get('node_type') == 'ad':
                    continue
                
                neighbor_features = np.array(neighbor_data['features'])
                distance = self._compute_weighted_distance(ad_features, neighbor_features, ad_Y)
                
                if distance <= self.radius:
                    nodes_found.append(neighbor)
                    queue.append(neighbor)
        
        return nodes_found
    
    def _search_dijkstra(self, ad_features, ad_Y):
        """Recherche Dijkstra O(E log V)"""
        # Similaire a BFS mais avec une priority queue
        # Pour simplifier, on utilise BFS ici
        return self._search_bfs(ad_features, ad_Y)
    
    def _search_hybrid(self, ad_features, ad_Y):
        """Methode hybride (auto-selection)"""
        # Si le graphe est petit, utiliser naive
        if self.graph.number_of_nodes() < 1000:
            return self._search_naive(ad_features, ad_Y)
        else:
            return self._search_bfs(ad_features, ad_Y)
    
    def cancel(self):
        """Annule la recherche"""
        self._is_cancelled = True
        self.quit()