import random
import time
import string
import hashlib
import json
from collections import defaultdict
from typing import Iterable, Hashable, Tuple, List, Dict, Set, Any
import collections


# --- Fonctions à tester (TODO: Implémentez vos solutions ici) ---

def partition_par_unions_naive(
        elements: Iterable[Hashable],
        relations: Iterable[Tuple[Hashable, Hashable]]
) -> List[List[Hashable]]:
    """
    Implémentation vraiment naïve (brute force) n'utilisant que des listes.
    La recherche d'un élément se fait par balayage de la liste de groupes.
    """
    # Étape 1 : Initialisation
    partition = [[elem] for elem in elements]

    # Créer une liste pour vérifier rapidement si un élément existe
    elements_set = set(elements)

    # Étape 2 : Parcourir les relations et effectuer les fusions
    for x, y in relations:
        # Vérifier l'existence des éléments
        if x not in elements_set or y not in elements_set:
            continue

        group_x = None
        group_y = None

        # Trouver les groupes de x et y par balayage (recherche lente)
        for group in partition:
            if x in group:
                group_x = group
            if y in group:
                group_y = group
            # On peut optimiser la boucle en sortant plus tôt si les deux sont trouvés
            if group_x and group_y:
                break

        # S'assurer que les deux éléments sont trouvés (devrait toujours l'être)
        if group_x is None or group_y is None:
            continue

        # Étape 3 : Fusionner si les groupes sont différents
        if group_x is not group_y:
            group_x.extend(group_y)
            # Retirer le groupe fusionné de la partition
            partition.remove(group_y)

    # Étape 4 : Retourner la partition finale
    return partition


# Les 5 fonctions "placeholders" demandées
def partition_par_unions_1(
        elements: Iterable[Hashable],
        relations: Iterable[Tuple[Hashable, Hashable]]
) -> List[List[Hashable]]:
    """TODO: implémentez votre première solution ici."""
    """
       Implémentation académique utilisant des sets.
       """
    """
    Implémentation corrigée utilisant des sets avec mapping direct vers les sets.
    """
    elements = list(elements)
    elements_set = set(elements)

    # Chaque élément pointe vers son set actuel
    elem_to_group = {}
    groups = []

    # Initialisation: chaque élément dans son propre groupe
    for elem in elements:
        group = {elem}
        groups.append(group)
        elem_to_group[elem] = group

    for x, y in relations:
        if x not in elements_set or y not in elements_set:
            continue

        group_x = elem_to_group[x]
        group_y = elem_to_group[y]

        if group_x is not group_y:
            # Fusionner group_y dans group_x (le plus grand)
            if len(group_y) > len(group_x):
                group_x, group_y = group_y, group_x

            group_x.update(group_y)

            # Mettre à jour toutes les références vers group_y
            for elem in group_y:
                elem_to_group[elem] = group_x

            # Retirer group_y de la liste des groupes
            groups.remove(group_y)

    return [list(group) for group in groups]

def partition_par_unions_2(
        elements: Iterable[Hashable],
        relations: Iterable[Tuple[Hashable, Hashable]]
) -> List[List[Hashable]]:
    """TODO: implémentez votre deuxième solution ici."""
    """
    Implémentation corrigée utilisant un dictionnaire pour mapper vers les représentants.
    """
    elements = list(elements)
    elements_set = set(elements)

    # Chaque élément est son propre représentant au début
    representative = {elem: elem for elem in elements}
    groups = {elem: [elem] for elem in elements}

    def find_representative(x):
        """Trouve le représentant du groupe contenant x."""
        return representative[x]

    def union(x, y):
        """Fusionne les groupes contenant x et y."""
        rep_x = find_representative(x)
        rep_y = find_representative(y)

        if rep_x == rep_y:
            return

        # Fusionner le plus petit groupe dans le plus grand
        group_x = groups[rep_x]
        group_y = groups[rep_y]

        if len(group_y) > len(group_x):
            rep_x, rep_y = rep_y, rep_x
            group_x, group_y = group_y, group_x

        # Ajouter tous les éléments de group_y à group_x
        group_x.extend(group_y)

        # Mettre à jour le représentant de tous les éléments de group_y
        for elem in group_y:
            representative[elem] = rep_x

        # Supprimer l'ancien groupe
        del groups[rep_y]

    for x, y in relations:
        if x in elements_set and y in elements_set:
            union(x, y)

    return list(groups.values())


