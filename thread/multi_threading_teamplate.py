import threading
import time
import random


def tache_io_bound(identifiant):
    """Tâche typique de multithreading : attend une ressource externe (I/O)."""
    print(f"Thread {identifiant}: Démarre la tâche I/O...")
    time.sleep(2)  # Simule une opération qui attend (ex: requête réseau, lecture de fichier)
    print(f"Thread {identifiant}: Termine la tâche I/O.")


def calculer_somme(liste_a_traiter, resultat, index):
    """Tâche CPU-bound : calcule la somme d'une sous-liste."""
    somme_partielle = sum(liste_a_traiter)
    resultat[index] = somme_partielle
    print(f"Thread {index}: Calcul de la somme partielle terminé.")


def executer_multithreading_io():
    """Exemple I/O-bound : Utilisation efficace du multithreading."""
    print("--- Démonstration I/O-bound ---")
    threads = []
    temps_debut = time.perf_counter()

    for i in range(4):
        thread = threading.Thread(target=tache_io_bound, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    temps_fin = time.perf_counter()
    print(f"Temps total pour 4 threads I/O-bound: {temps_fin - temps_debut:.4f} secondes.\n")


def executer_multithreading_cpu():
    """Exemple CPU-bound : Démonstration de l'effet du GIL."""
    print("--- Démonstration CPU-bound et l'effet du GIL ---")

    # Génération d'un grand tableau de données
    taille_vecteur = 100_000_000
    vecteur = [random.randint(0, 10) for _ in range(taille_vecteur)]

    # 1. Calcul Séquentiel
    print("Calcul séquentiel en cours...")
    temps_debut_seq = time.perf_counter()
    somme_totale_sequentielle = sum(vecteur)
    temps_fin_seq = time.perf_counter()
    temps_seq = temps_fin_seq - temps_debut_seq
    print(f"Somme séquentielle: {somme_totale_sequentielle}")
    print(f"Temps séquentiel: {temps_seq:.4f} secondes.\n")

    # 2. Calcul avec Multithreading (4 threads)
    print("Calcul avec 4 threads en cours...")
    nb_threads = 4
    threads = []
    resultats_partiels = [0] * nb_threads

    # Diviser le vecteur en 4 parties
    taille_partie = taille_vecteur // nb_threads

    temps_debut_thread = time.perf_counter()

    for i in range(nb_threads):
        debut = i * taille_partie
        fin = debut + taille_partie
        partie = vecteur[debut:fin]
        thread = threading.Thread(target=calculer_somme, args=(partie, resultats_partiels, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    somme_totale_thread = sum(resultats_partiels)
    temps_fin_thread = time.perf_counter()
    temps_thread = temps_fin_thread - temps_debut_thread

    print(f"Somme avec 4 threads: {somme_totale_thread}")
    print(f"Temps avec 4 threads: {temps_thread:.4f} secondes.")
    print(
        f"Le temps avec des threads est {'plus long' if temps_thread > temps_seq else 'similaire' if abs(temps_thread - temps_seq) < 0.1 else 'plus court'} que le temps séquentiel.")

    # Affichage du GIL
    print(f"Remarque: Le GIL (Global Interpreter Lock) limite le parallélisme de cette tâche CPU-bound.")
    print(
        "Le temps d'exécution avec 4 threads n'est pas significativement meilleur, voire pire, que la version séquentielle en raison du surcoût de la gestion des threads et de la limitation du GIL qui ne permet qu'un seul thread Python de s'exécuter à la fois.")


if __name__ == "__main__":
    executer_multithreading_io()
    executer_multithreading_cpu()
