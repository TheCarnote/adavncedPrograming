#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Benchmark race condition (multiprocessing + variable globale partagée) avec micro-travail avant l'incrément.
Scénarios:
  1) 1 seul processus (baseline, pas de concurrence)
  2) N processus SANS protection (race condition)
  3) N processus AVEC protection (Lock)
Mesure: temps, correctitude, pertes, débit.
Le "travail" est simulé par:
  - un très court sleep (mode 'sleep'), ou
  - une boucle active (mode 'busy') d'une durée ~work_us microsecondes.
"""

import time
import argparse
import multiprocessing as mp
from ctypes import c_longlong

# --- Variables globales partagées (références assignées dans chaque process) ---
COUNTER = None  # multiprocessing.Value(c_longlong, ...)
LOCK = None     # multiprocessing.Lock() ou None


def _init_globals(counter_ref, lock_ref):
    """Initialise les variables globales dans le *processus enfant*."""
    global COUNTER, LOCK
    COUNTER = counter_ref
    LOCK = lock_ref


def _do_work(work_us: int, work_mode: str):
    """
    Simule un petit travail avant l'incrément:
      - sleep: cède le CPU pendant ~work_us µs (la précision réelle dépend de l'OS)
      - busy: boucle active pendant ~work_us µs (plus fidèle pour 10 µs, mais CPU-bound)
    """
    if work_us <= 0:
        return
    if work_mode == "sleep":
        # Note: la granularité de time.sleep peut être ~1 ms ou plus selon OS.
        time.sleep(work_us / 1_000_000.0)
    else:
        # Boucle active approximative (meilleure précision µs)
        t_end = time.perf_counter() + (work_us / 1_000_000.0)
        while time.perf_counter() < t_end:
            pass


def _worker(iters: int, use_lock: bool, yield_every: int, work_us: int, work_mode: str):
    """Boucle d'incréments; utilise les globals COUNTER / LOCK, et simule un micro-travail avant chaque incrément."""
    global COUNTER, LOCK
    for k in range(iters):
        _do_work(work_us, work_mode)

        if use_lock and LOCK is not None:
            # Section critique protégée : atomique via Lock explicite
            with LOCK:
                COUNTER.value += 1
        else:
            # SANS protection : RMW non atomique -> pertes probables
            COUNTER.value += 1

        # (Optionnel) accentuer les interleavings
        if yield_every and (k % yield_every == 0):
            time.sleep(0)


def process_entry(iters: int, use_lock: bool, yield_every: int,
                  work_us: int, work_mode: str, counter_ref, lock_ref):
    """
    Point d'entrée top-level (picklable) pour mp.Process.
    Initialise les globals, puis lance la boucle worker.
    """
    _init_globals(counter_ref, lock_ref)
    _worker(iters, use_lock, yield_every, work_us, work_mode)


def run_single(total_ops: int, work_us: int, work_mode: str):
    """Scénario 1 : séquentiel (aucune concurrence), avec micro-travail avant chaque incrément."""
    local = 0
    t0 = time.perf_counter()
    for _ in range(total_ops):
        _do_work(work_us, work_mode)
        local += 1
    dt = time.perf_counter() - t0

    expected = total_ops
    final = local
    ok = (final == expected)
    lost = expected - final
    thr = expected / dt if dt > 0 else float("inf")
    return {
        "name": f"Séquentiel (1 processus, {work_us} µs/{work_mode})",
        "time": dt, "final": final, "expected": expected,
        "ok": ok, "lost": lost, "throughput": thr
    }


def run_processes(n_procs: int, iters_per_proc: int, protect: bool,
                  yield_every: int, work_us: int, work_mode: str):
    """Scénarios 2 & 3 : concurrence par processus avec variable globale partagée."""
    # IMPORTANT: Value(lock=False) pour ne pas confondre avec un verrou interne implicite.
    counter = mp.Value(c_longlong, 0, lock=False)
    lock = mp.Lock() if protect else None

    procs = [
        mp.Process(
            target=process_entry,
            args=(iters_per_proc, protect, yield_every, work_us, work_mode, counter, lock)
        )
        for _ in range(n_procs)
    ]

    t0 = time.perf_counter()
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    dt = time.perf_counter() - t0

    expected = n_procs * iters_per_proc
    final = counter.value
    ok = (final == expected)
    lost = expected - final
    thr = expected / dt if dt > 0 else float("inf")

    label = ("Processus SANS protection" if not protect
             else "Processus AVEC protection (Lock)")
    return {
        "name": f"{label} ({work_us} µs/{work_mode})",
        "time": dt, "final": final, "expected": expected,
        "ok": ok, "lost": lost, "throughput": thr
    }


def print_result(res: dict):
    verdict = "OK" if res["ok"] else "INCORRECT"
    print(f"\n=== {res['name']} ===")
    print(f"Résultat final : {res['final']:,} / Attendu : {res['expected']:,} -> {verdict}")
    if not res["ok"]:
        print(f"Mises à jour perdues : {res['lost']:,} "
              f"({res['lost']/res['expected']*100:.2f}% d'erreur)")
    print(f"Temps écoulé : {res['time']:.6f} s")
    print(f"Débit (ops/s) : {res['throughput']:,.0f}")


def main():
    parser = argparse.ArgumentParser(
        description="Race condition en multiprocessing avec variable globale partagée et micro-travail avant incrément."
    )
    parser.add_argument("--procs", type=int, default=max(2, mp.cpu_count() // 2),
                        help="Nombre de processus pour la concurrence (défaut: mi-CPU).")
    parser.add_argument("--ops", type=int, default=1_000_000,
                        help="Nombre total d'opérations (défaut: 1_000_000).")
    parser.add_argument("--yield-every", type=int, default=0,
                        help="time.sleep(0) toutes N itérations (0 pour désactiver).")
    parser.add_argument("--work-us", type=int, default=10,
                        help="Durée du micro-travail par itération, en microsecondes (défaut: 10).")
    parser.add_argument("--work-mode", choices=["sleep", "busy"], default="sleep",
                        help="Mode de micro-travail: 'sleep' (I/O-like) ou 'busy' (CPU-like). Défaut: sleep.")
    args = parser.parse_args()

    n_procs = args.procs
    total_ops = args.ops
    iters_per_proc = total_ops // n_procs
    yield_every = args.yield_every
    work_us = args.work_us
    work_mode = args.work_mode

    # 1) Baseline : 1 processus (avec le même micro-travail)
    res1 = run_single(total_ops, work_us, work_mode)
    print_result(res1)

    # 2) Concurrence SANS protection
    res2 = run_processes(n_procs, iters_per_proc, protect=False,
                         yield_every=yield_every, work_us=work_us, work_mode=work_mode)
    print_result(res2)

    # 3) Concurrence AVEC protection (Lock)
    res3 = run_processes(n_procs, iters_per_proc, protect=True,
                         yield_every=yield_every, work_us=work_us, work_mode=work_mode)
    print_result(res3)

    # Récapitulatif
    print("\n=== Récapitulatif ===")
    for r in (res1, res2, res3):
        status = "OK" if r["ok"] else f"INCORRECT (pertes: {r['lost']:,})"
        print(f"- {r['name']:<55} : {status:25} | {r['time']:.4f} s | {r['throughput']:,.0f} ops/s")


if __name__ == "__main__":
    # Sur macOS/Windows, le start method par défaut est 'spawn'.
    # Garder la création des objets partagés à l'intérieur de main().
    main()
