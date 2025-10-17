#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Évaluateur de script brute-force pour la recherche pondérée sur graphe.

Usage
-----
python evaluate_bruteforce.py <script_path> <points.csv> <queries.csv> <candidate_output.csv> <reference.csv> [--report report.csv]

- <script_path>         : chemin du script à évaluer (ex: brute_force_search.py)
- <points.csv>          : fichier des nœuds (node_id, feature_1..feature_50)
- <queries.csv>         : fichier des requêtes (avec A_vector/Y_vector/D)
- <candidate_output.csv>: chemin où le script évalué écrira sa sortie
- <reference.csv>       : fichier de référence (vérité terrain) au même format que la sortie
- --report              : (optionnel) CSV détaillé par requête (comparaison des volumes)

La métrique 'correctness' est la moyenne, sur les requêtes, de:
    correctness_q = min(num_matches_candidat, num_matches_reference) / max(1, num_matches_reference)

NB: on borne à 100% si le candidat retourne plus de nœuds que la référence.
Le temps de calcul mesure le temps d'exécution du script évalué (mur), hors parsing/évaluation.
"""
import argparse
import os
import sys
import subprocess
import time
from typing import Tuple

import pandas as pd

REQUIRED_OUT_COLS = ["query_id", "D", "num_matches", "nodes", "nodes_with_distance"]

def run_candidate(script_path: str, points_csv: str, queries_csv: str, candidate_out: str) -> Tuple[float, str, str]:
    """Lance le script candidat et mesure le temps d'exécution mur (en secondes).
    Retourne (elapsed_s, stdout, stderr).
    """
    # Supprime un éventuel ancien fichier de sortie pour éviter les confusions
    try:
        if os.path.exists(candidate_out):
            os.remove(candidate_out)
    except Exception:
        pass

    cmd = [sys.executable, script_path, points_csv, queries_csv, candidate_out]

    t0 = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    t1 = time.perf_counter()

    return t1 - t0, proc.stdout, proc.stderr

def load_output_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier non trouvé: {path}")
    df = pd.read_csv(path)
    # Vérifications minimales
    missing = [c for c in ["query_id", "num_matches"] if c not in df.columns]
    if missing:
        raise KeyError(f"Colonnes manquantes dans {path}: {missing}. Colonnes attendues: {REQUIRED_OUT_COLS}")
    # Normalisation
    df["query_id"] = df["query_id"].astype(str)
    df["num_matches"] = pd.to_numeric(df["num_matches"], errors="coerce").fillna(0).astype(int)
    return df[["query_id", "num_matches"]].copy()

def evaluate(candidate_df: pd.DataFrame, reference_df: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    """Compare le nombre de nœuds par requête. Retourne (df_details, correctness_moyenne).
    - df_details: query_id, num_ref, num_pred, correctness (0..1)
    - correctness_moyenne: moyenne sur toutes les requêtes de référence
    Les requêtes présentes dans la référence et absentes chez le candidat valent 0.
    """
    ref = reference_df.copy()
    pred = candidate_df.copy()

    # Jointure sur les requêtes de référence
    details = ref.merge(pred, on="query_id", how="left", suffixes=("_ref", "_pred"))
    details["num_matches_pred"].fillna(0, inplace=True)
    details["num_matches_pred"] = details["num_matches_pred"].astype(int)

    # correctness par requête (bornée à 1.0)
    # Evite division par zéro si la référence contient 0 (on définit alors correctness=1 si pred=0, sinon 0)
    def corr_row(row):
        n_ref = int(row["num_matches_ref"])
        n_pred = int(row["num_matches_pred"])
        if n_ref <= 0:
            return 1.0 if n_pred == 0 else 0.0
        return min(n_pred / n_ref, 1.0)

    details["correctness"] = details.apply(corr_row, axis=1)

    mean_correctness = float(details["correctness"].mean()) if len(details) else 0.0

    # Renomme colonnes pour lisibilité finale
    details = details.rename(columns={
        "num_matches_ref": "num_ref",
        "num_matches_pred": "num_pred"
    })[["query_id", "num_ref", "num_pred", "correctness"]]

    return details, mean_correctness

def main():
    ap = argparse.ArgumentParser(description="Évalue un script brute-force sur la base d'un CSV de référence.")
    ap.add_argument("script_path", type=str, help="Chemin du script candidat (ex: brute_force_search.py)")
    ap.add_argument("points_csv", type=str, help="Fichier des nœuds")
    ap.add_argument("queries_csv", type=str, help="Fichier des requêtes")
    ap.add_argument("candidate_output", type=str, help="Chemin de sortie où le candidat écrira ses résultats")
    ap.add_argument("reference_csv", type=str, help="Fichier de référence (vérité terrain)")
    ap.add_argument("--report", type=str, default=None, help="Chemin d'export CSV détaillé par requête")
    args = ap.parse_args()

    # 1) Exécuter le candidat et mesurer le temps
    elapsed, out, err = run_candidate(args.script_path, args.points_csv, args.queries_csv, args.candidate_output)

    # 2) Charger la sortie candidat et la référence
    cand_df = load_output_csv(args.candidate_output)
    ref_df = load_output_csv(args.reference_csv)

    # 3) Évaluer
    details, mean_corr = evaluate(cand_df, ref_df)

    # 4) Enregistrer le report si demandé
    if args.report:
        details.to_csv(args.report, index=False)

    # 5) Afficher un résumé clair
    total_q = len(ref_df)
    exact = int((details["num_ref"] == details["num_pred"]).sum())
    print("\\n===== Résumé de l'évaluation =====")
    print(f"Requêtes (référence): {total_q}")
    print(f"Temps d'exécution (script candidat): {elapsed:.3f} s")
    print(f"Exact match (num_ref == num_pred): {exact}/{total_q} ({(exact/total_q*100 if total_q else 0):.1f}%)")
    print(f"Correctness moyenne (0..1): {mean_corr:.4f}  -> {(mean_corr*100):.2f}%")

    if out.strip():
        print("\\n--- STDOUT candidat ---\\n" + out.strip())
    if err.strip():
        print("\\n--- STDERR candidat ---\\n" + err.strip())

if __name__ == "__main__":
    main()
