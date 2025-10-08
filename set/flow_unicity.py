import time
import random
from typing import List, Any


# --- Solution 1 : Manuelle (inefficace) ---
def filter_unique_manually(data_stream: List[Any]) -> List[Any]:
    """
    Filtre les éléments uniques d'un flux en itérant manuellement.
    Complexité : O(n*k) où k est la taille de la liste des éléments uniques.
    """
    unique_elements = []
    for item in data_stream:
        if item not in unique_elements:
            unique_elements.append(item)
    return unique_elements


# --- Solution 2 : Optimisée avec Set (la plus courante) ---
def filter_unique_with_set(data_stream: List[Any]) -> List[Any]:
    """
    Filtre les éléments uniques en utilisant un set pour une recherche rapide.
    Complexité : O(n).
    """
    seen_elements = set()
    unique_elements = []
    for item in data_stream:
        if item not in seen_elements:
            seen_elements.add(item)
            unique_elements.append(item)
    return unique_elements


# --- Solution 3 : Pythonique et Ultra-rapide ---
def filter_unique_pythonic(data_stream: List[Any]) -> List[Any]:
    """
    Filtre les éléments uniques en utilisant la conversion directe en set et liste.
    Complexité : O(n).
    """
    return list(dict.fromkeys(data_stream))


# --- Fonction principale de test ---
def main():
    """
    Fonction principale qui exécute les tests de performance.
    """
    print("--- Comparaison de performance pour la détection d'éléments uniques ---")
    print("Test de 3 méthodes : Manuelle, avec Set, et Pythonique.")
    print("La méthode manuelle est désactivée pour les tailles > 150,000 pour éviter les délais.")
    print("-" * 50)

    # Génération des tests de performance
    test_sizes = [1_000, 5_000, 25_000, 150_000, 750_000, 1_500_000]

    for size in test_sizes:
        # Création d'un flux de données avec des doublons.
        data_stream = [random.randint(0, int(size * 0.75)) for _ in range(size)]

        print(f"\n##### Test avec un flux de {size} éléments #####")

        # Test de la solution Manuelle
        if size <= 150_000:
            start_time_manual = time.perf_counter()
            result_manual = filter_unique_manually(data_stream)
            end_time_manual = time.perf_counter()
            duration_manual = (end_time_manual - start_time_manual) * 1000
            print(f"  Méthode Manuelle  : {duration_manual:.4f} ms")
        else:
            result_manual = None
            print("  Méthode Manuelle  : --- (test désactivé, trop lent) ---")

        # Test de la solution avec Set
        start_time_set = time.perf_counter()
        result_set = filter_unique_with_set(data_stream)
        end_time_set = time.perf_counter()
        duration_set = (end_time_set - start_time_set) * 1000
        print(f"  Méthode avec Set  : {duration_set:.4f} ms")

        # Test de la solution Pythonique
        start_time_pythonic = time.perf_counter()
        result_pythonic = filter_unique_pythonic(data_stream)
        end_time_pythonic = time.perf_counter()
        duration_pythonic = (end_time_pythonic - start_time_pythonic) * 1000
        print(f"  Méthode Pythonique: {duration_pythonic:.4f} ms")

        # Vérification de la justesse (uniquement si le test manuel a été exécuté)
        if result_manual is not None:
            assert sorted(result_set) == sorted(result_manual) == sorted(result_pythonic)
        else:
            assert sorted(result_set) == sorted(result_pythonic)


if __name__ == "__main__":
    main()
