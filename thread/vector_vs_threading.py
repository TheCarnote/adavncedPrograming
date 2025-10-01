import threading
import time
import random
import numpy as np
import math


def calculer_somme_sin_partielle(liste_a_traiter, resultat, index):
    """Tâche CPU-bound pour le multithreading : calcule la somme du sinus."""
    somme_partielle = sum(math.sin(x) for x in liste_a_traiter)
    resultat[index] = somme_partielle


def executer_comparaison():
    """Exécute les trois méthodes de calcul et affiche les résultats."""
    print("--- Comparaison de performance sur 100 millions d'éléments ---")

    taille_vecteur = 100_000_000

    # Génération des données
    # Les nombres entiers sont suffisants car np.sin() gère les types.
    vecteur_py = [random.randint(0, 100) for _ in range(taille_vecteur)]
    vecteur_np = np.array(vecteur_py, dtype=np.float64)  # Conversion en tableau NumPy, type float pour le sin()

    # 1. Calcul Séquentiel (boucle Python)
    print("Calcul séquentiel en cours (boucle Python)...")
    temps_debut_seq = time.perf_counter()
    somme_totale_sequentielle = sum(math.sin(x) for x in vecteur_py)
    temps_fin_seq = time.perf_counter()
    temps_seq = temps_fin_seq - temps_debut_seq
    print(f"Temps séquentiel: {temps_seq:.4f} secondes.\n")

    # 2. Calcul avec Multithreading (4 threads)
    print("Calcul avec 4 threads en cours...")
    nb_threads = 4
    threads = []
    resultats_partiels = [0] * nb_threads

    taille_partie = taille_vecteur // nb_threads

    temps_debut_thread = time.perf_counter()

    for i in range(nb_threads):
        debut = i * taille_partie
        fin = debut + taille_partie
        partie = vecteur_py[debut:fin]
        thread = threading.Thread(target=calculer_somme_sin_partielle, args=(partie, resultats_partiels, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    somme_totale_thread = sum(resultats_partiels)
    temps_fin_thread = time.perf_counter()
    temps_thread = temps_fin_thread - temps_debut_thread

    print(f"Temps avec 4 threads: {temps_thread:.4f} secondes.")
    print(
        f"Le temps avec des threads est {'plus long' if temps_thread > temps_seq else 'similaire' if abs(temps_thread - temps_seq) < 0.1 else 'plus court'} que le temps séquentiel.\n")
    print(
        "Explication: L'utilisation de math.sin() est une tâche CPU-bound, et le GIL empêche le parallélisme. Le surcoût de la gestion des threads peut même ralentir l'exécution.")

    # 3. Calcul Vectoriel avec NumPy
    print("Calcul vectoriel avec NumPy en cours...")
    temps_debut_np = time.perf_counter()
    somme_totale_np = np.sin(vecteur_np).sum()
    temps_fin_np = time.perf_counter()
    temps_np = temps_fin_np - temps_debut_np

    print(f"Temps avec NumPy: {temps_np:.4f} secondes.")
    print(f"Le temps avec NumPy est ~{int(temps_seq / temps_np)} fois plus rapide que la version séquentielle.")
    print(
        "Explication: NumPy utilise des instructions SIMD optimisées pour calculer le sinus sur des paquets de données, ce qui est extrêmement rapide.")

    # Affichage des sommes pour vérification
    print("\n--- Vérification des résultats ---")
    # Utilisation d'une tolérance pour les comparaisons des sommes en virgule flottante
    print(f"Somme séquentielle : {somme_totale_sequentielle}")
    print(f"Somme avec threads : {somme_totale_thread}")
    print(f"Somme avec NumPy   : {somme_totale_np}")


if __name__ == "__main__":
    executer_comparaison()
