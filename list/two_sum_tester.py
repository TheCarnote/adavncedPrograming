import time
from typing import List, Optional


# --- Solution par défaut (peu performante) ---
def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Retourne les indices de deux nombres dans la liste 'nums' dont la somme vaut 'target'.

    Cette implémentation est de complexité O(n^2), ce qui est inefficace pour de grandes listes.
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return sorted([i, j])
    return None

def two_sum_v2(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Version optimisée de la fonction two_sum utilisant un dictionnaire pour une complexité O(n).
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return sorted([seen[complement], i])
        seen[num] = i
    return None

# --- Tests de Correction ---
def run_correctness_tests():
    """Exécute 5 tests pour vérifier la justesse de la solution."""
    print("--- Démarrage des tests de correction ---")
    tests = [
        ([2, 7, 11, 15], 9, [0, 1]),  # Cas simple
        ([3, 2, 4], 6, [1, 2]),  # Ordre différent
        ([3, 3], 6, [0, 1]),  # Éléments identiques
        ([1, 2, 3, 4, 5], 10, None),  # Pas de solution
        ([-1, -2, 3, 5], 2, [0, 2])  # Nombres négatifs
    ]
    all_passed = True
    for i, (nums, target, expected) in enumerate(tests):
        result = two_sum_v2(nums, target)
        # On trie le résultat pour éviter les problèmes d'ordre ([1, 2] vs [2, 1])
        if result is not None:
            result.sort()

        if result == expected:
            print(f"Test de correction #{i + 1} : PASSED ✅")
        else:
            print(f"Test de correction #{i + 1} : FAILED ❌")
            print(f"  Entrée : nums={nums}, target={target}")
            print(f"  Attendu : {expected}")
            print(f"  Obtenu : {result}")
            all_passed = False

    if all_passed:
        print("\nTous les tests de correction ont réussi. 🎉")
    else:
        print("\nCertains tests de correction ont échoué. 😥")
    print("--- Fin des tests de correction ---")
    print("-" * 50)


# --- Tests de Performance ---
def run_performance_tests():
    """Exécute 5 tests pour évaluer la performance de la solution."""
    print("--- Démarrage des tests de performance ---")

    # Génération des jeux de données pour les tests de performance
    sizes = [10, 100, 1000, 10000, 50000]
    # Création de listes où la solution est toujours à la fin pour maximiser le temps de recherche pour la solution O(n^2)
    performance_tests = [
        (list(range(s)), s - 2 + s - 1) for s in sizes
    ]

    all_passed = True
    for i, (nums, target) in enumerate(performance_tests):
        start_time = time.time()
        two_sum_v2(nums, target)
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Conversion en millisecondes

        size = len(nums)
        print(f"Test de performance #{i + 1} : Taille de la liste = {size}")
        print(f"  Temps d'exécution : {duration:.4f} ms")

    print("\nLes temps d'exécution montrent l'efficacité de la solution pour différentes tailles de données.")
    print("--- Fin des tests de performance ---")
    print("-" * 50)


# --- Fonction principale (main) ---
def main():
    """Fonction principale pour exécuter tous les tests."""
    print("Bienvenue dans le testeur de solution 'Two Sum'.")
    print("Remplacez la fonction `two_sum` par votre solution et ré-exécutez ce script.\n")

    run_correctness_tests()
    run_performance_tests()
    


if __name__ == "__main__":
    main()
