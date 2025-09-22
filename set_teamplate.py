"""
Ce fichier Python illustre les manipulations et l'usage de la structure de données 'set'.

Un 'set' est une collection non ordonnée d'éléments uniques et non modifiables (hachables).
Il est très efficace pour les opérations d'appartenance, d'union, d'intersection, et de différence.
"""

# --- 1. Création d'un set ---
# Les éléments en double sont automatiquement supprimés.
print("--- 1. Création de sets ---")
my_set = {1, 2, 3, 4, 4, 5}
print(f"Set créé à partir d'une liste avec des doublons : {my_set}") # Les doublons ont disparu.

# Création d'un set vide (ne pas utiliser {} car cela crée un dictionnaire vide)
empty_set = set()
print(f"Set vide : {empty_set}")

# Création à partir d'une liste ou d'un tuple
list_to_set = set([1, 2, 3, 3, 2, 1])
print(f"Set créé à partir d'une liste : {list_to_set}")
print("-" * 50)


# --- 2. Ajout et suppression d'éléments ---
print("--- 2. Ajout et suppression d'éléments ---")
my_set = {10, 20, 30}
print(f"Set initial : {my_set}")

# Ajout d'un élément avec .add()
my_set.add(40)
print(f"Après l'ajout de 40 : {my_set}")

# Ajout d'éléments avec .update() (accepte un itérable)
my_set.update([50, 60, 20])
print(f"Après l'ajout de [50, 60, 20] : {my_set}") # 20 n'est pas ajouté car il existe déjà.

# Suppression d'un élément avec .remove() (lève une erreur si l'élément n'existe pas)
my_set.remove(60)
print(f"Après la suppression de 60 : {my_set}")

# Suppression d'un élément avec .discard() (ne lève pas d'erreur si l'élément n'existe pas)
my_set.discard(100)
print(f"Après la suppression de 100 (non existant) : {my_set}")

# Suppression d'un élément aléatoire avec .pop()
popped_element = my_set.pop()
print(f"Élément supprimé aléatoirement : {popped_element}")
print(f"Set après .pop() : {my_set}")

# Suppression de tous les éléments
my_set.clear()
print(f"Set après .clear() : {my_set}")
print("-" * 50)


# --- 3. Vérification de l'appartenance (très rapide) ---
print("--- 3. Vérification de l'appartenance ---")
big_set = set(range(1_000_000))
search_number = 999_999

start_time = time.time()
is_in = search_number in big_set
end_time = time.time()

print(f"Vérification de l'appartenance de {search_number} dans le set : {is_in}")
print(f"Temps d'exécution : {(end_time - start_time) * 1000:.4f} ms") # Opération en O(1)
print("-" * 50)


# --- 4. Opérations mathématiques sur les sets ---
print("--- 4. Opérations mathématiques ---")
set_A = {1, 2, 3, 4, 5}
set_B = {4, 5, 6, 7, 8}

# Union : tous les éléments des deux sets (set_A | set_B)
union_set = set_A.union(set_B)
print(f"Union de A et B : {union_set}")

# Intersection : éléments communs aux deux sets (set_A & set_B)
intersection_set = set_A.intersection(set_B)
print(f"Intersection de A et B : {intersection_set}")

# Différence : éléments de A qui ne sont pas dans B (set_A - set_B)
difference_set = set_A.difference(set_B)
print(f"Différence (A - B) : {difference_set}")

# Différence symétrique : éléments dans A ou B, mais pas dans les deux (set_A ^ set_B)
sym_difference_set = set_A.symmetric_difference(set_B)
print(f"Différence symétrique : {sym_difference_set}")
print("-" * 50)


# --- 5. Sous-ensemble et sur-ensemble ---
print("--- 5. Sous-ensemble et sur-ensemble ---")
set_X = {1, 2, 3}
set_Y = {1, 2, 3, 4, 5}

# set_X est un sous-ensemble de set_Y ? (set_X <= set_Y)
is_subset = set_X.issubset(set_Y)
print(f"X est-il un sous-ensemble de Y ? : {is_subset}")

# set_Y est un sur-ensemble de set_X ? (set_Y >= set_X)
is_superset = set_Y.issuperset(set_X)
print(f"Y est-il un sur-ensemble de X ? : {is_superset}")
print("-" * 50)


# --- 6. Le frozenset (set immuable) ---
# Un frozenset ne peut pas être modifié après sa création.
print("--- 6. Le frozenset (set immuable) ---")
my_frozenset = frozenset([1, 2, 3])
print(f"Frozenset créé : {my_frozenset}")

# Tentative de modification (lèvera une erreur)
# my_frozenset.add(4) # Uncomment to see the error

# Utilité : peut être utilisé comme clé de dictionnaire
dict_of_frozensets = {frozenset([1, 2]): "valeur_1", frozenset([3, 4]): "valeur_2"}
print(f"Dictionnaire avec des frozensets comme clés : {dict_of_frozensets}")
