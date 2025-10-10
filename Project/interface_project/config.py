# -*- coding: utf-8 -*-
"""
Configuration et constantes pour l'application de visualisation de graphe
"""

# ==================== COULEURS ====================

class Colors:
    """Palette de couleurs pour l'interface"""
    
    # Couleurs des noeuds
    NODE_REGULAR_OUTSIDE = '#B0BEC5'
    NODE_REGULAR_INSIDE = '#66BB6A'
    AD_UNSELECTED = '#FF7043'
    AD_SELECTED = '#E53935'
    
    # Couleurs des aretes
    EDGE_NODE_NODE = '#ECEFF1'
    EDGE_AD_NODE = '#FFCCBC'
    
    # Couleurs de l'ellipsoide
    ELLIPSOID_FACE = '#2196F3'
    ELLIPSOID_EDGE = '#1976D2'
    
    # Couleurs de l'interface
    BACKGROUND = '#263238'
    PANEL_BG = '#37474F'
    TEXT_PRIMARY = '#ECEFF1'
    TEXT_SECONDARY = '#B0BEC5'
    ACCENT = '#00BCD4'
    SUCCESS = '#4CAF50'
    ERROR = '#F44336'
    WARNING = '#FF9800'


# ==================== PARAMETRES DE VISUALISATION ====================

class ViewConfig:
    """Configuration de la visualisation 3D"""
    
    # Taille des noeuds
    NODE_SIZE_REGULAR = 20
    NODE_SIZE_REGULAR_INSIDE = 40
    NODE_SIZE_AD_UNSELECTED = 80
    NODE_SIZE_AD_SELECTED = 150
    
    # Transparence
    NODE_ALPHA = 0.7
    EDGE_ALPHA = 0.2
    ELLIPSOID_ALPHA = 0.15
    
    # Largeur des aretes
    EDGE_WIDTH_NODE_NODE = 0.5
    EDGE_WIDTH_AD_NODE = 1.0
    
    # Parametres de l'ellipsoide
    ELLIPSOID_RESOLUTION = 30
    
    # Limites d'affichage des aretes selon le zoom
    EDGE_DISTANCE_THRESHOLD_MIN = 0.1
    EDGE_DISTANCE_THRESHOLD_MAX = 2.0


# ==================== PARAMETRES DE L'APPLICATION ====================

class AppConfig:
    """Configuration generale de l'application"""
    
    # Dimensions de la fenetre
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 900
    WINDOW_TITLE = "Visualisation de Graphe Publicitaire - Recherche Ponderee"
    
    # Dimensions des panneaux
    CONTROL_PANEL_WIDTH = 350
    CONSOLE_HEIGHT = 200
    
    # Parametres du graphe
    DEFAULT_K_NN = 10
    
    # Strategies de recherche disponibles
    SEARCH_STRATEGIES = {
        'naive': 'Naive (O(N))',
        'bfs': 'BFS (O(E))',
        'dijkstra': 'Dijkstra (O(E log V))',
        'hybrid': 'Hybride (Auto)'
    }
    
    # Messages de la console
    CONSOLE_MAX_LINES = 1000
    CONSOLE_TIMESTAMP_FORMAT = "%H:%M:%S"
    
    # Threads
    THREAD_UPDATE_INTERVAL_MS = 100


# ==================== CHEMINS DES FICHIERS ====================

class Paths:
    """Chemins des fichiers de donnees"""
    
    NODES_CSV = "../adsSim_data_nodes.csv"
    ADS_CSV = "../queries_structured.csv"
    GRAPH_PICKLE = "../advertising_graph.pkl"


# ==================== MESSAGES ====================

class Messages:
    """Messages standard de l'application"""
    
    # Construction du graphe
    LOADING_DATA = "Chargement des donnees..."
    BUILDING_KNN = "Construction du graphe K-NN..."
    ADDING_ADS = "Ajout des annonces publicitaires..."
    SAVING_GRAPH = "Sauvegarde du graphe..."
    GRAPH_COMPLETE = "Graphe construit avec succes"
    
    # Recherche
    SEARCH_START = "Recherche en cours..."
    SEARCH_COMPLETE = "Recherche terminee"
    SEARCH_CANCELLED = "Recherche annulee"
    
    # Erreurs
    ERROR_NO_GRAPH = "Aucun graphe charge. Veuillez d'abord construire le graphe."
    ERROR_NO_AD_SELECTED = "Veuillez selectionner une annonce."
    ERROR_INVALID_RADIUS = "Rayon X invalide. Veuillez entrer un nombre positif."
    ERROR_FILE_NOT_FOUND = "Fichier de donnees introuvable."