def partition_par_unions_3(
        elements: Iterable[Hashable],
        relations: Iterable[Tuple[Hashable, Hashable]]
) -> List[List[Hashable]]:
    """
        Union-Find (Weighted Quick-Union) :
        - Union par taille (attache l'arbre le plus petit au plus grand)
        - PAS de compression de chemin (volontairement, pour rester "optimisé mais pas au max")

        Complexité (amortie) : ~ O(m log n)
          - n = nombre d'éléments
          - m = nombre de relations valides (dont les deux extrémités ∈ elements)

        Politique :
          - Ignore toute relation (x, y) si x ou y n'appartient pas à `elements`.
          - Retourne une liste de listes (ordre indéterminé, ce qui convient à compare_results).
        """

    # Matériel de base
    elements = list(elements)
    elements_set = set(elements)

    # Parent et taille des composantes (représentation par racines)
    parent: Dict[Hashable, Hashable] = {e: e for e in elements}
    size: Dict[Hashable, int] = {e: 1 for e in elements}

    def find(x: Hashable) -> Hashable:
        """Trouve la racine de x (sans compression de chemin)."""
        # x est supposé ∈ elements_set avant l'appel
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: Hashable, y: Hashable) -> None:
        """Fusionne les composantes contenant x et y en utilisant l'union par taille."""
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        # Attache le plus petit au plus grand
        if size[rx] < size[ry]:
            parent[rx] = ry
            size[ry] += size[rx]
        else:
            parent[ry] = rx
            size[rx] += size[ry]

    # Appliquer les relations (en ignorant celles hors domaine)
    for (x, y) in relations:
        if (x in elements_set) and (y in elements_set):
            union(x, y)

    # Rassembler les groupes par racine
    groups: Dict[Hashable, List[Hashable]] = {}
    for e in elements:
        r = find(e)  # sans compression pour rester cohérent avec le choix de l'algo
        if r not in groups:
            groups[r] = []
        groups[r].append(e)

    return list(groups.values())


def partition_par_unions_4(
        elements: Iterable[Hashable],
        relations: Iterable[Tuple[Hashable, Hashable]]
) -> List[List[Hashable]]:
    """
        Union-Find avec compression de chemin ET union par rang.
        Complexité amortie: O(α(n)) par opération, où α est l'inverse d'Ackermann.
        """
    elements = list(elements)
    elements_set = set(elements)

    parent = {elem: elem for elem in elements}
    rank = {elem: 0 for elem in elements}

    def find(x):
        """Trouve la racine avec compression de chemin."""
        if parent[x] != x:
            parent[x] = find(parent[x])  # Compression de chemin
        return parent[x]

    def union(x, y):
        """Union par rang."""
        root_x = find(x)
        root_y = find(y)

        if root_x == root_y:
            return

        # Union par rang: attacher le plus petit au plus grand
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1

    # Traiter toutes les relations
    for x, y in relations:
        if x in elements_set and y in elements_set:
            union(x, y)

    # Construire les groupes finaux
    groups = {}
    for elem in elements:
        root = find(elem)
        if root not in groups:
            groups[root] = []
        groups[root].append(elem)

    return list(groups.values())


def partition_par_unions_5(
        elements: Iterable[Hashable],
        relations: Iterable[Tuple[Hashable, Hashable]]
) -> List[List[Hashable]]:
    """
        Approche basée sur les graphes avec DFS pour trouver les composantes connexes.
        """
    elements = list(elements)
    elements_set = set(elements)

    # Construire le graphe d'adjacence
    graph = {elem: set() for elem in elements}

    for x, y in relations:
        if x in elements_set and y in elements_set:
            graph[x].add(y)
            graph[y].add(x)

    visited = set()
    groups = []

    def dfs(node, current_group):
        """DFS pour explorer une composante connexe."""
        if node in visited:
            return
        visited.add(node)
        current_group.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, current_group)

    # Trouver toutes les composantes connexes
    for elem in elements:
        if elem not in visited:
            group = []
            dfs(elem, group)
            groups.append(group)

    return groups


# --- Fonctions utilitaires pour la génération de données et la comparaison ---

