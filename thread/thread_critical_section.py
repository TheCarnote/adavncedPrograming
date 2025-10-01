import threading
import time

# Variable globale partagée
compteur = 0
# Verrou pour la synchronisation
verrou = threading.Lock()

# On augmente le nombre d'incréments par thread pour augmenter la charge
NB_INCREMENTS = 500_000


def tache_sans_verrou():
    """
    Incrémente le compteur global sans verrou.
    Ajoute un petit calcul pour augmenter la probabilité de race condition.
    """
    global compteur
    for _ in range(NB_INCREMENTS):
        # Lecture
        valeur_temp = compteur
        # Calcul
        valeur_temp += 1
        # Ajout d'une petite "pause" pour garantir un changement de contexte
        # C'est une astuce, mais cela simule une opération plus longue
        # (valeur_temp / 1000) * (valeur_temp / 1000)

        # Ecriture
        compteur = valeur_temp


def tache_avec_verrou():
    """
    Incrémente le compteur global en utilisant un verrou.
    """
    global compteur
    for _ in range(NB_INCREMENTS):
        with verrou:
            # L'opération est rendue atomique par le verrou
            compteur += 1


def executer_threads(fonction_tache, titre):
    """
    Fonction utilitaire pour lancer des threads et mesurer le temps.
    """
    global compteur
    compteur = 0
    threads = []

    print(f"\n--- {titre} ---")
    temps_debut = time.perf_counter()

    # On va tester avec un nombre de threads plus grand
    NB_THREADS = 8

    # Crée et lance les threads
    for _ in range(NB_THREADS):
        thread = threading.Thread(target=fonction_tache)
        threads.append(thread)
        thread.start()

    # Attend la fin de tous les threads
    for thread in threads:
        thread.join()

    temps_fin = time.perf_counter()
    temps_total = temps_fin - temps_debut

    valeur_attendue = NB_THREADS * NB_INCREMENTS

    print(f"Temps total: {temps_total:.4f} secondes.")
    print(f"Valeur finale du compteur: {compteur}")
    print(f"Valeur attendue: {valeur_attendue}")

    if compteur == valeur_attendue:
        print("Le résultat est correct.")
    else:
        print(f"Le résultat est INCORRECT. Écart: {valeur_attendue - compteur}. Une race condition s'est produite. 🐍")


if __name__ == "__main__":
    # Exécution du test SANS verrou
    executer_threads(tache_sans_verrou, "Démonstration de la race condition (SANS VERROU)")

    # Exécution du test AVEC verrou
    executer_threads(tache_avec_verrou, "Démonstration de la solution (AVEC VERROU)")
