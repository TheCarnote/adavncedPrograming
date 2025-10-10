# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour l'application
"""

import time
from datetime import datetime


def format_time(seconds):
    """
    Formate un temps en secondes en format lisible
    
    Args:
        seconds: Temps en secondes
        
    Returns:
        String formaté (ex: "1.23s" ou "123.45ms")
    """
    if seconds < 1:
        return "{0:.2f}ms".format(seconds * 1000)
    elif seconds < 60:
        return "{0:.2f}s".format(seconds)
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return "{0}m {1:.1f}s".format(minutes, secs)


def format_number(number):
    """
    Formate un nombre avec des séparateurs de milliers
    
    Args:
        number: Nombre à formater
        
    Returns:
        String formaté (ex: "5,000")
    """
    return "{0:,}".format(number)


def get_timestamp():
    """
    Retourne un timestamp formaté pour les logs
    
    Returns:
        String avec l'heure actuelle (ex: "14:32:15")
    """
    return datetime.now().strftime("%H:%M:%S")


class Timer:
    """
    Classe utilitaire pour mesurer le temps d'exécution
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Démarre le chronomètre"""
        self.start_time = time.time()
        self.end_time = None
    
    def stop(self):
        """Arrête le chronomètre"""
        self.end_time = time.time()
    
    def elapsed(self):
        """
        Retourne le temps écoulé
        
        Returns:
            Temps en secondes (float)
        """
        if self.start_time is None:
            return 0
        
        if self.end_time is None:
            return time.time() - self.start_time
        
        return self.end_time - self.start_time
    
    def elapsed_formatted(self):
        """
        Retourne le temps écoulé formaté
        
        Returns:
            String formaté
        """
        return format_time(self.elapsed())