def generate_random_chars(length: int = 4) -> str:
    """Génère une chaîne de caractères aléatoires lisibles."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_test_data(n_elements: int, n_relations: int) -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    Génère des éléments et des relations de test selon les spécifications.
    Les éléments générés sont garantis d'être uniques.
    """
    print(f"Génération des données : {n_elements} éléments, {n_relations} relations.")

    # Utiliser un set pour garantir l'unicité des éléments
    unique_elements = set()
    while len(unique_elements) < n_elements:
        unique_elements.add(generate_random_chars())
    elements = list(unique_elements)

    relations = []

    n_valid_relations = n_relations // 2
    if n_elements < 2:
        n_valid_relations = 0

    # Créer les relations valides à partir des éléments uniques
    for _ in range(n_valid_relations):
        x, y = random.sample(elements, 2)
        relations.append((x, y))

    # Créer les relations aléatoires
    n_random_relations = n_relations - n_valid_relations
    for _ in range(n_random_relations):
        x = generate_random_chars()
        y = generate_random_chars()
        relations.append((x, y))

    random.shuffle(relations)
    return elements, relations


def compare_results(result1: List[List[Hashable]], result2: List[List[Hashable]]) -> bool:
    """Compare deux partitions de groupes, indépendamment de l'ordre."""

    def normalize_partition(partition):
        return sorted([tuple(sorted(group)) for group in partition])

    try:
        return normalize_partition(result1) == normalize_partition(result2)
    except Exception as e:
        print(f"Erreur lors de la normalisation des résultats : {e}")
        return False


def run_tests(
        implementations: Dict[str, callable],
        n_elements_list: List[int],
        n_relations_factors: List[float]
) -> None:
    """
    Exécute les tests de performance et de validité.
    """
    print("🚀 Début des tests de performance et de validité.")
    print("-" * 50)

    for i, n_elements in enumerate(n_elements_list):
        for j, factor in enumerate(n_relations_factors):
            # Correction ici pour le calcul du nombre de relations
            if factor == 1000:
                n_relations = 1000
            else:
                n_relations = max(1000, int(n_elements * factor)) if n_elements > 0 else 1000

            elements, relations = generate_test_data(n_elements, n_relations)

            print(f"\n🧪 Test {i + 1}.{j + 1} : {n_elements} éléments, {n_relations} relations")

            print("  -> Exécution de la référence (naïve)... ", end="")
            start_time = time.time()
            ref_result = partition_par_unions_naive(elements, relations)
            end_time = time.time()
            print(f"Terminé en {end_time - start_time:.4f}s")

            for name, func in implementations.items():
                print(f"  -> Exécution de '{name}'... ", end="")
                try:
                    start_time = time.time()
                    current_result = func(elements, relations)
                    end_time = time.time()
                    duration = end_time - start_time

                    is_correct = compare_results(ref_result, current_result)
                    status = "✅ Correct" if is_correct else "❌ Erreur"
                    print(f"Terminé en {duration:.4f}s ({status})")

                    if not is_correct:
                        print(f"     Les résultats de '{name}' sont incorrects pour ce test.")
                except Exception as e:
                    print(f"Erreur lors de l'exécution de '{name}': {e}")

            print("-" * 50)

    print("\n✅ Tous les tests sont terminés.")

#--------

def hash_partition(partition: List[List[Any]]) -> str:
    """Crée un hash unique pour une partition, indépendamment de l'ordre."""
    try:
        # Normaliser: trier chaque groupe et trier les groupes
        normalized = sorted([tuple(sorted(group)) for group in partition])
        # Créer un hash reproductible
        return hashlib.md5(str(normalized).encode()).hexdigest()[:8]
    except Exception as e:
        return f"ERROR_{str(e)[:8]}"


def analyze_partition(partition: List[List[Any]], name: str) -> Dict[str, Any]:
    """Analyse détaillée d'une partition."""
    try:
        # Statistiques de base
        num_groups = len(partition)
        total_elements = sum(len(group) for group in partition)
        group_sizes = [len(group) for group in partition]

        # Vérifier la validité
        all_elements = set()
        has_duplicates = False
        empty_groups = 0

        for group in partition:
            if len(group) == 0:
                empty_groups += 1
            for elem in group:
                if elem in all_elements:
                    has_duplicates = True
                all_elements.add(elem)

        return {
            'name': name,
            'hash': hash_partition(partition),
            'num_groups': num_groups,
            'total_elements': total_elements,
            'group_sizes': sorted(group_sizes, reverse=True),
            'max_group_size': max(group_sizes) if group_sizes else 0,
            'min_group_size': min(group_sizes) if group_sizes else 0,
            'empty_groups': empty_groups,
            'has_duplicates': has_duplicates,
            'is_valid': not has_duplicates and empty_groups == 0,
            'partition': partition  # Pour debug si nécessaire
        }
    except Exception as e:
        return {
            'name': name,
            'error': str(e),
            'is_valid': False
        }


