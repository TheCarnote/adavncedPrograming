"""
Point d'entrée de l'application
"""

import sys
import os

# Ajouter le dossier courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Fonction principale"""
    
    app = QApplication(sys.argv)
    
    # Style global de l'application
    app.setStyle('Fusion')
    
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()