# -*- coding: utf-8 -*-
"""
Worker thread pour la construction du graphe en arriere-plan
"""

from PyQt5.QtCore import QThread, pyqtSignal
import sys
import os

# Importer le module de generation de graphe
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generate_graph import load_data, build_graph, save_graph, load_graph as load_graph_from_file
from config import Paths, Messages
from utils.helpers import Timer


class GraphBuilderWorker(QThread):
    """
    Thread worker pour construire le graphe de maniere asynchrone
    """
    
    # Signaux emis par le worker
    progress = pyqtSignal(int, str)  # (pourcentage, message)
    finished = pyqtSignal(object)     # (graph)
    error = pyqtSignal(str)           # (message d'erreur)
    
    def __init__(self, k_nn=10, load_existing=False):
        """
        Args:
            k_nn: Nombre de voisins pour K-NN
            load_existing: Si True, charge le graphe existant au lieu de le reconstruire
        """
        super().__init__()
        self.k_nn = k_nn
        self.load_existing = load_existing
        self._is_cancelled = False
    
    def run(self):
        """Execute la construction du graphe"""
        
        timer = Timer()
        timer.start()
        
        try:
            if self.load_existing:
                # Charger un graphe existant
                self.progress.emit(0, "Chargement du graphe existant...")
                
                import os
                script_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(script_dir)
                pickle_path = os.path.join(parent_dir, Paths.GRAPH_PICKLE)
                
                if not os.path.exists(pickle_path):
                    self.error.emit("Fichier graphe introuvable. Construction d'un nouveau graphe...")
                    # Continuer avec la construction
                    self.load_existing = False
                else:
                    graph = load_graph_from_file(pickle_path)
                    self.progress.emit(100, "Graphe charge avec succes ({0:.2f}s)".format(timer.elapsed()))
                    self.finished.emit(graph)
                    return
            
            # Construction d'un nouveau graphe
            
            # Etape 1: Chargement des donnees (10%)
            if self._is_cancelled:
                return
            
            self.progress.emit(0, Messages.LOADING_DATA)
            nodes_df, ads_df = load_data()
            
            if nodes_df is None or ads_df is None:
                self.error.emit(Messages.ERROR_FILE_NOT_FOUND)
                return
            
            self.progress.emit(10, "Donnees chargees: {0} noeuds, {1} ads ({2:.2f}s)".format(
                len(nodes_df), len(ads_df), timer.elapsed()))
            
            # Etape 2: Construction du graphe K-NN (10% -> 50%)
            if self._is_cancelled:
                return
            
            self.progress.emit(10, Messages.BUILDING_KNN)
            graph = build_graph(nodes_df, ads_df, k=self.k_nn)
            
            if self._is_cancelled:
                return
            
            self.progress.emit(50, "Graphe K-NN construit: {0} noeuds, {1} aretes ({2:.2f}s)".format(
                graph.number_of_nodes(), graph.number_of_edges(), timer.elapsed()))
            
            # Etape 3: Ajout des ads (50% -> 80%)
            if self._is_cancelled:
                return
            
            self.progress.emit(80, Messages.ADDING_ADS)
            
            # Etape 4: Sauvegarde (80% -> 90%)
            if self._is_cancelled:
                return
            
            self.progress.emit(90, Messages.SAVING_GRAPH)
            
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            save_graph(graph, parent_dir)
            
            # Termine
            timer.stop()
            self.progress.emit(100, Messages.GRAPH_COMPLETE + " ({0})".format(timer.elapsed_formatted()))
            self.finished.emit(graph)
            
        except Exception as e:
            import traceback
            error_msg = "Erreur lors de la construction du graphe: {0}\n{1}".format(
                str(e), traceback.format_exc())
            self.error.emit(error_msg)
    
    def cancel(self):
        """Annule l'operation en cours"""
        self._is_cancelled = True
        self.quit()