def detailed_comparison_analysis(
        elements: List[Any],
        relations: List[Tuple[Any, Any]],
        implementations: Dict[str, callable]
) -> Dict[str, Any]:
    """Analyse comparative détaillée de toutes les implémentations."""

    print(f"\n🔍 ANALYSE DÉTAILLÉE")
    print(f"📊 Données: {len(elements)} éléments, {len(relations)} relations")
    print(f"🔗 Relations valides: {sum(1 for x, y in relations if x in set(elements) and y in set(elements))}")
    print("=" * 60)

    results = {}
    analyses = []

    # Exécuter toutes les implémentations
    for name, func in implementations.items():
        try:
            start_time = time.time()
            result = func(elements, relations)
            duration = time.time() - start_time

            analysis = analyze_partition(result, name)
            analysis['duration'] = duration
            analyses.append(analysis)
            results[name] = result

        except Exception as e:
            analyses.append({
                'name': name,
                'error': str(e),
                'is_valid': False,
                'duration': 0
            })

    # Grouper par hash (résultats identiques)
    hash_groups = defaultdict(list)
    for analysis in analyses:
        if 'hash' in analysis:
            hash_groups[analysis['hash']].append(analysis)

    # Afficher l'analyse
    print("\n📋 RÉSULTATS PAR IMPLÉMENTATION:")
    print("-" * 60)
    for analysis in sorted(analyses, key=lambda x: x.get('duration', 0)):
        name = analysis['name']
        if 'error' in analysis:
            print(f"❌ {name:15s} | ERREUR: {analysis['error']}")
        else:
            valid_icon = "✅" if analysis['is_valid'] else "❌"
            print(f"{valid_icon} {name:15s} | {analysis['duration']:.4f}s | "
                  f"Hash: {analysis['hash']} | "
                  f"Groupes: {analysis['num_groups']:4d} | "
                  f"Éléments: {analysis['total_elements']:5d}")

            if not analysis['is_valid']:
                issues = []
                if analysis['has_duplicates']:
                    issues.append("doublons")
                if analysis['empty_groups'] > 0:
                    issues.append(f"{analysis['empty_groups']} groupes vides")
                print(f"   └─ PROBLÈMES: {', '.join(issues)}")

    # Analyser les groupes de résultats identiques
    print(f"\n🎯 GROUPES DE RÉSULTATS IDENTIQUES:")
    print("-" * 60)

    consensus_found = False
    largest_group_size = 0
    largest_group_hash = None

    for hash_val, group in hash_groups.items():
        if len(group) > 1:  # Plus d'une implémentation avec le même résultat
            print(f"📦 Hash {hash_val} ({len(group)} implémentations):")
            for analysis in group:
                valid_icon = "✅" if analysis.get('is_valid', False) else "❌"
                print(f"   {valid_icon} {analysis['name']}")

            if len(group) > largest_group_size:
                largest_group_size = len(group)
                largest_group_hash = hash_val

            # Montrer les détails du premier résultat du groupe
            first = group[0]
            if 'group_sizes' in first:
                print(f"   └─ Détails: {first['num_groups']} groupes, "
                      f"tailles: {first['group_sizes'][:5]}{'...' if len(first['group_sizes']) > 5 else ''}")

    # Résultats uniques
    unique_results = [group[0] for group in hash_groups.values() if len(group) == 1]
    if unique_results:
        print(f"\n🔸 RÉSULTATS UNIQUES ({len(unique_results)}):")
        for analysis in unique_results:
            valid_icon = "✅" if analysis.get('is_valid', False) else "❌"
            print(f"   {valid_icon} {analysis['name']} (Hash: {analysis.get('hash', 'N/A')})")

    # Recommandations
    print(f"\n💡 ANALYSE ET RECOMMANDATIONS:")
    print("-" * 60)

    if largest_group_size > 1:
        print(
            f"✨ CONSENSUS DÉTECTÉ: {largest_group_size} implémentations donnent le même résultat (Hash: {largest_group_hash})")
        consensus_group = [a for a in analyses if a.get('hash') == largest_group_hash]
        if all(a.get('is_valid', False) for a in consensus_group):
            print("   └─ Ce résultat semble VALIDE (pas de doublons, pas de groupes vides)")
        else:
            print("   └─ ATTENTION: Ce résultat a des problèmes de validité")
    else:
        print("⚠️  AUCUN CONSENSUS: Toutes les implémentations donnent des résultats différents")

    # Identifier les implémentations suspectes
    invalid_impls = [a for a in analyses if not a.get('is_valid', True)]
    if invalid_impls:
        print(f"\n❌ IMPLÉMENTATIONS AVEC ERREURS ({len(invalid_impls)}):")
        for analysis in invalid_impls:
            print(f"   - {analysis['name']}")

    return {
        'analyses': analyses,
        'hash_groups': dict(hash_groups),
        'consensus_hash': largest_group_hash,
        'consensus_size': largest_group_size,
        'total_implementations': len(analyses),
        'valid_implementations': sum(1 for a in analyses if a.get('is_valid', True))
    }


