import time
import random
from typing import List, Any


# --- Solution Optimale (avec Set) ---
def remove_duplicates_with_set(data: List[Any]) -> List[Any]:
    """
    Élimine les doublons d'une liste en utilisant un set pour une performance optimale.
    Complexité: O(n) en moyenne.
    """
    return list(set(data))


# --- Solution Manuelle (non optimisée) ---
def remove_duplicates_manually(data: List[Any]) -> List[Any]:
    """
    Élimine les doublons d'une liste en itérant manuellement.
    Complexité: O(n^2) car 'in' sur une liste est une opération O(n).
    """
    unique_list = []
    for item in data:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


# --- Fonction principale de test ---
def main():
    """
    Fonction principale qui exécute les tests de performance.
    """
    print("--- Comparaison de performance pour l'élimination des doublons ---")
    print("L'utilisation d'un set est la méthode recommandée pour cette tâche.")
    print("-" * 50)

    # Génération des tests de performance
    # Nous commençons avec 1000 éléments et multiplions par 5 à chaque fois.
    test_sizes = [1_000, 5_000, 25_000, 125_000, 625_000]

    for size in test_sizes:
        # Création d'une liste avec des doublons pour le test
        # environ 50% de doublons
        data_to_test = [random.randint(0, size // 2) for _ in range(size)]

        print(f"\n##### Test avec {size} éléments #####")

        # Test de la solution avec Set
        start_time_set = time.perf_counter()
        result_set = remove_duplicates_with_set(data_to_test)
        end_time_set = time.perf_counter()
        duration_set = (end_time_set - start_time_set) * 1000  # en ms

        # Test de la solution manuelle
        start_time_manual = time.perf_counter()
        result_manual = remove_duplicates_manually(data_to_test)
        end_time_manual = time.perf_counter()
        duration_manual = (end_time_manual - start_time_manual) * 1000  # en ms

        # Vérification de la justesse (les deux solutions doivent donner le même résultat)
        assert sorted(result_set) == sorted(result_manual)

        print(f"  Méthode avec Set : {duration_set:.4f} ms")
        print(f"  Méthode Manuelle : {duration_manual:.4f} ms")


if __name__ == "__main__":
    main()
