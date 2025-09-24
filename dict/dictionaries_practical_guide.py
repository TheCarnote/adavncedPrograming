# dictionary_guide.py

# ==============================================================================
# GUIDE PRATIQUE DU DICTIONNAIRE EN PYTHON
# ==============================================================================

def main():
    """
    Fonction principale pour explorer les fonctionnalités des dictionnaires.
    Ce programme sert de guide et de référence pour l'apprentissage.
    """
    print("🚀 BIENVENUE DANS LE GUIDE PRATIQUE DU DICTIONNAIRE EN PYTHON")
    print("Ce programme est une référence pour comprendre et utiliser les dictionnaires.")
    print("------------------------------------------------------------------")

    # --- 1. Création et initialisation ---
    print("\n[SECTION 1: CRÉATION ET INITIALISATION]")

    # Création d'un dictionnaire vide
    empty_dict = {}
    print(f"1. Création d'un dictionnaire vide : {empty_dict}")

    # Création avec des paires clé-valeur
    fruit_prices = {
        'pomme': 0.5,
        'banane': 0.3,
        'orange': 0.6,
        'raisin': 1.2
    }
    print(f"2. Création avec des valeurs : {fruit_prices}")

    # Création à partir de listes (avec zip)
    keys = ['France', 'Japon', 'Allemagne']
    values = ['Paris', 'Tokyo', 'Berlin']
    capitals = dict(zip(keys, values))
    print(f"3. Création à partir de listes (via zip) : {capitals}")

    # --- 2. Accès et modification ---
    print("\n[SECTION 2: ACCÈS ET MODIFICATION]")

    # Accès direct (peut lever une KeyError)
    print(f"1. Accès direct à la 'pomme' : {fruit_prices['pomme']}")

    # Accès sécurisé avec .get()
    # Cela évite les erreurs si la clé n'existe pas, et renvoie une valeur par défaut
    missing_item = fruit_prices.get('fraise', 'Non disponible')
    print(f"2. Accès à 'fraise' (via .get()) : {missing_item}")

    # Ajout d'une nouvelle clé-valeur
    fruit_prices['cerise'] = 2.5
    print(f"3. Ajout de 'cerise' : {fruit_prices}")

    # Modification d'une valeur existante
    fruit_prices['banane'] = 0.35
    print(f"4. Mise à jour de la 'banane' : {fruit_prices}")

    # --- 3. Parcours (Itération) ---
    print("\n[SECTION 3: PARCOURS (ITÉRATION)]")

    # Parcourir les clés (le plus courant)
    print("1. Parcourir les clés :")
    for key in fruit_prices:
        print(f"   - {key}")

    # Parcourir les valeurs
    print("2. Parcourir les valeurs :")
    for value in fruit_prices.values():
        print(f"   - {value}")

    # Parcourir les paires (clé, valeur) avec .items()
    print("3. Parcourir les paires (clé, valeur) :")
    for fruit, price in fruit_prices.items():
        print(f"   - Le prix du {fruit} est {price}")

    # --- 4. Suppression d'éléments ---
    print("\n[SECTION 4: SUPPRESSION D'ÉLÉMENTS]")

    # Suppression par clé avec 'del'
    del fruit_prices['raisin']
    print(f"1. Suppression de 'raisin' avec 'del' : {fruit_prices}")

    # Suppression avec .pop() pour récupérer la valeur supprimée
    removed_price = fruit_prices.pop('banane')
    print(f"2. Suppression de 'banane' avec .pop(), prix récupéré : {removed_price}")
    print(f"   Dictionnaire final : {fruit_prices}")

    # Vider le dictionnaire
    fruit_prices.clear()
    print(f"3. Dictionnaire vidé avec .clear() : {fruit_prices}")

    # --- 5. Autres opérations utiles ---
    print("\n[SECTION 5: AUTRES OPÉRATIONS]")

    # Vérification d'existence de clé avec l'opérateur 'in'
    is_pomme_in_dict = 'pomme' in fruit_prices
    print(f"1. 'pomme' est-il dans le dictionnaire ? {is_pomme_in_dict}")

    # Concaténation de dictionnaires (avec l'opérateur **)
    dico1 = {'a': 1, 'b': 2}
    dico2 = {'c': 3, 'd': 4}
    merged_dict = {**dico1, **dico2}
    print(f"2. Fusion de deux dictionnaires : {merged_dict}")

    # Création par compréhension
    squares = {x: x ** 2 for x in range(1, 6)}
    print(f"3. Création par compréhension : {squares}")

    print("\n------------------------------------------------------------------")
    print("🏁 Fin du guide. Vous avez maintenant une vue d'ensemble des fonctions des dictionnaires.")


if __name__ == "__main__":
    main()
