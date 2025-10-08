# longest_substring.py

import time
import random
import string
from typing import Dict, List


# --- Fonctions à tester ---

def length_of_longest_substring_naive(s: str) -> int:
    """
    Méthode 1: Naïve avec triple boucle. Très inefficace.
    Complexité: O(n^3)
    """
    n = len(s)
    if n == 0:
        return 0

    max_len = 0
    for i in range(n):
        for j in range(i, n):
            # Vérifier si la sous-chaîne s[i:j+1] a des caractères uniques
            substring = s[i:j + 1]
            if len(set(substring)) == len(substring):
                max_len = max(max_len, len(substring))
            else:
                break
    return max_len


def length_of_longest_substring_optimized_no_dict(s: str) -> int:
    """
    Méthode 2: Fenêtre glissante avec un set. Moins efficace que la méthode par dictionnaire.
    Complexité: O(n^2)
    """
    n = len(s)
    if n == 0:
        return 0

    max_len = 0
    i = 0  # Pointeur de début de fenêtre
    j = 0  # Pointeur de fin de fenêtre
    current_window = set()

    while j < n:
        if s[j] not in current_window:
            current_window.add(s[j])
            max_len = max(max_len, len(current_window))
            j += 1
        else:
            # Un doublon a été trouvé, on retire le premier caractère
            # de la fenêtre jusqu'à ce que le doublon soit éliminé
            current_window.remove(s[i])
            i += 1

    return max_len

def length_of_longest_substring_optimized_dict(s: str) -> int:
    """
    Méthode 3: Fenêtre glissante avec un dictionnaire pour un accès en temps constant.
    Complexité: O(n)
    """
    n = len(s)
    if n == 0:
        return 0

    char_map = {}
    max_len = 0
    start = 0

    for end in range(n):
        char = s[end]
        if char in char_map and char_map[char] >= start:
            start = char_map[char] + 1

        char_map[char] = end
        max_len = max(max_len, end - start + 1)

    return max_len

def length_of_longest_substring_array(s: str) -> int:
    """
    Fenêtre glissante avec un tableau de 256 éléments (pour ASCII).
    Plus rapide que le dict en pratique, même complexité O(n).
    """
    n = len(s)
    if n == 0:
        return 0

    # Tableau pour stocker la dernière position de chaque caractère (ASCII 0-255)
    last_seen = [-1] * 256
    max_len = 0
    start = 0

    for end in range(n):
        char_code = ord(s[end])
        if last_seen[char_code] >= start:
            start = last_seen[char_code] + 1
        
        last_seen[char_code] = end
        max_len = max(max_len, end - start + 1)

    return max_len

# --- Fonctions utilitaires pour le test ---

def generate_dataset(size: int) -> str:
    """Génère une chaîne de caractères aléatoire de la taille spécifiée."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(size))


def run_performance_test(implementations: Dict[str, callable], datasets: Dict[str, str]) -> None:
    """
    Exécute les tests de performance pour chaque implémentation sur chaque jeu de données.
    """
    print("🚀 Début des tests de performance pour le problème de la plus longue sous-chaîne.")
    print("-" * 70)

    results = {}

    for dataset_name, dataset in datasets.items():
        print(f"📊 Données: {dataset_name} ({len(dataset)} caractères)")

        # Exécuter et tester chaque implémentation
        for impl_name, impl_func in implementations.items():
            start_time = time.time()
            result = impl_func(dataset)
            duration = time.time() - start_time

            results[(dataset_name, impl_name)] = duration
            print(f"  -> '{impl_name}' | Temps d'exécution : {duration:.4f}s | Résultat : {result}")
        print("-" * 70)

    # Affichage récapitulatif
    print("🏆 Récapitulatif des performances")
    print("-" * 70)

    # header = f"{'Dataset':<15}  | {'Dictionnaire (n)':<20} | {'Tableau ASCII (n)':<20}"
    header = f"{'Dataset':<15} | {'Naïve (n^3)':<20} | {'Set (n^2)':<20} | {'Dictionnaire (n)':<20} | {'Tableau ASCII (n)':<20}"
    print(header)
    print("-" * 70)

    for dataset_name in datasets.keys():
        row = f"{dataset_name:<15} | "
        for impl_name in implementations.keys():
            duration = results.get((dataset_name, impl_name), 'N/A')
            display_time = f"{duration:.4f}s" if isinstance(duration, float) else duration
            row += f"{display_time:<20} | "
        print(row.rstrip(' |'))


if __name__ == "__main__":
    implementations = {
        "Naïve (n^3)": length_of_longest_substring_naive,
        "Set (n^2)": length_of_longest_substring_optimized_no_dict,
        "Dictionnaire (n)": length_of_longest_substring_optimized_dict,
        "Tableau ASCII (n)": length_of_longest_substring_array,
    }

    print("⏳ Génération des ensembles de données de test...")
    datasets = {
        "5k": generate_dataset(5000),
        "10k": generate_dataset(50000),
        "100k": generate_dataset(500000),
        "200k": generate_dataset(1000000),
        "300k": generate_dataset(5000000),
    }
    print("✅ Génération terminée.")

    run_performance_test(implementations, datasets)
