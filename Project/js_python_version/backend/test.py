# -*- coding: utf-8 -*-
"""
Script pour analyser queries_structured.csv avec pandas
Structure attendue: ad_id, point_A (50 valeurs), Y_vector (valeur numérique), D (distance numérique)
"""

import pandas as pd
import os

def analyze_csv_structure():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ads_path = os.path.join(script_dir, 'queries_structured.csv')
    
    print(f"📁 Analyse de {ads_path}")
    print("=" * 80)
    
    # Structure attendue
    print("🎯 STRUCTURE ATTENDUE:")
    print("   1. ad_id : Identifiant de l'annonce")
    print("   2. point_A : 50 valeurs numériques séparées par ';'")
    print("   3. Y_vector : Valeur numérique unique")
    print("   4. D : Distance numérique")
    
    print("\n" + "=" * 80)
    
    # Charger le CSV avec pandas
    try:
        df = pd.read_csv(ads_path)
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return
    
    # Informations générales
    print(f"📋 INFORMATIONS GÉNÉRALES:")
    print(f"   - Forme du DataFrame: {df.shape} (lignes, colonnes)")
    print(f"   - Colonnes trouvées: {list(df.columns)}")
    
    print("\n" + "=" * 80)
    
    # Vérification du nombre de colonnes
    expected_cols = 4
    actual_cols = len(df.columns)
    
    if actual_cols == expected_cols:
        print(f"✅ Nombre de colonnes correct: {actual_cols}/4")
    else:
        print(f"❌ Nombre de colonnes incorrect: {actual_cols}/4")
        return
    
    print("\n" + "=" * 80)
    
    # Analyse de la première ligne
    if len(df) > 0:
        first_row = df.iloc[0]
        print(f"📊 ANALYSE DE LA PREMIÈRE LIGNE:")
        
        for i, (col, val) in enumerate(first_row.items(), 1):
            val_str = str(val)
            print(f"\n  Colonne {i}: '{col}'")
            print(f"    Valeur: '{val_str[:100]}{'...' if len(val_str) > 100 else ''}'")
            print(f"    Type pandas: {df[col].dtype}")
            print(f"    Longueur: {len(val_str)} caractères")
            
            # Validation selon la position et le nom de colonne
            if i == 1:  # Première colonne - ad_id
                print(f"    Attendu: ad_id (identifiant)")
                if 'ad' in col.lower() or 'id' in col.lower():
                    print(f"    ✅ Nom de colonne semble correct")
                else:
                    print(f"    ⚠️  Nom de colonne inattendu (attendu: ad_id)")
                
                if pd.isna(val) or val_str.strip() == '':
                    print(f"    ❌ Valeur vide")
                else:
                    print(f"    ✅ ID: {val_str}")
            
            elif i == 2:  # Deuxième colonne - point_A
                print(f"    Attendu: point_A (50 valeurs séparées par ';')")
                if 'point' in col.lower() or col.lower() == 'point_a':
                    print(f"    ✅ Nom de colonne correct")
                else:
                    print(f"    ⚠️  Nom de colonne inattendu (attendu: point_A)")
                
                if ';' in val_str:
                    coords = val_str.split(';')
                    print(f"    📏 Nombre de valeurs: {len(coords)}")
                    
                    if len(coords) == 50:
                        print(f"    ✅ Nombre correct de valeurs (50)")
                    else:
                        print(f"    ❌ Nombre incorrect: {len(coords)}/50")
                    
                    # Vérifier que toutes les valeurs sont numériques
                    try:
                        numeric_coords = [float(x.strip()) for x in coords[:5]]  # Test sur les 5 premières
                        print(f"    ✅ Valeurs numériques (échantillon): {numeric_coords}")
                        
                        # Stats sur toutes les valeurs
                        all_coords = [float(x.strip()) for x in coords]
                        print(f"    📊 Range: [{min(all_coords):.6f}, {max(all_coords):.6f}]")
                    except ValueError as e:
                        print(f"    ❌ Certaines valeurs ne sont pas numériques: {e}")
                else:
                    print(f"    ❌ Pas de séparateur ';' détecté")
            
            elif i == 3:  # Troisième colonne - Y_vector
                print(f"    Attendu: Y_vector (valeur numérique unique)")
                if 'y_vector' in col.lower() or 'vector' in col.lower():
                    print(f"    ✅ Nom de colonne correct")
                else:
                    print(f"    ⚠️  Nom de colonne inattendu (attendu: Y_vector)")
                
                try:
                    if pd.isna(val):
                        print(f"    ❌ Valeur manquante (NaN)")
                    else:
                        y_value = float(val)
                        print(f"    ✅ Valeur numérique: {y_value}")
                except (ValueError, TypeError):
                    print(f"    ❌ Valeur non numérique: '{val_str}'")
            
            elif i == 4:  # Quatrième colonne - D
                print(f"    Attendu: D (distance numérique)")
                if col.lower() == 'd' or 'distance' in col.lower():
                    print(f"    ✅ Nom de colonne correct")
                else:
                    print(f"    ⚠️  Nom de colonne inattendu (attendu: D)")
                
                try:
                    if pd.isna(val):
                        print(f"    ❌ Valeur manquante (NaN)")
                    else:
                        distance = float(val)
                        print(f"    ✅ Distance numérique: {distance}")
                except (ValueError, TypeError):
                    print(f"    ❌ Valeur non numérique: '{val_str}'")
    
    print("\n" + "=" * 80)
    
    # Validation complète du fichier
    print(f"🔍 VALIDATION COMPLÈTE:")
    
    # Vérifier toutes les lignes de point_A
    if len(df.columns) >= 2:
        point_a_col = df.columns[1]  # Deuxième colonne
        print(f"\n📏 Validation de toutes les valeurs point_A:")
        
        invalid_rows = []
        for idx, val in enumerate(df[point_a_col]):
            val_str = str(val)
            if ';' in val_str:
                coords = val_str.split(';')
                if len(coords) != 50:
                    invalid_rows.append((idx, len(coords)))
        
        if invalid_rows:
            print(f"    ❌ {len(invalid_rows)} lignes avec un nombre incorrect de coordonnées:")
            for row_idx, count in invalid_rows[:5]:  # Montrer les 5 premières
                print(f"      Ligne {row_idx}: {count} valeurs")
        else:
            print(f"    ✅ Toutes les lignes ont 50 coordonnées")
    
    # Statistiques générales
    print(f"\n📈 STATISTIQUES:")
    print(f"   - Nombre total de lignes: {len(df)}")
    print(f"   - Mémoire utilisée: {df.memory_usage(deep=True).sum()} bytes")
    
    # Vérifier les valeurs manquantes
    missing_values = df.isnull().sum()
    if missing_values.any():
        print(f"\n⚠️  VALEURS MANQUANTES:")
        for col, count in missing_values.items():
            if count > 0:
                print(f"   - {col}: {count} valeurs manquantes")
    else:
        print(f"\n✅ Aucune valeur manquante détectée")
    
    # Aperçu final
    print(f"\n👀 APERÇU DES 3 PREMIÈRES LIGNES:")
    # Tronquer point_A pour l'affichage
    df_display = df.copy()
    if len(df.columns) >= 2:
        point_a_col = df.columns[1]
        df_display[point_a_col] = df_display[point_a_col].astype(str).str[:50] + '...'
    
    print(df_display.head(3))

if __name__ == "__main__":
    analyze_csv_structure()