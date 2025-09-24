import random
import time
from typing import List, Tuple, Dict, Optional


# --- Implémentations du problème Two Sum ---

def two_sum_naive(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Méthode 1: Force brute avec deux boucles imbriquées.
    Complexité: O(n^2) - Très inefficace pour les grands ensembles de données.
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_sorted_optimized(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Méthode 2: Optimisation pour une liste triée (sans dictionnaire).
    Complexité: O(n log n) à cause du tri, puis O(n) pour la recherche.
    """
    sorted_nums = sorted(nums)
    left, right = 0, len(sorted_nums) - 1

    while left < right:
        current_sum = sorted_nums[left] + sorted_nums[right]
        if current_sum == target:
            idx1 = nums.index(sorted_nums[left])
            if sorted_nums[left] == sorted_nums[right]:
                nums_copy = list(nums)  # Create a copy to find the second index
                nums_copy[idx1] = float('inf')  # "Hide" the first element
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
    Complexité: O(n) - Un seul parcours de la liste.
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


# --- Fonctions utilitaires pour le test ---

def generate_dataset(size: int) -> List[int]:
    """Génère un ensemble de données de la taille spécifiée."""
    return [random.randint(-10 ** 9, 10 ** 9) for _ in range(size)]


def generate_viable_target(nums: List[int]) -> int:
    """Génère une cible valide en sélectionnant aléatoirement deux nombres."""
    idx1, idx2 = random.sample(range(len(nums)), 2)
    return nums[idx1] + nums[idx2]


def run_performance_test(
        implementations: Dict[str, callable],
        datasets: Dict[str, List[int]],
        runs_per_test: int = 100,
        timeout_seconds: int = 30
) -> None:
    """
    Exécute les tests de performance. S'arrête si le temps d'exécution dépasse le seuil.
    """
    print("🚀 Début des tests de performance pour le problème des deux sommes.")
    print("-" * 70)

    results = {}
    disabled_implementations = set()

    for dataset_name, dataset in datasets.items():
        print(f"📊 Données: {dataset_name} ({len(dataset)} éléments)")

        target = generate_viable_target(dataset)

        for impl_name, impl_func in implementations.items():
            if impl_name in disabled_implementations:
                print(f"  -> '{impl_name}' | Non exécuté, temps d'exécution précédent trop long.")
                continue

            total_time = 0
            start_time = time.time()

            # Exécution de la fonction pour chaque run
            for _ in range(runs_per_test):
                impl_func(dataset, target)
                current_time = time.time() - start_time
                if current_time > timeout_seconds:
                    print(
                        f"  -> '{impl_name}' | Temps d'exécution a dépassé {timeout_seconds}s. Étape non polynômiale.")
                    disabled_implementations.add(impl_name)
                    break  # Sort de la boucle des runs

            if impl_name not in disabled_implementations:
                total_time = time.time() - start_time
                results[(dataset_name, impl_name)] = total_time
                print(f"  -> '{impl_name}' | Temps total pour {runs_per_test} exécutions : {total_time:.4f}s")
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
            duration = results.get((dataset_name, impl_name), 'Trop lent')
            display_time = f"{duration:.4f}s" if isinstance(duration, float) else duration
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
        "750k": generate_dataset(750000),
        "1.5M": generate_dataset(1500000)
    }
    print("✅ Génération terminée.")

    run_performance_test(implementations, datasets, runs_per_test=100)
