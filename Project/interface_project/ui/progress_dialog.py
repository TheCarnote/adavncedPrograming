# -*- coding: utf-8 -*-
"""
Dialogue de progression pour les operations longues
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PyQt5.QtCore import Qt


class ProgressDialog(QDialog):
    """
    Dialogue avec barre de progression et bouton d'annulation
    """
    
    def __init__(self, title="Operation en cours", parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(500, 150)
        
        self.cancelled = False
        
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface"""
        
        layout = QVBoxLayout()
        
        # Message
        self.message_label = QLabel("Initialisation...")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Bouton Annuler
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.on_cancel)
        layout.addWidget(self.cancel_btn)
        
        self.setLayout(layout)
        
        # Style
        self.setStyleSheet("""
            QDialog {
                background-color: #37474F;
            }
            QLabel {
                color: #ECEFF1;
                font-size: 13px;
                padding: 10px;
            }
            QProgressBar {
                border: 2px solid #546E7A;
                border-radius: 5px;
                text-align: center;
                background-color: #263238;
                color: #ECEFF1;
            }
            QProgressBar::chunk {
                background-color: #00BCD4;
            }
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E53935;
            }
        """)
    
    def update_progress(self, value, message):
        """
        Met a jour la progression
        
        Args:
            value: Pourcentage (0-100)
            message: Message a afficher
        """
        self.progress_bar.setValue(value)
        self.message_label.setText(message)
    
    def on_cancel(self):
        """Appele quand on clique sur Annuler"""
        self.cancelled = True
        self.message_label.setText("Annulation en cours...")
        self.cancel_btn.setEnabled(False)
    
    def is_cancelled(self):
        """Retourne True si l'operation a ete annulee"""
        return self.cancelled