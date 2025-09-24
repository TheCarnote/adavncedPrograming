import random
import time
from typing import List, Tuple, Dict, Optional
import multiprocessing
import sys

# --- Implémentations du problème Two Sum (fonctions inchangées) ---

def two_sum_naive(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Méthode 1: Force brute avec deux boucles imbriquées. O(n^2)."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None

def two_sum_sorted_optimized(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Méthode 2: Optimisation pour une liste triée. O(n log n)."""
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
    """Méthode 3: La solution la plus efficace, O(n)."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

# --- Fonctions utilitaires ---

def run_single_test(args):
    """
    Fonction enveloppe pour un test unique, destinée à être exécutée par le pool.
    Renvoie le nom de la méthode, du jeu de données, et le temps d'exécution.
    """
    impl_name, impl_func, dataset_name, dataset, target = args
    start_time = time.time()
    try:
        impl_func(dataset, target)
        duration = time.time() - start_time
        return (impl_name, dataset_name, 'success', duration)
    except Exception as e:
        return (impl_name, dataset_name, 'error', str(e))

def generate_dataset(size: int) -> List[int]:
    """Génère un ensemble de données de la taille spécifiée."""
    return [random.randint(-10**9, 10**9) for _ in range(size)]

def generate_viable_target(nums: List[int]) -> int:
    """Génère une cible valide en sélectionnant aléatoirement deux nombres."""
    idx1, idx2 = random.sample(range(len(nums)), 2)
    return nums[idx1] + nums[idx2]

def run_performance_test_with_pool(
    implementations: Dict[str, callable],
    datasets: Dict[str, List[int]],
    pool_size: int = 4
) -> None:
    """
    Exécute les tests de performance en utilisant un pool de processus.
    """
    print("🚀 Début des tests de performance avec un pool de processus.")
    print("-" * 70)
    
    results = {}
    tasks = []

    # Créer la liste des tâches à exécuter par le pool
    for dataset_name, dataset in datasets.items():
        target = generate_viable_target(dataset)
        for impl_name, impl_func in implementations.items():
            # Ajout de chaque test au pool de tâches
            tasks.append((impl_name, impl_func, dataset_name, dataset, target))

    # Utilisation d'un pool de processus
    with multiprocessing.Pool(processes=pool_size) as pool:
        # map_async envoie toutes les tâches en parallèle
        async_result = pool.map_async(run_single_test, tasks)
        
        # Attendre la fin des tâches avec un affichage de progression
        while not async_result.ready():
            print(f"Progression... {len(tasks) - async_result._number_left} / {len(tasks)} tâches terminées.", end='\r')
            time.sleep(1)

        print("\n✅ Toutes les tâches sont terminées.")
        
        # Récupérer les résultats
        for impl_name, dataset_name, status, duration in async_result.get():
            if status == 'success':
                results[(dataset_name, impl_name)] = duration
            else:
                results[(dataset_name, impl_name)] = 'Erreur'

    # Affichage récapitulatif
    print("\n🏆 Récapitulatif des performances")
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
        "750k": generate_dataset(750000),
        "1.5M": generate_dataset(1500000)
    }
    print("✅ Génération terminée.")
    
    # La taille du pool peut être ajustée ici
    run_performance_test_with_pool(implementations, datasets, pool_size=4)
