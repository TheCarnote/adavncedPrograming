# -*- coding: utf-8 -*-
"""
Fenêtre principale de l'application
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .control_panel import ControlPanel
from .graph_viewer_3d import GraphViewer3D
from .log_console import LogConsole
from .progress_dialog import ProgressDialog
from config import AppConfig
from workers.graph_builder import GraphBuilderWorker
from workers.search_worker import SearchWorker


class MainWindow(QMainWindow):
    """
    Fenêtre principale avec layout en 3 zones:
    - Panneau de contrôle (gauche)
    - Visualisation 3D (centre)
    - Console de logs (bas)
    """
    
    def __init__(self):
        super().__init__()
        
        self.graph = None
        self.graph_builder_worker = None
        self.search_worker = None
        self.progress_dialog = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface"""
        
        # Configuration de la fenêtre
        self.setWindowTitle(AppConfig.WINDOW_TITLE)
        self.setGeometry(100, 100, AppConfig.WINDOW_WIDTH, AppConfig.WINDOW_HEIGHT)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ========== ZONE SUPERIEURE (Panneau + Viewer 3D) ==========
        top_splitter = QSplitter(Qt.Horizontal)
        
        # Panneau de contrôle
        self.control_panel = ControlPanel()
        self.control_panel.setFixedWidth(AppConfig.CONTROL_PANEL_WIDTH)
        top_splitter.addWidget(self.control_panel)
        
        # Viewer 3D
        self.graph_viewer = GraphViewer3D()
        top_splitter.addWidget(self.graph_viewer)
        
        top_splitter.setCollapsible(0, False)
        top_splitter.setCollapsible(1, False)
        
        main_layout.addWidget(top_splitter, stretch=1)
        
        # ========== ZONE INFERIEURE (Console) ==========
        self.console = LogConsole()
        self.console.setFixedHeight(AppConfig.CONSOLE_HEIGHT)
        main_layout.addWidget(self.console)
        
        central_widget.setLayout(main_layout)
        
        # ========== CONNEXION DES SIGNAUX ==========
        self.control_panel.build_graph_clicked.connect(self.on_build_graph)
        self.control_panel.load_graph_clicked.connect(self.on_load_graph)
        self.control_panel.regenerate_clicked.connect(self.on_regenerate)
        self.control_panel.search_clicked.connect(self.on_search)
        
        # ========== STYLE GLOBAL ==========
        self.setStyleSheet("""
            QMainWindow {
                background-color: #263238;
            }
        """)
        
        # Message de bienvenue
        self.console.log_step("Application demarree")
        self.console.log("Bienvenue dans l'outil de visualisation de graphe publicitaire !")
        self.console.log_warning("Construisez ou chargez un graphe pour commencer.")
    
    def on_build_graph(self):
        """Construit un nouveau graphe"""
        self.console.log_step("Demarrage de la construction du graphe...")
        
        # Désactiver les contrôles
        self.control_panel.enable_controls(False)
        
        # Créer le worker
        self.graph_builder_worker = GraphBuilderWorker(k_nn=AppConfig.DEFAULT_K_NN, load_existing=False)
        
        # Connecter les signaux
        self.graph_builder_worker.progress.connect(self.on_graph_build_progress)
        self.graph_builder_worker.finished.connect(self.on_graph_build_finished)
        self.graph_builder_worker.error.connect(self.on_graph_build_error)
        
        # Créer le dialogue de progression
        self.progress_dialog = ProgressDialog("Construction du graphe", self)
        self.progress_dialog.cancel_btn.clicked.connect(self.on_cancel_graph_build)
        
        # Démarrer le worker
        self.graph_builder_worker.start()
        self.progress_dialog.exec_()
    
    def on_load_graph(self):
        """Charge un graphe existant"""
        self.console.log_step("Chargement du graphe existant...")
        
        # Désactiver les contrôles
        self.control_panel.enable_controls(False)
        
        # Créer le worker
        self.graph_builder_worker = GraphBuilderWorker(load_existing=True)
        
        # Connecter les signaux
        self.graph_builder_worker.progress.connect(self.on_graph_build_progress)
        self.graph_builder_worker.finished.connect(self.on_graph_build_finished)
        self.graph_builder_worker.error.connect(self.on_graph_build_error)
        
        # Créer le dialogue de progression
        self.progress_dialog = ProgressDialog("Chargement du graphe", self)
        self.progress_dialog.cancel_btn.clicked.connect(self.on_cancel_graph_build)
        
        # Démarrer le worker
        self.graph_builder_worker.start()
        self.progress_dialog.exec_()
    
    def on_graph_build_progress(self, percentage, message):
        """Mise à jour de la progression de construction"""
        if self.progress_dialog:
            self.progress_dialog.update_progress(percentage, message)
        
        self.console.log(message)
    
    def on_graph_build_finished(self, graph):
        """Appelé quand la construction est terminée"""
        self.graph = graph
        
        # Fermer le dialogue
        if self.progress_dialog:
            self.progress_dialog.accept()
        
        # Charger le graphe dans l'interface
        self.load_graph(graph)
        
        # Réactiver les contrôles
        self.control_panel.enable_controls(True)
        
        self.console.log_success("Graphe pret a etre visualise !")
    
    def on_graph_build_error(self, error_message):
        """Appelé en cas d'erreur"""
        if self.progress_dialog:
            self.progress_dialog.reject()
        
        self.console.log_error(error_message)
        
        # Réactiver les contrôles
        self.control_panel.enable_controls(True)
        
        QMessageBox.critical(self, "Erreur", error_message)
    
    def on_cancel_graph_build(self):
        """Annule la construction du graphe"""
        if self.graph_builder_worker:
            self.console.log_warning("Annulation de la construction...")
            self.graph_builder_worker.cancel()
        
        if self.progress_dialog:
            self.progress_dialog.reject()
        
        # Réactiver les contrôles
        self.control_panel.enable_controls(True)
    
    def on_regenerate(self):
        """Régénère la vue 3D avec les features sélectionnées"""
        features = self.control_panel.get_selected_features()
        self.console.log_step("Regeneration de la vue 3D avec features {0}...".format(features))
        
        if self.graph:
            self.graph_viewer.set_graph(self.graph, features)
            self.console.log_success("Vue 3D regeneree !")
        else:
            self.console.log_error("Aucun graphe charge")
    
    def on_search(self):
        """Lance une recherche"""
        ad = self.control_panel.get_selected_ad()
        radius = self.control_panel.get_radius()
        method = self.control_panel.get_selected_method()
        
        if not ad:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner un ad.")
            return
        
        if radius is None or radius <= 0:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un rayon X valide.")
            return
        
        if not self.graph:
            QMessageBox.warning(self, "Erreur", "Aucun graphe charge.")
            return
        
        self.console.log_step("Recherche: ad={0}, X={1}, methode={2}".format(ad, radius, method))
        
        # Sélectionner l'ad dans la vue 3D
        self.graph_viewer.set_selected_ad(ad)
        
        # Désactiver les contrôles
        self.control_panel.enable_controls(False)
        
        # Créer le worker
        self.search_worker = SearchWorker(self.graph, ad, radius, method)
        
        # Connecter les signaux
        self.search_worker.progress.connect(self.on_search_progress)
        self.search_worker.finished.connect(self.on_search_finished)
        self.search_worker.error.connect(self.on_search_error)
        
        # Créer le dialogue
        self.progress_dialog = ProgressDialog("Recherche en cours", self)
        self.progress_dialog.progress_bar.setMaximum(0)  # Mode indéterminé
        self.progress_dialog.cancel_btn.clicked.connect(self.on_cancel_search)
        
        # Démarrer
        self.search_worker.start()
        self.progress_dialog.exec_()
    
    def on_search_progress(self, message):
        """Mise à jour de la progression de recherche"""
        self.console.log(message)
    
    def on_search_finished(self, nodes_found, elapsed_time):
        """Recherche terminée"""
        if self.progress_dialog:
            self.progress_dialog.accept()
        
        # Réactiver les contrôles
        self.control_panel.enable_controls(True)
        
        self.console.log_success("Recherche terminee en {0:.3f}s".format(elapsed_time))
        self.console.log("{0} noeuds trouves dans le rayon X".format(len(nodes_found)))
        
        # Afficher les résultats sur le graphe
        self.graph_viewer.set_search_results(nodes_found)
    
    def on_search_error(self, error_message):
        """Erreur lors de la recherche"""
        if self.progress_dialog:
            self.progress_dialog.reject()
        
        self.console.log_error(error_message)
        self.control_panel.enable_controls(True)
        
        QMessageBox.critical(self, "Erreur", error_message)
    
    def on_cancel_search(self):
        """Annule la recherche"""
        if self.search_worker:
            self.console.log_warning("Annulation de la recherche...")
            self.search_worker.cancel()
        
        if self.progress_dialog:
            self.progress_dialog.reject()
        
        self.control_panel.enable_controls(True)
    
    def load_graph(self, graph):
        """Charge un graphe dans l'interface"""
        self.graph = graph
        
        # Extraire les features
        sample_node = list(graph.nodes(data=True))[0]
        num_features = len(sample_node[1]['features'])
        feature_names = ["feature_{0}".format(i+1) for i in range(num_features)]
        
        # Extraire les ads
        ad_nodes = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'ad']
        
        # Remplir les dropdowns
        self.control_panel.set_features(feature_names)
        self.control_panel.set_ads(ad_nodes)
        
        # Afficher le graphe en 3D avec les 3 premières features
        self.graph_viewer.set_graph(graph, (0, 1, 2))
        
        self.console.log_success("Graphe charge : {0} noeuds, {1} aretes".format(
            graph.number_of_nodes(), graph.number_of_edges()))
        self.console.log("   - {0} ads disponibles".format(len(ad_nodes)))
        self.console.log("   - {0} features par noeud".format(num_features))