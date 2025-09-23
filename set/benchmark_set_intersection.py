import time
from typing import List, Any


# --- 1) Naïve : double boucle ---
def intersection_naive(list1: List[Any], list2: List[Any]) -> List[Any]:
    commons = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2 and item1 not in commons:
                commons.append(item1)
                break
    return commons


# --- 2) Avec "in" ---
def intersection_with_in(list1: List[Any], list2: List[Any]) -> List[Any]:
    commons = []
    for item in list1:
        if item in list2 and item not in commons:
            commons.append(item)
    return commons


# --- 3) Avec tri et parcours ---
def intersection_sorted(list1: List[Any], list2: List[Any]) -> List[Any]:
    list1 = sorted(list1)
    list2 = sorted(list2)
    i = j = 0
    commons = []
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            if not commons or commons[-1] != list1[i]:
                commons.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return commons


# --- 4) Avec set ---
def intersection_with_set(list1: List[Any], list2: List[Any]) -> List[Any]:
    return list(set(list1) & set(list2))


# --- Benchmark ---
def main():
    print("--- Comparaison de performance des méthodes d’intersection ---")
    test_sizes = [1_000, 5_000, 10_000, 20_000, 100_000]

    for size in test_sizes:
        list_a = [f"item_{i}" for i in range(size)]
        list_b = [f"item_{j}" for j in range(size)]

        # Ajouter un élément commun garanti
        list_a.append("common")
        list_b.append("common")

        print(f"\n##### Test avec {size} éléments #####")

        # Dictionnaire des fonctions
        methods = {
            "Naïve (double boucle)": intersection_naive,
            "List + in": intersection_with_in,
            "List + tri": intersection_sorted,
            "Set": intersection_with_set,
        }

        # Exécuter et mesurer
        results = {}
        for name, func in methods.items():
            start = time.perf_counter()
            result = func(list_a, list_b)
            end = time.perf_counter()
            duration = (end - start) * 1000
            results[name] = (result, duration)
            print(f"  {name:<20} : {duration:8.4f} ms ({len(result)} éléments)")

        # Vérification cohérence des résultats
        all_results = [set(r[0]) for r in results.values()]
        assert all(r == all_results[0] for r in all_results), "⚠️ Les méthodes ne donnent pas le même résultat !"


if __name__ == "__main__":
    main()
