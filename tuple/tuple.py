"""
Problème : Stockage de coordonnées 2D/3D

Énoncé :
Concevez un programme qui stocke un grand nombre de points 2D (coordonnées (x, y)). Le programme doit permettre d'ajouter ces points et de calculer la distance euclidienne entre une paire de points, extraite aléatoirement du stockage. L'objectif est de comparer les performances de deux implémentations : l'une utilisant une liste de tuples pour représenter les points et l'autre une liste de listes. La comparaison portera sur le temps d'exécution total de l'opération d'ajout et des requêtes de calcul de distance, sur un nombre croissant de points.
"""

import time
import random
from typing import List, Tuple, Union


# --- Fonctions de gestion de points ---
# Solution utilisant des tuples (recommandée)
def store_points_with_tuples(num_points: int) -> List[Tuple[float, float]]:
    """
    Crée et retourne une liste de points 2D sous forme de tuples (x, y).
    """
    return [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(num_points)]


# Solution utilisant des listes
def store_points_with_lists(num_points: int) -> List[List[float]]:
    """
    Crée et retourne une liste de points 2D sous forme de listes [x, y].
    """
    return [[random.uniform(0, 1000), random.uniform(0, 1000)] for _ in range(num_points)]


def calculate_distance(p1: Union[Tuple, List], p2: Union[Tuple, List]) -> float:
    """
    Calcule la distance euclidienne entre deux points (tuples ou listes).
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


# --- Fonctions de test de performance ---
def run_performance_test(store_func, num_points: int, num_queries: int):
    """
    Exécute les tests de performance pour une fonction de stockage donnée.
    """
    # 1. Test de l'ajout (création de la liste de points)
    start_time_add = time.perf_counter()
    points = store_func(num_points)
    end_time_add = time.perf_counter()
    duration_add = (end_time_add - start_time_add) * 1000  # en ms

    # 2. Test des requêtes de distance
    start_time_query = time.perf_counter()
    for _ in range(num_queries):
        # Choix de deux indices aléatoires
        idx1 = random.randint(0, num_points - 1)
        idx2 = random.randint(0, num_points - 1)
        calculate_distance(points[idx1], points[idx2])
    end_time_query = time.perf_counter()
    duration_query = (end_time_query - start_time_query) * 1000  # en ms

    return duration_add, duration_query


# --- Script principal (main) ---
def main():
    """
    Fonction principale pour exécuter la comparaison de performance.
    """
    print("--- Comparaison de performance pour le stockage de coordonnées ---")
    print("Les tuples (immuables) sont généralement plus performants pour le stockage.")
    print("-" * 50)

    # Définition des paramètres de test
    test_params = [
        (1_000, 1_000),  # 1000 points, 1000 requêtes
        (10_000, 10_000),  # 10 000 points, 10 000 requêtes
        (100_000, 100_000),  # 100 000 points, 100 000 requêtes
        (500_000, 50_000),  # 500 000 points, 50 000 requêtes
        (1000_000, 100_000)  # 500 000 points, 50 000 requêtes
    ]

    for num_points, num_queries in test_params:
        print(f"\n##### Test avec {num_points} points et {num_queries} requêtes #####")

        # Test avec des tuples
        add_tuple, query_tuple = run_performance_test(store_points_with_tuples, num_points, num_queries)
        print(f"  Tuple: Ajout: {add_tuple:.4f} ms | Requêtes: {query_tuple:.4f} ms")

        # Test avec des listes
        add_list, query_list = run_performance_test(store_points_with_lists, num_points, num_queries)
        print(f"  Liste: Ajout: {add_list:.4f} ms | Requêtes: {query_list:.4f} ms")


if __name__ == "__main__":
    main()
