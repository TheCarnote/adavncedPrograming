# -*- coding: utf-8 -*-
"""
Panneau de contrôle pour la sélection des features et paramètres de recherche
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QPushButton, QLineEdit, QGroupBox,
                             QSpacerItem, QSizePolicy)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont


class ControlPanel(QWidget):
    """
    Panneau de contrôle avec :
    - Construction/chargement du graphe
    - Sélection de 3 features pour la visualisation
    - Sélection d'un ad
    - Paramètres de recherche (rayon X, méthode)
    """
    
    # Signaux émis par le panneau
    build_graph_clicked = pyqtSignal()  # Construire le graphe
    load_graph_clicked = pyqtSignal()   # Charger un graphe existant
    regenerate_clicked = pyqtSignal()   # Régénérer la vue 3D
    search_clicked = pyqtSignal()       # Lancer recherche
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.feature_names = []
        self.ad_list = []
        
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface du panneau"""
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # ========== TITRE ==========
        title = QLabel("Panneau de Controle")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #00BCD4;
            padding: 10px 0;
        """)
        layout.addWidget(title)
        
        # ========== SECTION 0: CONSTRUCTION DU GRAPHE ==========
        graph_group = QGroupBox("Graphe")
        graph_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #ECEFF1;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        graph_layout = QVBoxLayout()
        
        # Boutons pour construire/charger
        buttons_layout = QHBoxLayout()
        
        self.build_btn = QPushButton("Construire")
        self.build_btn.setMinimumHeight(35)
        self.build_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:disabled {
                background-color: #546E7A;
                color: #90A4AE;
            }
        """)
        self.build_btn.clicked.connect(self.build_graph_clicked.emit)
        buttons_layout.addWidget(self.build_btn)
        
        self.load_btn = QPushButton("Charger")
        self.load_btn.setMinimumHeight(35)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #546E7A;
                color: #90A4AE;
            }
        """)
        self.load_btn.clicked.connect(self.load_graph_clicked.emit)
        buttons_layout.addWidget(self.load_btn)
        
        graph_layout.addLayout(buttons_layout)
        
        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)
        
        # ========== SECTION 1: SÉLECTION DES FEATURES ==========
        features_group = QGroupBox("Visualisation 3D")
        features_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #ECEFF1;
                border: 2px solid #00BCD4;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        features_layout = QVBoxLayout()
        
        features_label = QLabel("Selectionnez 3 features pour l'affichage 3D :")
        features_label.setStyleSheet("color: #B0BEC5; font-size: 11px;")
        features_layout.addWidget(features_label)
        
        # Dropdown 1
        feature1_layout = QHBoxLayout()
        feature1_layout.addWidget(QLabel("Feature X :"))
        self.feature1_combo = QComboBox()
        self.feature1_combo.setMinimumHeight(30)
        feature1_layout.addWidget(self.feature1_combo)
        features_layout.addLayout(feature1_layout)
        
        # Dropdown 2
        feature2_layout = QHBoxLayout()
        feature2_layout.addWidget(QLabel("Feature Y :"))
        self.feature2_combo = QComboBox()
        self.feature2_combo.setMinimumHeight(30)
        feature2_layout.addWidget(self.feature2_combo)
        features_layout.addLayout(feature2_layout)
        
        # Dropdown 3
        feature3_layout = QHBoxLayout()
        feature3_layout.addWidget(QLabel("Feature Z :"))
        self.feature3_combo = QComboBox()
        self.feature3_combo.setMinimumHeight(30)
        feature3_layout.addWidget(self.feature3_combo)
        features_layout.addLayout(feature3_layout)
        
        # Bouton Régénérer
        self.regenerate_btn = QPushButton("Regenerer la vue 3D")
        self.regenerate_btn.setMinimumHeight(40)
        self.regenerate_btn.setEnabled(False)  # Désactivé par défaut
        self.regenerate_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ACC1;
            }
            QPushButton:pressed {
                background-color: #0097A7;
            }
            QPushButton:disabled {
                background-color: #546E7A;
                color: #90A4AE;
            }
        """)
        self.regenerate_btn.clicked.connect(self.regenerate_clicked.emit)
        features_layout.addWidget(self.regenerate_btn)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # ========== SECTION 2: RECHERCHE ==========
        search_group = QGroupBox("Recherche dans le rayon X")
        search_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #ECEFF1;
                border: 2px solid #FF7043;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        search_layout = QVBoxLayout()
        
        ad_label = QLabel("Selection de l'annonce (Ad) :")
        ad_label.setStyleSheet("color: #B0BEC5; font-size: 11px; margin-top: 5px;")
        search_layout.addWidget(ad_label)
        
        self.ad_combo = QComboBox()
        self.ad_combo.setMinimumHeight(30)
        self.ad_combo.setEnabled(False)  # Désactivé par défaut
        search_layout.addWidget(self.ad_combo)
        
        ad_hint = QLabel("Vous pouvez aussi cliquer sur un ad dans le graphe")
        ad_hint.setStyleSheet("color: #78909C; font-size: 10px; font-style: italic;")
        search_layout.addWidget(ad_hint)
        
        # Rayon X
        radius_layout = QHBoxLayout()
        radius_layout.addWidget(QLabel("Rayon X :"))
        self.radius_input = QLineEdit()
        self.radius_input.setPlaceholderText("Ex: 5.0")
        self.radius_input.setMinimumHeight(30)
        self.radius_input.setEnabled(False)  # Désactivé par défaut
        radius_layout.addWidget(self.radius_input)
        search_layout.addLayout(radius_layout)
        
        # Méthode de recherche
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Methode :"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Hybride (Auto)",
            "Naive (O(N))",
            "BFS (O(E))",
            "Dijkstra (O(E log V))"
        ])
        self.method_combo.setMinimumHeight(30)
        self.method_combo.setEnabled(False)  # Désactivé par défaut
        method_layout.addWidget(self.method_combo)
        search_layout.addLayout(method_layout)
        
        # Bouton Lancer recherche
        self.search_btn = QPushButton("Lancer la recherche")
        self.search_btn.setMinimumHeight(40)
        self.search_btn.setEnabled(False)  # Désactivé par défaut
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
            QPushButton:disabled {
                background-color: #546E7A;
                color: #90A4AE;
            }
        """)
        self.search_btn.clicked.connect(self.search_clicked.emit)
        search_layout.addWidget(self.search_btn)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # ========== SPACER ==========
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.setLayout(layout)
        
        # Style global
        self.setStyleSheet("""
            QWidget {
                background-color: #37474F;
                color: #ECEFF1;
            }
            QLabel {
                color: #ECEFF1;
                font-size: 12px;
            }
            QComboBox {
                background-color: #263238;
                color: #ECEFF1;
                border: 1px solid #546E7A;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox:hover {
                border: 1px solid #00BCD4;
            }
            QComboBox::drop-down {
                border: none;
            }
            QLineEdit {
                background-color: #263238;
                color: #ECEFF1;
                border: 1px solid #546E7A;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #00BCD4;
            }
        """)
    
    def set_features(self, feature_names):
        """Remplit les dropdowns avec les noms de features"""
        self.feature_names = feature_names
        
        self.feature1_combo.clear()
        self.feature2_combo.clear()
        self.feature3_combo.clear()
        
        self.feature1_combo.addItems(feature_names)
        self.feature2_combo.addItems(feature_names)
        self.feature3_combo.addItems(feature_names)
        
        if len(feature_names) >= 3:
            self.feature1_combo.setCurrentIndex(0)
            self.feature2_combo.setCurrentIndex(1)
            self.feature3_combo.setCurrentIndex(2)
        
        # Activer le bouton régénérer
        self.regenerate_btn.setEnabled(True)
    
    def set_ads(self, ad_list):
        """Remplit le dropdown avec la liste des ads"""
        self.ad_list = ad_list
        self.ad_combo.clear()
        self.ad_combo.addItems(ad_list)
        
        # Activer les contrôles de recherche
        self.ad_combo.setEnabled(True)
        self.radius_input.setEnabled(True)
        self.method_combo.setEnabled(True)
        self.search_btn.setEnabled(True)
    
    def get_selected_features(self):
        """Retourne les indices des 3 features sélectionnées"""
        return (
            self.feature1_combo.currentIndex(),
            self.feature2_combo.currentIndex(),
            self.feature3_combo.currentIndex()
        )
    
    def get_selected_ad(self):
        """Retourne l'ID de l'ad sélectionné"""
        ad = self.ad_combo.currentText()
        return ad if ad else None
    
    def set_selected_ad(self, ad_id):
        """Sélectionne un ad dans le dropdown"""
        index = self.ad_combo.findText(ad_id)
        if index >= 0:
            self.ad_combo.setCurrentIndex(index)
    
    def get_radius(self):
        """Retourne le rayon X saisi"""
        try:
            return float(self.radius_input.text())
        except ValueError:
            return None
    
    def get_selected_method(self):
        """Retourne la méthode de recherche sélectionnée"""
        text = self.method_combo.currentText()
        if "Hybride" in text:
            return "hybrid"
        elif "Naive" in text:
            return "naive"
        elif "BFS" in text:
            return "bfs"
        elif "Dijkstra" in text:
            return "dijkstra"
        return "hybrid"
    
    def enable_controls(self, enabled=True):
        """Active ou désactive tous les contrôles"""
        self.build_btn.setEnabled(enabled)
        self.load_btn.setEnabled(enabled)
        self.feature1_combo.setEnabled(enabled)
        self.feature2_combo.setEnabled(enabled)
        self.feature3_combo.setEnabled(enabled)
        self.regenerate_btn.setEnabled(enabled and len(self.feature_names) > 0)
        self.ad_combo.setEnabled(enabled and len(self.ad_list) > 0)
        self.radius_input.setEnabled(enabled and len(self.ad_list) > 0)
        self.method_combo.setEnabled(enabled and len(self.ad_list) > 0)
        self.search_btn.setEnabled(enabled and len(self.ad_list) > 0)