def run_single_test_with_analysis(
        elements: List[Any],
        relations: List[Tuple[Any, Any]],
        implementations: Dict[str, callable]
) -> None:
    """Exécute un test unique avec analyse détaillée."""
    analysis_result = detailed_comparison_analysis(elements, relations, implementations)

    # Suggestions d'actions
    print(f"\n🎯 SUGGESTIONS D'ACTION:")
    print("-" * 60)

    if analysis_result['consensus_size'] >= 3:
        consensus_hash = analysis_result['consensus_hash']
        consensus_impls = [analysis['name'] for analysis in analysis_result['hash_groups'][consensus_hash]]
        print(f"1. Le consensus ({consensus_impls}) est probablement CORRECT")
        print("2. Investiguer les implémentations divergentes")
    elif analysis_result['consensus_size'] == 2:
        print("1. Deux implémentations concordent - vérifier manuellement")
        print("2. Les autres implémentations sont probablement incorrectes")
    else:
        print("1. SITUATION CRITIQUE: Aucun consensus détecté")
        print("2. Vérifier la logique de TOUTES les implémentations")
        print("3. Faire un test manuel avec un petit jeu de données")


# Fonction modifiée pour les tests
def run_tests_with_detailed_analysis(
        implementations: Dict[str, callable],
        n_elements_list: List[int],
        n_relations_factors: List[float],
        detailed_analysis_frequency: int = 5  # Analyse détaillée tous les N tests
) -> None:
    """
    Version améliorée de run_tests avec analyse détaillée périodique.
    """
    print("🚀 Début des tests de performance et de validité AVEC ANALYSE DÉTAILLÉE.")
    print("-" * 70)

    test_counter = 0

    for i, n_elements in enumerate(n_elements_list):
        for j, factor in enumerate(n_relations_factors):
            test_counter += 1

            # Calcul du nombre de relations
            if factor == 1000:
                n_relations = 1000
            else:
                n_relations = max(1000, int(n_elements * factor)) if n_elements > 0 else 1000

            elements, relations = generate_test_data(n_elements, n_relations)

            print(f"\n🧪 Test {i + 1}.{j + 1} : {n_elements} éléments, {n_relations} relations")

            # Analyse détaillée périodiquement ou si on détecte des erreurs
            should_analyze = (test_counter % detailed_analysis_frequency == 1)

            if not should_analyze:
                # Test rapide normal
                print("  -> Exécution de la référence (naïve)... ", end="")
                start_time = time.time()
                ref_result = partition_par_unions_naive(elements, relations)
                end_time = time.time()
                print(f"Terminé en {end_time - start_time:.4f}s")

                error_count = 0
                for name, func in implementations.items():
                    if name == 'naïve':  # Skip duplicate
                        continue
                    print(f"  -> Exécution de '{name}'... ", end="")
                    try:
                        start_time = time.time()
                        current_result = func(elements, relations)
                        end_time = time.time()
                        duration = end_time - start_time

                        is_correct = compare_results(ref_result, current_result)
                        status = "✅ Correct" if is_correct else "❌ Erreur"
                        print(f"Terminé en {duration:.4f}s ({status})")

                        if not is_correct:
                            error_count += 1
                    except Exception as e:
                        print(f"Erreur lors de l'exécution de '{name}': {e}")
                        error_count += 1

                # Si beaucoup d'erreurs, faire une analyse détaillée
                if error_count >= len(implementations) // 2:
                    print(f"\n⚠️  TROP D'ERREURS DÉTECTÉES ({error_count}) - ANALYSE DÉTAILLÉE:")
                    should_analyze = True

            if should_analyze:
                # Analyse détaillée
                run_single_test_with_analysis(elements, relations, implementations)

            print("-" * 70)

    print("\n✅ Tous les tests sont terminés.")

