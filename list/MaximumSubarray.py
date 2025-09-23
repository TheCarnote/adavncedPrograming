import time
from typing import List


# --- Solution par défaut (peu performante, O(n^2)) ---
def max_subarray_brute_force(nums: List[int]) -> int:
    """
    Calcule la somme maximale d'un sous-tableau en testant toutes les possibilités.
    Complexité: O(n^2).
    """
    if not nums:
        return 0

    max_sum = float('-inf')
    n = len(nums)

    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += nums[j]
            if current_sum > max_sum:
                max_sum = current_sum

    return max_sum


# --- Solution optimale (Algorithme de Kadane, O(n)) ---
def max_subarray_kadane(nums: List[int]) -> int:
    """
    Calcule la somme maximale d'un sous-tableau en utilisant l'algorithme de Kadane.
    Complexité: O(n).
    """
    if not nums:
        return 0

    current_max = nums[0]
    global_max = nums[0]

    for i in range(1, len(nums)):
        # Pour chaque élément, soit on l'ajoute au sous-tableau précédent,
        # soit on commence un nouveau sous-tableau avec cet élément.
        current_max = max(nums[i], current_max + nums[i])

        # On met à jour la somme maximale globale si nécessaire.
        if current_max > global_max:
            global_max = current_max

    return global_max


# --- Fonctions de test et de comparaison ---
def run_correctness_tests(solution_func, func_name: str):
    """Exécute des tests pour vérifier la justesse d'une solution."""
    print(f"--- Démarrage des tests de correction pour {func_name} ---")
    tests = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),  # Cas classique
        ([1], 1),  # Un seul élément
        ([-1], -1),  # Un seul élément négatif
        ([5, 4, -1, 7, 8], 23),  # Tous positifs
        ([-2, -1], -1),  # Tous négatifs
        ([0, -1, 0, 1, 2], 3)  # Avec des zéros
    ]

    all_passed = True
    for i, (nums, expected) in enumerate(tests):
        result = solution_func(nums)
        if result == expected:
            print(f"Test de correction #{i + 1} : PASSED ✅")
        else:
            print(f"Test de correction #{i + 1} : FAILED ❌")
            print(f"  Entrée : nums={nums}")
            print(f"  Attendu : {expected}")
            print(f"  Obtenu : {result}")
            all_passed = False

    if all_passed:
        print("\nTous les tests de correction ont réussi. 🎉")
    else:
        print("\nCertains tests de correction ont échoué. 😥")
    print("--- Fin des tests de correction ---")
    print("-" * 50)


def run_performance_tests(solution_func, func_name: str):
    """Exécute des tests pour évaluer la performance de la solution."""
    print(f"--- Démarrage des tests de performance pour {func_name} ---")

    sizes = [1000, 5000, 10000, 50000, 100000]

    for i, size in enumerate(sizes):
        nums = list(range(size))

        start_time = time.time()
        solution_func(nums)
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Conversion en millisecondes

        print(f"Test de performance #{i + 1} : Taille de la liste = {size}")
        print(f"  Temps d'exécution : {duration:.4f} ms")

    print("--- Fin des tests de performance ---")
    print("-" * 50)


# --- Fonction principale (main) ---
def main():
    """Fonction principale pour exécuter tous les tests."""
    print("Bienvenue dans le testeur de solutions 'Maximum Subarray'.")
    print("Vous pouvez utiliser les fonctions `max_subarray_brute_force` et `max_subarray_kadane` comme modèles.")
    print("Remplacez ces fonctions par votre propre solution pour la tester.\n")

    # Exécution des tests pour la solution "brute force"
    print("\n##### Tests pour la solution O(n^2) par défaut #####")
    run_correctness_tests(max_subarray_brute_force, "Solution O(n^2)")
    run_performance_tests(max_subarray_brute_force, "Solution O(n^2)")

    # Exécution des tests pour l'algorithme de Kadane
    print("\n##### Tests pour la solution O(n) (Kadane) #####")
    run_correctness_tests(max_subarray_kadane, "Algorithme de Kadane")
    run_performance_tests(max_subarray_kadane, "Algorithme de Kadane")


if __name__ == "__main__":
    main()
