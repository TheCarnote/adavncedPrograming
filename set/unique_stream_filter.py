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


# --- Solution 2 : Mon approche (Gemini) ---
def gemini_proposal(data_stream: List[Any]) -> List[Any]:
    """
    Proposée par Gemini. Cette approche utilise un set pour la recherche rapide.
    Elle préserve l'ordre en construisant une nouvelle liste.
    Complexité : O(n).
    """
    seen_elements = set()
    unique_elements = []
    for item in data_stream:
        if item not in seen_elements:
            seen_elements.add(item)
            unique_elements.append(item)
    return unique_elements


# --- Solution 3 : dictionnary based gemini (enseignant optimisé) ---
def teacher_optimized_with_list(data_stream: List[Any]) -> List[Any]:
    """
    Proposée par l'enseignant. Cette approche utilise une liste et une astuce
    basée sur dict.fromkeys pour une performance ultra-rapide tout en conservant l'ordre.
    Complexité : O(n).
    """
    return list(dict.fromkeys(data_stream))


# --- Solution 4 : La méthode Set la plus directe (Carnote) ---
def filter_unique_direct_set(data_stream: List[Any]) -> List[Any]:
    """
    Filtre les éléments uniques en convertissant directement en set,
    puis en liste. Ne préserve PAS l'ordre d'origine des éléments.
    Complexité : O(n).
    """
    return list(set(data_stream))


# --- Fonction principale de test ---
def main():
    """
    Fonction principale qui exécute les tests de performance.
    """
    print("--- Comparaison de performance pour la détection d'éléments uniques ---")
    print("Test de 4 méthodes : Manuelle, Gemini, Enseignant, et Set Direct.")
    print("La méthode manuelle est désactivée pour les grandes listes.")
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
            print(f"  Méthode Manuelle             : {duration_manual:.4f} ms")
        else:
            result_manual = None
            print("  Méthode Manuelle             : --- (test désactivé, trop lent) ---")

        # Test de ma proposition (Gemini)
        start_time_gemini = time.perf_counter()
        result_gemini = gemini_proposal(data_stream)
        end_time_gemini = time.perf_counter()
        duration_gemini = (end_time_gemini - start_time_gemini) * 1000
        print(f"  Méthode Gemini               : {duration_gemini:.4f} ms")

        # Test de la proposition (dictonnary)
        start_time_teacher = time.perf_counter()
        result_teacher = teacher_optimized_with_list(data_stream)
        end_time_teacher = time.perf_counter()
        duration_teacher = (end_time_teacher - start_time_teacher) * 1000
        print(f"  Méthode dictonnary         : {duration_teacher:.4f} ms")

        # Test de la solution Set directe
        start_time_direct_set = time.perf_counter()
        result_direct_set = filter_unique_direct_set(data_stream)
        end_time_direct_set = time.perf_counter()
        duration_direct_set = (end_time_direct_set - start_time_direct_set) * 1000
        print(f"  Méthode Set du prof (sans ordre) : {duration_direct_set:.4f} ms")

        # Vérification de la justesse (les résultats doivent être les mêmes)
        # Note : On trie pour comparer car les sets ne garantissent pas l'ordre
        if result_manual is not None:
            assert sorted(result_gemini) == sorted(result_manual) == sorted(result_teacher) == sorted(result_direct_set)
        else:
            assert sorted(result_gemini) == sorted(result_teacher) == sorted(result_direct_set)


if __name__ == "__main__":
    main()
