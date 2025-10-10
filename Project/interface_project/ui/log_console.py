# -*- coding: utf-8 -*-
"""
Widget de console pour afficher les logs de l'application
"""

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor, QColor, QFont, QTextDocument
from PyQt5.QtCore import Qt
from datetime import datetime


class LogConsole(QTextEdit):
    """
    Console de logs avec defilement automatique et coloration des messages
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuration de base
        self.setReadOnly(True)
        
        # Limiter le nombre de lignes (via le document)
        self.document().setMaximumBlockCount(1000)
        
        # Style
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        
        # Police monospace
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
    
    def log(self, message, level="info"):
        """
        Ajoute un message dans la console
        
        Args:
            message: Message a afficher
            level: Niveau du message ('info', 'success', 'warning', 'error', 'step')
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Couleurs selon le niveau
        colors = {
            'info': '#D4D4D4',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#F44336',
            'step': '#00BCD4'
        }
        
        color = colors.get(level, colors['info'])
        
        # Format: [HH:MM:SS] Message
        html = '<span style="color: #888;">[{0}]</span> '.format(timestamp)
        html += '<span style="color: {0};">{1}</span>'.format(color, message)
        
        self.append(html)
        
        # Scroll automatique vers le bas
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()
        )
    
    def log_step(self, message):
        """Log d'une etape (cyan)"""
        self.log("► " + message, "step")
    
    def log_success(self, message):
        """Log de succes (vert)"""
        self.log("✓ " + message, "success")
    
    def log_error(self, message):
        """Log d'erreur (rouge)"""
        self.log("✗ " + message, "error")
    
    def log_warning(self, message):
        """Log d'avertissement (orange)"""
        self.log("⚠ " + message, "warning")
    
    def clear_console(self):
        """Efface la console"""
        self.clear()
        self.log_step("Console effacee")