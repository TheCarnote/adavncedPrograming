# Fichier : template_listes_python.py
# Ce script est un template complet pour l'utilisation des listes en Python.
# Il couvre la création, l'accès, la modification, les méthodes principales, et les opérations avancées.

# --- Création de listes ---

ma_liste = []
fruits = ["pomme", "banane", "orange"]
nombres = list(range(5))  # [0, 1, 2, 3, 4]
carres = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
lettres = list("python")  # ['p', 'y', 't', 'h', 'o', 'n']

# --- Accès et modification ---

print(f"Premier fruit : {fruits[0]}")
fruits[1] = "kiwi"
print(f"Dernier fruit : {fruits[-1]}")
print(f"Sous-liste à partir de l'indice 1 : {fruits[1:]}")

# --- Méthodes principales des listes ---

fruits.append("mangue")
fruits.insert(1, "cerise")
fruits.remove("kiwi")
dernier = fruits.pop()
fruits.extend(["ananas", "melon"])
print(f"Liste après modifications : {fruits}")
print(f"'ananas' est-il dans la liste ? {'ananas' in fruits}")

copie_fruits = fruits.copy()
fruits.clear()
print(f"Copie de la liste avant clear : {copie_fruits}")
print(f"Liste après clear : {fruits}")
fruits = copie_fruits.copy()

# --- Opérations avancées ---

liste1 = [1, 2, 3]
liste2 = [4, 5]
fusion = liste1 + liste2
triple = liste1 * 3

for fruit in fruits:
    print(f"Fruit : {fruit}")

for i, fruit in enumerate(fruits):
    print(f"Index {i}: {fruit}")

nombres = [5, 2, 9, 1]
nombres.sort()
nombres_tries = sorted(nombres, reverse=True)
print(f"Nombres triés croissant : {nombres}")
print(f"Nombres triés décroissant : {nombres_tries}")

pairs = [x for x in nombres if x % 2 == 0]
print(f"Nombres pairs : {pairs}")

fruits.reverse()
print(f"Fruits inversés : {fruits}")

index_ananas = fruits.index("ananas") if "ananas" in fruits else -1
print(f"Indice de 'ananas' : {index_ananas}")

test_fruits = ["pomme", "banane", "pomme", "kiwi"]
nb_pommes = test_fruits.count("pomme")
print(f"Nombre de 'pomme' dans test_fruits : {nb_pommes}")

# --- Unicité (suppression des doublons) ---

liste = [1, 2, 2, 3, 1]
unique = list(set(liste))
print(f"Liste unique (ordre non garanti) : {unique}")

unique_ordonne = list(dict.fromkeys(liste))
print(f"Liste unique (ordre conservé) : {unique_ordonne}")

# --- Flatten (aplatir) une liste de listes ---
liste_de_listes = [[1, 2], [3, 4], [5]]
aplatir = [item for sous_liste in liste_de_listes for item in sous_liste]
print(f"Liste aplatit : {aplatir}")

# --- Résumé des méthodes principales ---
resume = '''
Principales méthodes des listes :

append(x)     : Ajoute x à la fin
extend(liste) : Ajoute tous les éléments d’une autre liste
insert(i, x)  : Insère x à l’indice i
remove(x)     : Supprime la première occurrence de x
pop([i])      : Retire et retourne l’élément à l’indice i
clear()       : Vide la liste
index(x)      : Indice de la première occurrence de x
count(x)      : Nombre d’occurrences de x
sort()        : Trie la liste
reverse()     : Inverse la liste
copy()        : Copie superficielle
'''
print(resume)

# --- Affichage final ---
print("Liste finale des fruits :", fruits)
print("Liste fusionnée :", fusion)
print("Liste aplatit :", aplatir)
print("Liste sans doublons (ordre conservé) :", unique_ordonne)

# Fin du template
