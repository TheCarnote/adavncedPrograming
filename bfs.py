from typing import Dict, List, Any
import time


# --- Solution par défaut (fonctionnelle mais inefficace pour les grandes listes) ---
def bfs_list_based(graph: Dict[Any, List[Any]], start_node: Any) -> Dict[Any, int]:
    """
    Implémentation du Parcours en Largeur (BFS) utilisant une liste Python.

    Cette version est fonctionnelle mais l'utilisation de list.pop(0) rend l'opération
    de retrait inefficace (complexité O(n)), impactant la performance sur de grands graphes.

    Args:
        graph (Dict): Le graphe représenté par un dictionnaire d'adjacence.
        start_node (Any): Le nœud de départ.

    Returns:
        Dict: Un dictionnaire des distances minimales de chaque nœud au nœud de départ.
    """
    distances = {node: -1 for node in graph}
    distances[start_node] = 0

    queue = [start_node]  # Utilisation d'une liste pour simuler la file d'attente

    while queue:
        current_node = queue.pop(0)  # !!! Opération inefficace (O(n)) !!!

        for neighbor in graph.get(current_node, []):
            if distances[neighbor] == -1:
                distances[neighbor] = distances[current_node] + 1
                queue.append(neighbor)

    return distances


# --- Espace pour la solution de l'étudiant ---
# def bfs_optimized(graph: Dict[Any, List[Any]], start_node: Any) -> Dict[Any, int]:
#    """
#    Implémentation optimisée du Parcours en Largeur (BFS) utilisant collections.deque.
#    Complexité: O(V + E).
#    """
#    from collections import deque
#    distances = {node: -1 for node in graph}
#    distances[start_node] = 0
#
#    queue = deque([start_node])
#
#    while queue:
#        current_node = queue.popleft()
#
#        for neighbor in graph.get(current_node, []):
#            if distances[neighbor] == -1:
#                distances[neighbor] = distances[current_node] + 1
#                queue.append(neighbor)
#
#    return distances

# --- Fonctions de test ---
def run_correctness_tests(solution_func, func_name: str):
    """Exécute des tests pour vérifier la justesse d'une solution."""
    print(f"--- Démarrage des tests de correction pour {func_name} ---")
    graph_small = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    expected_distances_small = {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 2}

    try:
        result = solution_func(graph_small, 'A')
        if result == expected_distances_small:
            print(f"Test de correction sur le petit graphe : PASSED ✅")
        else:
            print(f"Test de correction sur le petit graphe : FAILED ❌")
            print(f"  Attendu: {expected_distances_small}")
            print(f"  Obtenu: {result}")
    except Exception as e:
        print(f"Test de correction a échoué avec une erreur : {e}")

    print("--- Fin des tests de correction ---")
    print("-" * 50)


def run_performance_tests(solution_func, func_name: str):
    """Exécute 5 tests pour évaluer la performance de la solution."""
    print(f"--- Démarrage des tests de performance pour {func_name} ---")

    num_nodes = 500
    for i in range(20):
        # Création d'un graphe en ligne pour illustrer la performance
        graph_perf = {j: [j + 1] if j < num_nodes - 1 else [] for j in range(num_nodes)}

        start_time = time.time()
        solution_func(graph_perf, 0)
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # en ms

        print(f"Test de performance #{i + 1}: Graphe de {num_nodes} nœuds")
        print(f"  Temps d'exécution : {duration:.4f} ms")

        num_nodes *= 2  # On double le nombre de nœuds pour le prochain test

    print("--- Fin des tests de performance ---")
    print("-" * 50)


# --- Fonction principale (main) ---
def main():
    """Fonction principale pour exécuter tous les tests."""
    print("Bienvenue dans le testeur d'algorithme de Parcours en Largeur (BFS).")
    print("La solution par défaut est fonctionnelle, mais pas performante.")
    print("Remplacez la fonction `bfs_list_based` par votre solution et ré-exécutez ce script.")
    print("-" * 50)

    # Exécution des tests pour la solution par défaut
    run_correctness_tests(bfs_list_based, "Solution avec liste")
    run_performance_tests(bfs_list_based, "Solution avec liste")


if __name__ == "__main__":
    main()
