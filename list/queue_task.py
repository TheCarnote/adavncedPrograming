from typing import List, Any
import time


# --- Solution proposée par défaut (intentionnellement inefficace) ---
def process_tasks_list_based(tasks: List[Any], operation: str, value: Any = None) -> Any:
    """
    Gère les tâches d'une file d'attente en utilisant une liste.
    Cette implémentation utilise une liste de manière non optimale pour simuler une file d'attente.
    Les ajouts en début de liste sont inefficaces (O(n)).

    Args:
        tasks (List[Any]): La liste représentant la file d'attente.
        operation (str): L'opération à effectuer ('add' ou 'process').
        value (Any): La tâche à ajouter, si l'opération est 'add'.

    Returns:
        Any: La tâche traitée si l'opération est 'process', sinon None.
    """
    if operation == "add":
        # Ajout en début de liste, ce qui est une opération lente (O(n)) pour une liste.
        tasks.insert(0, value)
        return None
    elif operation == "process":
        # Retrait du dernier élément (non-FIFO), ce qui est incorrect.
        if tasks:
            return tasks.pop()
        return None

    raise ValueError("Opération non valide. Utilisez 'add' ou 'process'.")


# --- Fonction principale de test ---
def main():
    """
    Fonction principale qui teste la solution et montre son échec.
    """
    print("Bienvenue dans le testeur de file d'attente FIFO.")
    print("La solution par défaut utilise une liste de manière incorrecte.")
    print("Pour que les tests réussissent, les étudiants doivent implémenter une solution FIFO valide.")
    print("-" * 50)

    print("--- Démarrage des tests de correction ---")

    # Cas de test 1 : Ordre d'arrivée incorrect
    print("\nTest 1: Ordre d'arrivée (FIFO) -- Échec attendu pour la solution par défaut")
    tasks = []

    # Ajout des tâches
    print("  Ajout de 'Tache A'...")
    process_tasks_list_based(tasks, "add", "Tache A")
    print("  Ajout de 'Tache B'...")
    process_tasks_list_based(tasks, "add", "Tache B")
    print("  Ajout de 'Tache C'...")
    process_tasks_list_based(tasks, "add", "Tache C")

    # Traitement des tâches
    print("  Traitement des tâches...")
    processed_task1 = process_tasks_list_based(tasks, "process")
    processed_task2 = process_tasks_list_based(tasks, "process")
    processed_task3 = process_tasks_list_based(tasks, "process")

    # L'ordre correct devrait être 'Tache A', 'Tache B', 'Tache C'
    expected_order = ["Tache A", "Tache B", "Tache C"]
    actual_order = [processed_task1, processed_task2, processed_task3]

    if actual_order == expected_order:
        print("  Test 1 PASSED ✅")
    else:
        print("  Test 1 FAILED ❌")
        print(f"    Ordre attendu : {expected_order}")
        print(f"    Ordre obtenu  : {actual_order}")

    print("\n--- Fin des tests de correction ---")
    print("-" * 50)
    print("La solution par défaut a échoué car elle n'a pas respecté l'ordre FIFO.")
    print(
        "Une solution correcte pour une file d'attente devrait utiliser le principe du 'premier arrivé, premier servi'.")


if __name__ == "__main__":
    main()
