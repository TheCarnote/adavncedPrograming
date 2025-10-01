import multiprocessing
import time
import random
import numpy as np
import math
import matplotlib

matplotlib.use('TkAgg')  # ou 'Qt5Agg' selon ton setup
import matplotlib.pyplot as plt

# Constantes globales
ELEMENTS_PAR_CALCUL = 10000
NB_BLOCS = 1000  # nombre de blocs de calcul
TAILLE_VECTEUR_TOTAL = ELEMENTS_PAR_CALCUL * NB_BLOCS
PROCESSUS_A_TESTER = [1, 2, 4, 8, 12, 16]


# =====================
# Méthodes de calcul
# =====================

def calculer_somme_sin_complexe_multiprocess(partie):
    """Méthode de base avec math.sin (boucle Python)"""
    resultat_partiel = []
    partie_np = np.array(partie, dtype=np.float64)
    for i in range(0, len(partie_np), ELEMENTS_PAR_CALCUL):
        somme = 0
        for x in partie_np[i: i + ELEMENTS_PAR_CALCUL]:
            somme += math.sin(x)
        resultat_partiel.append(somme)
    return resultat_partiel


def calculer_somme_numpy_multiprocess(partie):
    """Méthode NumPy vectorisée"""
    partie_np = np.array(partie, dtype=np.float64)
    sin_partie = np.sin(partie_np)

    taille_valide = (len(sin_partie) // ELEMENTS_PAR_CALCUL) * ELEMENTS_PAR_CALCUL
    sin_partie = sin_partie[:taille_valide]
    reshaped_sin = sin_partie.reshape(-1, ELEMENTS_PAR_CALCUL)
    return list(np.sum(reshaped_sin, axis=1))


def copilote_accelerated(partie):
    """Simulation d'une accélération vectorielle (type GPU)"""
    partie_np = np.array(partie, dtype=np.float64)
    return [np.sum(np.sin(partie_np))]


# === Bilelos accelerated : LUT entiers 0–100 ===
LUT_INT = np.sin(np.arange(0, 101))  # LUT de 101 valeurs en cache L1


def bilelos_accelerated_int(partie):
    resultat = []
    partie_np = np.array(partie, dtype=np.int32)  # valeurs entières [0..100]
    for i in range(0, len(partie_np), ELEMENTS_PAR_CALCUL):
        sous_vecteur = partie_np[i:i + ELEMENTS_PAR_CALCUL]
        somme = np.sum(LUT_INT[sous_vecteur])  # lookup direct
        resultat.append(somme)
    return resultat


# === Claude Optimized : LUT + vectorisation numpy avancée ===
LUT_CLAUDE = np.sin(np.arange(0, 101))  # Même LUT


def claude_optimized(partie):
    """
    Approche Claude : LUT + vectorisation numpy complète
    - Conversion directe en numpy array d'entiers
    - Lookup vectorisé sur tout le tableau
    - Reshape et sum vectorisés
    """
    partie_np = np.array(partie, dtype=np.int32)

    # Lookup vectorisé : remplace tous les indices d'un coup
    sin_values = LUT_CLAUDE[partie_np]

    # Calcul par blocs de manière vectorisée
    taille_valide = (len(sin_values) // ELEMENTS_PAR_CALCUL) * ELEMENTS_PAR_CALCUL
    sin_values = sin_values[:taille_valide]
    reshaped = sin_values.reshape(-1, ELEMENTS_PAR_CALCUL)

    # Retour direct d'un array numpy (plus rapide que list())
    return np.sum(reshaped, axis=1).tolist()


# =====================
# Bench multiprocessing
# =====================

def executer_multiprocessing_tests(vecteur, methode="pur"):
    temps_par_process = []
    print(f"\n--- Tests Multiprocessing [{methode}] ---")

    if methode == "pur":
        func = calculer_somme_sin_complexe_multiprocess
    elif methode == "numpy":
        func = calculer_somme_numpy_multiprocess
    elif methode == "copilote":
        func = copilote_accelerated
    elif methode == "bilelos":
        func = bilelos_accelerated_int
    elif methode == "claude":
        func = claude_optimized
    else:
        raise ValueError("Méthode inconnue")

    for nb_process in PROCESSUS_A_TESTER:
        print(f"  > Exécution avec {nb_process} processus...")
        temps_debut = time.perf_counter()

        taille_partie = len(vecteur) // nb_process
        parties = [vecteur[i * taille_partie:(i + 1) * taille_partie] for i in range(nb_process)]

        with multiprocessing.Pool(processes=nb_process) as pool:
            resultats_partiels = pool.map(func, parties)

        resultat_final = sum(sum(res) for res in resultats_partiels)
        temps_fin = time.perf_counter()
        temps_total = temps_fin - temps_debut
        temps_par_process.append(temps_total)
        print(f"    Temps total: {temps_total:.4f} sec.")

    return temps_par_process


# =====================
# Génération du graphique
# =====================

def generer_plot(resultats_dict):
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(14, 8))

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    markers = ['o', 's', '^', 'D', 'v']

    for idx, (label, resultats) in enumerate(resultats_dict.items()):
        plt.plot(PROCESSUS_A_TESTER, resultats,
                 marker=markers[idx],
                 linestyle='-',
                 linewidth=2.5,
                 markersize=8,
                 color=colors[idx],
                 label=label)

    plt.title('Performance vs. Nombre de Processus\nComparaison des Méthodes de Calcul sin(x)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Nombre de processus', fontsize=13, fontweight='bold')
    plt.ylabel('Temps d\'exécution (secondes)', fontsize=13, fontweight='bold')
    plt.xticks(PROCESSUS_A_TESTER, fontsize=11)
    plt.yticks(fontsize=11)
    plt.legend(fontsize=11, loc='best', framealpha=0.9)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("performance.png", dpi=150)
    plt.show()


# =====================
# Main
# =====================

if __name__ == "__main__":
    print("=" * 60)
    print(" BENCHMARK MULTIPROCESSING - BATTLE ROYALE ")
    print("=" * 60)
    print(f"Taille du vecteur : {TAILLE_VECTEUR_TOTAL:,} éléments")
    print(f"Processus testés : {PROCESSUS_A_TESTER}")
    print("=" * 60)

    print("\n️  Génération des données...")
    vecteur_py = [random.randint(0, 100) for _ in range(TAILLE_VECTEUR_TOTAL)]
    print(" Données générées.\n")

    resultats_pure = executer_multiprocessing_tests(vecteur_py, methode="pur")
    resultats_numpy = executer_multiprocessing_tests(vecteur_py, methode="numpy")
    resultats_copilote = executer_multiprocessing_tests(vecteur_py, methode="copilote")
    resultats_bilelos = executer_multiprocessing_tests(vecteur_py, methode="bilelos")
    resultats_claude = executer_multiprocessing_tests(vecteur_py, methode="claude")

    resultats_dict = {
        "Multiprocessing Pur": resultats_pure,
        "Multiprocessing + NumPy": resultats_numpy,
        "Copilote Accelerated": resultats_copilote,
        "Bilelos Accelerated (LUT 0-100)": resultats_bilelos,
        "Claude Optimized 🚀": resultats_claude,
    }

    print("\n" + "=" * 60)
    print(" RÉSULTATS FINAUX")
    print("=" * 60)
    for nom, temps in resultats_dict.items():
        print(f"{nom:35s} | Meilleur temps : {min(temps):.4f}s")
    print("=" * 60)

    generer_plot(resultats_dict)
