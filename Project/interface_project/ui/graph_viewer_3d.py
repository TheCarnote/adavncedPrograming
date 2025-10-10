# -*- coding: utf-8 -*-
"""
Widget de visualisation 3D du graphe avec Matplotlib
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox
from PyQt5.QtCore import Qt
import numpy as np

# Matplotlib imports
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

from config import Colors, ViewConfig


class GraphViewer3D(QWidget):
    """
    Widget de visualisation 3D du graphe avec Matplotlib
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.graph = None
        self.selected_features = (0, 1, 2)
        self.selected_ad = None
        self.search_results = []
        self.show_edges = False  # Par défaut désactivé
        
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface"""
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # ========== TOOLBAR SUPERIEUR ==========
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        self.info_label = QLabel("Aucun graphe charge")
        self.info_label.setStyleSheet("color: #B0BEC5; font-size: 12px;")
        toolbar_layout.addWidget(self.info_label)
        
        toolbar_layout.addStretch()
        
        # Checkbox pour afficher les arêtes
        self.edges_checkbox = QCheckBox("Afficher les aretes")
        self.edges_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ECEFF1;
                font-size: 11px;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #546E7A;
                border-radius: 3px;
                background-color: #263238;
            }
            QCheckBox::indicator:checked {
                background-color: #00BCD4;
                border-color: #00BCD4;
            }
        """)
        self.edges_checkbox.stateChanged.connect(self.on_toggle_edges)
        toolbar_layout.addWidget(self.edges_checkbox)
        
        # Bouton Reset vue
        self.reset_btn = QPushButton("Reset Vue")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #546E7A;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 15px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #607D8B;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_view)
        toolbar_layout.addWidget(self.reset_btn)
        
        layout.addLayout(toolbar_layout)
        
        # ========== CANVAS MATPLOTLIB ==========
        # Figure plus grande et sans marges
        self.figure = Figure(figsize=(12, 8), facecolor='#263238', tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        
        # Activer le zoom avec la molette
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        
        self.ax = self.figure.add_subplot(111, projection='3d', facecolor='#263238')
        
        # Configurer l'apparence
        self.ax.set_xlabel('Feature X', color='#ECEFF1', fontsize=10)
        self.ax.set_ylabel('Feature Y', color='#ECEFF1', fontsize=10)
        self.ax.set_zlabel('Feature Z', color='#ECEFF1', fontsize=10)
        self.ax.tick_params(colors='#ECEFF1', labelsize=9)
        
        # Grille
        self.ax.grid(True, alpha=0.2, color='#ECEFF1')
        
        # Couleur des panes
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('#37474F')
        self.ax.yaxis.pane.set_edgecolor('#37474F')
        self.ax.zaxis.pane.set_edgecolor('#37474F')
        
        layout.addWidget(self.canvas)
        
        # ========== TOOLBAR NAVIGATION MATPLOTLIB ==========
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #37474F;
                border: none;
                spacing: 5px;
            }
            QToolButton {
                background-color: #546E7A;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #607D8B;
            }
        """)
        layout.addWidget(self.toolbar)
        
        self.setLayout(layout)
        
        # Style global
        self.setStyleSheet("""
            QWidget {
                background-color: #263238;
            }
        """)
    
    def on_scroll(self, event):
        """Gère le zoom avec la molette de la souris"""
        if event.button == 'up':
            # Zoom in
            scale_factor = 0.9
        elif event.button == 'down':
            # Zoom out
            scale_factor = 1.1
        else:
            return
        
        # Récupérer les limites actuelles
        xlim = self.ax.get_xlim3d()
        ylim = self.ax.get_ylim3d()
        zlim = self.ax.get_zlim3d()
        
        # Calculer les centres
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        z_center = (zlim[0] + zlim[1]) / 2
        
        # Calculer les nouvelles limites
        x_range = (xlim[1] - xlim[0]) * scale_factor / 2
        y_range = (ylim[1] - ylim[0]) * scale_factor / 2
        z_range = (zlim[1] - zlim[0]) * scale_factor / 2
        
        self.ax.set_xlim3d([x_center - x_range, x_center + x_range])
        self.ax.set_ylim3d([y_center - y_range, y_center + y_range])
        self.ax.set_zlim3d([z_center - z_range, z_center + z_range])
        
        self.canvas.draw()
    
    def on_toggle_edges(self, state):
        """Active/désactive l'affichage des arêtes"""
        self.show_edges = (state == Qt.Checked)
        self.render_graph()
    
    def set_graph(self, graph, selected_features=(0, 1, 2)):
        """
        Charge un graphe et l'affiche
        
        Args:
            graph: Graphe NetworkX
            selected_features: Tuple (idx_x, idx_y, idx_z) des features a afficher
        """
        self.graph = graph
        self.selected_features = selected_features
        self.selected_ad = None
        self.search_results = []
        
        self.render_graph()
    
    def render_graph(self):
        """Affiche le graphe en 3D"""
        
        if self.graph is None:
            return
        
        # Effacer le plot précédent
        self.ax.clear()
        
        # Reconfigurer les labels
        feature_indices = self.selected_features
        self.ax.set_xlabel(f'Feature {feature_indices[0] + 1}', color='#ECEFF1', fontsize=10)
        self.ax.set_ylabel(f'Feature {feature_indices[1] + 1}', color='#ECEFF1', fontsize=10)
        self.ax.set_zlabel(f'Feature {feature_indices[2] + 1}', color='#ECEFF1', fontsize=10)
        self.ax.tick_params(colors='#ECEFF1', labelsize=9)
        
        # Grille
        self.ax.grid(True, alpha=0.2, color='#ECEFF1')
        
        # Extraire les noeuds réguliers
        regular_nodes = [(n, d) for n, d in self.graph.nodes(data=True) 
                         if d.get('node_type') == 'regular']
        
        # Extraire les ads
        ad_nodes = [(n, d) for n, d in self.graph.nodes(data=True) 
                    if d.get('node_type') == 'ad']
        
        # Dictionnaire des positions pour les arêtes
        node_positions = {}
        
        # ========== AFFICHER LES ARETES (SI ACTIVÉ) ==========
        if self.show_edges:
            # Limiter le nombre d'arêtes affichées pour la performance
            edge_limit = 5000
            edges_to_draw = list(self.graph.edges())[:edge_limit]
            
            for edge in edges_to_draw:
                node1_id, node2_id = edge
                
                # Récupérer les positions
                node1_data = self.graph.nodes[node1_id]
                node2_data = self.graph.nodes[node2_id]
                
                features1 = np.array(node1_data['features'])
                features2 = np.array(node2_data['features'])
                
                x1, y1, z1 = features1[feature_indices[0]], features1[feature_indices[1]], features1[feature_indices[2]]
                x2, y2, z2 = features2[feature_indices[0]], features2[feature_indices[1]], features2[feature_indices[2]]
                
                # Déterminer la couleur selon le type d'arête
                edge_type = self.graph.edges[edge].get('edge_type', 'node_node')
                if edge_type == 'ad_node':
                    color = '#FF7043'  # Orange pour ad-node
                    alpha = 0.3
                else:
                    color = '#546E7A'  # Gris pour node-node
                    alpha = 0.1
                
                self.ax.plot([x1, x2], [y1, y2], [z1, z2], 
                            color=color, linewidth=0.5, alpha=alpha)
        
        # ========== AFFICHER LES NOEUDS REGULIERS ==========
        if regular_nodes:
            regular_positions = []
            regular_colors = []
            
            for node_id, data in regular_nodes:
                features = np.array(data['features'])
                x = features[feature_indices[0]]
                y = features[feature_indices[1]]
                z = features[feature_indices[2]]
                regular_positions.append([x, y, z])
                node_positions[node_id] = (x, y, z)
                
                # Couleur selon si dans les résultats de recherche
                if node_id in self.search_results:
                    regular_colors.append(Colors.NODE_REGULAR_INSIDE)
                else:
                    regular_colors.append(Colors.NODE_REGULAR_OUTSIDE)
            
            regular_positions = np.array(regular_positions)
            
            self.ax.scatter(
                regular_positions[:, 0],
                regular_positions[:, 1],
                regular_positions[:, 2],
                c=regular_colors,
                s=ViewConfig.NODE_SIZE_REGULAR,
                alpha=ViewConfig.NODE_ALPHA,
                edgecolors='white',
                linewidths=0.5,
                label='Noeuds reguliers',
                depthshade=True
            )
        
        # ========== AFFICHER LES ADS ==========
        if ad_nodes:
            ad_positions = []
            ad_colors = []
            ad_sizes = []
            
            for node_id, data in ad_nodes:
                features = np.array(data['features'])
                x = features[feature_indices[0]]
                y = features[feature_indices[1]]
                z = features[feature_indices[2]]
                ad_positions.append([x, y, z])
                node_positions[node_id] = (x, y, z)
                
                # Couleur et taille selon si sélectionné
                if node_id == self.selected_ad:
                    ad_colors.append(Colors.AD_SELECTED)
                    ad_sizes.append(ViewConfig.NODE_SIZE_AD_SELECTED)
                else:
                    ad_colors.append(Colors.AD_UNSELECTED)
                    ad_sizes.append(ViewConfig.NODE_SIZE_AD_UNSELECTED)
            
            ad_positions = np.array(ad_positions)
            
            self.ax.scatter(
                ad_positions[:, 0],
                ad_positions[:, 1],
                ad_positions[:, 2],
                c=ad_colors,
                s=ad_sizes,
                alpha=ViewConfig.NODE_ALPHA,
                edgecolors='white',
                linewidths=1.5,
                marker='D',  # Diamant
                label='Annonces (Ads)',
                depthshade=True
            )
        
        # Légende
        self.ax.legend(loc='upper right', fontsize=9, facecolor='#37474F', 
                      edgecolor='#546E7A', labelcolor='#ECEFF1')
        
        # Ajuster les limites pour bien voir le graphe
        if len(node_positions) > 0:
            all_positions = np.array(list(node_positions.values()))
            x_min, y_min, z_min = all_positions.min(axis=0)
            x_max, y_max, z_max = all_positions.max(axis=0)
            
            # Ajouter une marge de 10%
            x_margin = (x_max - x_min) * 0.1
            y_margin = (y_max - y_min) * 0.1
            z_margin = (z_max - z_min) * 0.1
            
            self.ax.set_xlim([x_min - x_margin, x_max + x_margin])
            self.ax.set_ylim([y_min - y_margin, y_max + y_margin])
            self.ax.set_zlim([z_min - z_margin, z_max + z_margin])
        
        # Mettre à jour l'info
        total_nodes = self.graph.number_of_nodes()
        total_ads = len(ad_nodes)
        self.info_label.setText(
            f"Graphe: {total_nodes} noeuds ({total_ads} ads) - "
            f"Features: {feature_indices[0]+1}, {feature_indices[1]+1}, {feature_indices[2]+1}"
        )
        
        # Rafraîchir le canvas
        self.canvas.draw()
    
    def set_selected_ad(self, ad_id):
        """Sélectionne un ad"""
        self.selected_ad = ad_id
        self.render_graph()
    
    def set_search_results(self, node_ids):
        """Affiche les résultats d'une recherche"""
        self.search_results = node_ids
        self.render_graph()
    
    def reset_view(self):
        """Reset la vue à l'état initial"""
        self.selected_ad = None
        self.search_results = []
        self.render_graph()
    
    def clear(self):
        """Efface le graphe"""
        self.graph = None
        self.selected_ad = None
        self.search_results = []
        self.ax.clear()
        self.canvas.draw()
        self.info_label.setText("Aucun graphe charge")