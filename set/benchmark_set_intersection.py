import time
import random
from typing import List, Any


# --- Solution Optimale (avec Set) ---
def has_common_elements_with_set(list1: List[Any], list2: List[Any]) -> bool:
    """
    Vérifie l'existence d'un élément commun entre deux listes en utilisant des sets.
    Complexité: O(n + m), où n et m sont les tailles des deux listes.
    C'est très performant car la création du set et l'intersection sont rapides.
    """
    # Convertir une des listes en set pour une recherche rapide (O(1) en moyenne)
    set1 = set(list1)

    # Parcourir la deuxième liste et vérifier si un élément est dans le set
    for item in list2:
        if item in set1:
            return True

    return False


# Note: Une solution encore plus courte serait 'return bool(set(list1) & set(list2))'
# mais la version ci-dessus est plus pédagogique et s'arrête dès qu'un commun est trouvé.

# --- Solution Manuelle (avec double boucle) ---
def has_common_elements_manually(list1: List[Any], list2: List[Any]) -> bool:
    """
    Vérifie l'existence d'un élément commun entre deux listes avec une double boucle.
    Complexité: O(n * m), où n et m sont les tailles des deux listes.
    Cette approche est très inefficace pour de grandes listes.
    """
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                return True

    return False


# --- Fonction principale de test ---
def main():
    """
    Fonction principale qui exécute les tests de performance.
    """
    print("--- Comparaison de performance pour la détection d'éléments communs ---")
    print("L'utilisation des sets est la méthode recommandée pour cette tâche.")
    print("-" * 50)

    # Génération des tests de performance
    # Nous commençons avec 1000 éléments et multiplions par 5 à chaque fois.
    test_sizes = [1_000, 5_000, 25_000, 125_000, 625_000]

    # On garantit qu'il y a toujours un élément commun pour que les boucles ne parcourent pas toute la liste.
    common_element = "common"

    for size in test_sizes:
        # Création des listes de test
        list_a = [f"item_{i}" for i in range(size)]
        list_b = [f"item_{j}" for j in range(size)]

        # Ajout de l'élément commun à la fin pour maximiser le temps de recherche pour la méthode manuelle
        list_a.append(common_element)
        list_b.append(common_element)
        #random.shuffle(list_a)
        #random.shuffle(list_b)

        print(f"\n##### Test avec des listes de {size} éléments #####")

        # Test de la solution avec Set
        start_time_set = time.perf_counter()
        result_set = has_common_elements_with_set(list_a, list_b)
        end_time_set = time.perf_counter()
        duration_set = (end_time_set - start_time_set) * 1000  # en ms

        # Test de la solution manuelle
        start_time_manual = time.perf_counter()
        result_manual = has_common_elements_manually(list_a, list_b)
        end_time_manual = time.perf_counter()
        duration_manual = (end_time_manual - start_time_manual) * 1000  # en ms

        # Vérification de la justesse
        assert result_set == result_manual == True

        print(f"  Méthode avec Set : {duration_set:.4f} ms")
        print(f"  Méthode Manuelle : {duration_manual:.4f} ms")


if __name__ == "__main__":
    main()