# Fonction modifiée pour les tests
def run_tests_with_detailed_analysis(
        implementations: Dict[str, callable],
        n_elements_list: List[int],
        n_relations_factors: List[float],
        detailed_analysis_frequency: int = 5  # Analyse détaillée tous les N tests
) -> None:
    """
    Version améliorée de run_tests avec analyse détaillée périodique.
    """
    print("🚀 Début des tests de performance et de validité AVEC ANALYSE DÉTAILLÉE.")
    print("-" * 70)

    test_counter = 0

    for i, n_elements in enumerate(n_elements_list):
        for j, factor in enumerate(n_relations_factors):
            test_counter += 1

            # Calcul du nombre de relations
            if factor == 1000:
                n_relations = 1000
            else:
                n_relations = max(1000, int(n_elements * factor)) if n_elements > 0 else 1000

            elements, relations = generate_test_data(n_elements, n_relations)

            print(f"\n🧪 Test {i + 1}.{j + 1} : {n_elements} éléments, {n_relations} relations")

            # Analyse détaillée périodiquement ou si on détecte des erreurs
            should_analyze = (test_counter % detailed_analysis_frequency == 1)

            if not should_analyze:
                # Test rapide normal
                print("  -> Exécution de la référence (naïve)... ", end="")
                start_time = time.time()
                ref_result = partition_par_unions_naive(elements, relations)
                end_time = time.time()
                print(f"Terminé en {end_time - start_time:.4f}s")

                error_count = 0
                for name, func in implementations.items():
                    if name == 'naïve':  # Skip duplicate
                        continue
                    print(f"  -> Exécution de '{name}'... ", end="")
                    try:
                        start_time = time.time()
                        current_result = func(elements, relations)
                        end_time = time.time()
                        duration = end_time - start_time

                        is_correct = compare_results(ref_result, current_result)
                        status = "✅ Correct" if is_correct else "❌ Erreur"
                        print(f"Terminé en {duration:.4f}s ({status})")

                        if not is_correct:
                            error_count += 1
                    except Exception as e:
                        print(f"Erreur lors de l'exécution de '{name}': {e}")
                        error_count += 1

                # Si beaucoup d'erreurs, faire une analyse détaillée
                if error_count >= len(implementations) // 2:
                    print(f"\n⚠️  TROP D'ERREURS DÉTECTÉES ({error_count}) - ANALYSE DÉTAILLÉE:")
                    should_analyze = True

            if should_analyze:
                # Analyse détaillée
                run_single_test_with_analysis(elements, relations, implementations)

            print("-" * 70)

    print("\n✅ Tous les tests sont terminés.")
# --- Exécution principale ---

if __name__ == "__main__":
    n_elements_list = [5_000, 25_000, 125_000, 750_000, 1_500_000, 2_500_000, 10_500_000]
    n_relations_factors = [1000, 1 / 20, 1 / 10, 1 / 5, 1 / 2]

    implementations = {
        "naïve": partition_par_unions_naive,
        "impl1": partition_par_unions_1,
        "impl2": partition_par_unions_2,
        "impl3": partition_par_unions_3,
        "impl4": partition_par_unions_4,
        "impl5": partition_par_unions_5,
    }

    elements, relations = generate_test_data(5000, 1000)
    run_single_test_with_analysis(elements, relations, implementations)

    # Ou utiliser la version modifiée des tests avec analyse périodique
    run_tests_with_detailed_analysis(implementations, n_elements_list, n_relations_factors)

#    run_tests(implementations, n_elements_list, n_relations_factors)
