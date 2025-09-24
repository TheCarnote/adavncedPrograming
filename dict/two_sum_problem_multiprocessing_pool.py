import random
import time
from typing import List, Tuple, Dict, Optional
import multiprocessing
import sys


# --- Implémentations du problème Two Sum ---

def two_sum_naive(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Méthode 1: Force brute avec deux boucles imbriquées.
    Complexité: O(n^2)
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_sorted_optimized(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Méthode 2: Optimisation pour une liste triée.
    Complexité: O(n log n)
    """
    sorted_nums = sorted(nums)
    left, right = 0, len(sorted_nums) - 1

    while left < right:
        current_sum = sorted_nums[left] + sorted_nums[right]
        if current_sum == target:
            idx1 = nums.index(sorted_nums[left])
            if sorted_nums[left] == sorted_nums[right]:
                nums_copy = list(nums)
                nums_copy[idx1] = float('inf')
                idx2 = nums_copy.index(sorted_nums[right])
            else:
                idx2 = nums.index(sorted_nums[right])
            return (idx1, idx2)
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None


def two_sum_hash_map(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Méthode 3: La solution la plus efficace, utilisant un dictionnaire (hash map).
    Complexité: O(n)
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


# --- Fonctions utilitaires pour le test ---

def worker_runner(func, nums, runs_per_test, shared_time, shared_status):
    """
    Exécute la fonction de test plusieurs fois et stocke le temps.
    """
    try:
        start_time = time.time()
        for _ in range(runs_per_test):
            target = nums[random.randint(0, len(nums) - 1)] + nums[random.randint(0, len(nums) - 1)]
            func(nums, target)
        duration = time.time() - start_time
        shared_time.value = duration
        shared_status.value = True  # Indique que l'exécution s'est terminée avec succès
    except Exception:
        shared_status.value = False  # Indique que l'exécution a échoué
    finally:
        sys.exit(0)


def generate_dataset(size: int) -> List[int]:
    """Génère un ensemble de données de la taille spécifiée."""
    return [random.randint(-10 ** 9, 10 ** 9) for _ in range(size)]


def run_performance_test_stable(
        implementations: Dict[str, callable],
        datasets: Dict[str, List[int]],
        runs_per_test: int = 1000,
        timeout_seconds: int = 30
) -> None:
    """
    Exécute les tests de performance de manière stable en utilisant le multiprocessing.
    """
    print("🚀 Début des tests de performance avec timeout et répétitions (version stable).")
    print("-" * 70)

    results = {}

    with multiprocessing.Manager() as manager:
        for dataset_name, dataset in datasets.items():
            print(f"📊 Données: {dataset_name} ({len(dataset)} éléments)")

            for impl_name, impl_func in implementations.items():
                print(f"  -> Exécution de '{impl_name}'...", end="", flush=True)

                shared_time = manager.Value('d', -1.0)  # 'd' pour double
                shared_status = manager.Value('b', False)  # 'b' pour bool (réussite)

                # Lancer le test dans un processus séparé
                p = multiprocessing.Process(
                    target=worker_runner,
                    args=(impl_func, dataset, runs_per_test, shared_time, shared_status)
                )
                p.start()

                # Attendre la fin du processus avec un timeout
                p.join(timeout=timeout_seconds)

                if p.is_alive():
                    # Si le processus est toujours vivant après le timeout, le tuer
                    p.terminate()
                    p.join()
                    results[(dataset_name, impl_name)] = 'Timeout'
                    print(f" Dépassé le temps limite de {timeout_seconds}s. (Non-polynômial)")
                else:
                    # Le processus s'est terminé, vérifier le statut
                    if shared_status.value:
                        duration = shared_time.value
                        results[(dataset_name, impl_name)] = duration
                        print(f" Terminé en {duration:.4f}s")
                    else:
                        results[(dataset_name, impl_name)] = 'Erreur'
                        print(" Échec de l'exécution.")

            print("-" * 70)

    # Affichage récapitulatif
    print("🏆 Récapitulatif des performances")
    print("-" * 70)

    header = f"{'Dataset':<15} | {'Naïve (n^2)':<25} | {'Optimisé (tri)':<25} | {'Dictionnaire (n)':<25}"
    print(header)
    print("-" * 70)

    for dataset_name in datasets.keys():
        row = f"{dataset_name:<15} | "
        for impl_name in implementations.keys():
            duration_or_status = results.get((dataset_name, impl_name), 'N/A')
            if isinstance(duration_or_status, float):
                display_time = f"{duration_or_status:.4f}s"
            else:
                display_time = duration_or_status
            row += f"{display_time:<25} | "
        print(row.rstrip(' |'))


# --- Exécution principale ---

if __name__ == "__main__":
    implementations = {
        "Naïve (n^2)": two_sum_naive,
        "Optimisé (tri)": two_sum_sorted_optimized,
        "Dictionnaire (n)": two_sum_hash_map
    }

    print("⏳ Génération des ensembles de données de test...")
    datasets = {
        "5k": generate_dataset(5000),
        "25k": generate_dataset(25000),
        "125k": generate_dataset(125000),
        # Des jeux de données plus grands peuvent être ajoutés ici pour des tests intensifs
    }
    print("✅ Génération terminée.")

    run_performance_test_stable(implementations, datasets, runs_per_test=100)
