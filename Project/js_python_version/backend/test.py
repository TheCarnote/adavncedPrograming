# # -*- coding: utf-8 -*-
# """
# Script pour analyser queries_structured.csv avec pandas
# Structure attendue: ad_id, point_A (50 valeurs), Y_vector (valeur numérique), D (distance numérique)
# """

# import pandas as pd
# import os

# def analyze_csv_structure():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     ads_path = os.path.join(script_dir, 'queries_structured.csv')
    
#     print(f"📁 Analyse de {ads_path}")
#     print("=" * 80)
    
#     # Structure attendue
#     print("🎯 STRUCTURE ATTENDUE:")
#     print("   1. ad_id : Identifiant de l'annonce")
#     print("   2. point_A : 50 valeurs numériques séparées par ';'")
#     print("   3. Y_vector : Valeur numérique unique")
#     print("   4. D : Distance numérique")
    
#     print("\n" + "=" * 80)
    
#     # Charger le CSV avec pandas
#     try:
#         df = pd.read_csv(ads_path)
#     except Exception as e:
#         print(f"❌ Erreur lors du chargement: {e}")
#         return
    
#     # Informations générales
#     print(f"📋 INFORMATIONS GÉNÉRALES:")
#     print(f"   - Forme du DataFrame: {df.shape} (lignes, colonnes)")
#     print(f"   - Colonnes trouvées: {list(df.columns)}")
    
#     print("\n" + "=" * 80)
    
#     # Vérification du nombre de colonnes
#     expected_cols = 4
#     actual_cols = len(df.columns)
    
#     if actual_cols == expected_cols:
#         print(f"✅ Nombre de colonnes correct: {actual_cols}/4")
#     else:
#         print(f"❌ Nombre de colonnes incorrect: {actual_cols}/4")
#         return
    
#     print("\n" + "=" * 80)
    
#     # Analyse de la première ligne
#     if len(df) > 0:
#         first_row = df.iloc[0]
#         print(f"📊 ANALYSE DE LA PREMIÈRE LIGNE:")
        
#         for i, (col, val) in enumerate(first_row.items(), 1):
#             val_str = str(val)
#             print(f"\n  Colonne {i}: '{col}'")
#             print(f"    Valeur: '{val_str[:100]}{'...' if len(val_str) > 100 else ''}'")
#             print(f"    Type pandas: {df[col].dtype}")
#             print(f"    Longueur: {len(val_str)} caractères")
            
#             # Validation selon la position et le nom de colonne
#             if i == 1:  # Première colonne - ad_id
#                 print(f"    Attendu: ad_id (identifiant)")
#                 if 'ad' in col.lower() or 'id' in col.lower():
#                     print(f"    ✅ Nom de colonne semble correct")
#                 else:
#                     print(f"    ⚠️  Nom de colonne inattendu (attendu: ad_id)")
                
#                 if pd.isna(val) or val_str.strip() == '':
#                     print(f"    ❌ Valeur vide")
#                 else:
#                     print(f"    ✅ ID: {val_str}")
            
#             elif i == 2:  # Deuxième colonne - point_A
#                 print(f"    Attendu: point_A (50 valeurs séparées par ';')")
#                 if 'point' in col.lower() or col.lower() == 'point_a':
#                     print(f"    ✅ Nom de colonne correct")
#                 else:
#                     print(f"    ⚠️  Nom de colonne inattendu (attendu: point_A)")
                
#                 if ';' in val_str:
#                     coords = val_str.split(';')
#                     print(f"    📏 Nombre de valeurs: {len(coords)}")
                    
#                     if len(coords) == 50:
#                         print(f"    ✅ Nombre correct de valeurs (50)")
#                     else:
#                         print(f"    ❌ Nombre incorrect: {len(coords)}/50")
                    
#                     # Vérifier que toutes les valeurs sont numériques
#                     try:
#                         numeric_coords = [float(x.strip()) for x in coords[:5]]  # Test sur les 5 premières
#                         print(f"    ✅ Valeurs numériques (échantillon): {numeric_coords}")
                        
#                         # Stats sur toutes les valeurs
#                         all_coords = [float(x.strip()) for x in coords]
#                         print(f"    📊 Range: [{min(all_coords):.6f}, {max(all_coords):.6f}]")
#                     except ValueError as e:
#                         print(f"    ❌ Certaines valeurs ne sont pas numériques: {e}")
#                 else:
#                     print(f"    ❌ Pas de séparateur ';' détecté")
            
#             elif i == 3:  # Troisième colonne - Y_vector
#                 print(f"    Attendu: Y_vector (valeur numérique unique)")
#                 if 'y_vector' in col.lower() or 'vector' in col.lower():
#                     print(f"    ✅ Nom de colonne correct")
#                 else:
#                     print(f"    ⚠️  Nom de colonne inattendu (attendu: Y_vector)")
                
#                 try:
#                     if pd.isna(val):
#                         print(f"    ❌ Valeur manquante (NaN)")
#                     else:
#                         y_value = float(val)
#                         print(f"    ✅ Valeur numérique: {y_value}")
#                 except (ValueError, TypeError):
#                     print(f"    ❌ Valeur non numérique: '{val_str}'")
            
#             elif i == 4:  # Quatrième colonne - D
#                 print(f"    Attendu: D (distance numérique)")
#                 if col.lower() == 'd' or 'distance' in col.lower():
#                     print(f"    ✅ Nom de colonne correct")
#                 else:
#                     print(f"    ⚠️  Nom de colonne inattendu (attendu: D)")
                
#                 try:
#                     if pd.isna(val):
#                         print(f"    ❌ Valeur manquante (NaN)")
#                     else:
#                         distance = float(val)
#                         print(f"    ✅ Distance numérique: {distance}")
#                 except (ValueError, TypeError):
#                     print(f"    ❌ Valeur non numérique: '{val_str}'")
    
#     print("\n" + "=" * 80)
    
#     # Validation complète du fichier
#     print(f"🔍 VALIDATION COMPLÈTE:")
    
#     # Vérifier toutes les lignes de point_A
#     if len(df.columns) >= 2:
#         point_a_col = df.columns[1]  # Deuxième colonne
#         print(f"\n📏 Validation de toutes les valeurs point_A:")
        
#         invalid_rows = []
#         for idx, val in enumerate(df[point_a_col]):
#             val_str = str(val)
#             if ';' in val_str:
#                 coords = val_str.split(';')
#                 if len(coords) != 50:
#                     invalid_rows.append((idx, len(coords)))
        
#         if invalid_rows:
#             print(f"    ❌ {len(invalid_rows)} lignes avec un nombre incorrect de coordonnées:")
#             for row_idx, count in invalid_rows[:5]:  # Montrer les 5 premières
#                 print(f"      Ligne {row_idx}: {count} valeurs")
#         else:
#             print(f"    ✅ Toutes les lignes ont 50 coordonnées")
    
#     # Statistiques générales
#     print(f"\n📈 STATISTIQUES:")
#     print(f"   - Nombre total de lignes: {len(df)}")
#     print(f"   - Mémoire utilisée: {df.memory_usage(deep=True).sum()} bytes")
    
#     # Vérifier les valeurs manquantes
#     missing_values = df.isnull().sum()
#     if missing_values.any():
#         print(f"\n⚠️  VALEURS MANQUANTES:")
#         for col, count in missing_values.items():
#             if count > 0:
#                 print(f"   - {col}: {count} valeurs manquantes")
#     else:
#         print(f"\n✅ Aucune valeur manquante détectée")
    
#     # Aperçu final
#     print(f"\n👀 APERÇU DES 3 PREMIÈRES LIGNES:")
#     # Tronquer point_A pour l'affichage
#     df_display = df.copy()
#     if len(df.columns) >= 2:
#         point_a_col = df.columns[1]
#         df_display[point_a_col] = df_display[point_a_col].astype(str).str[:50] + '...'
    
#     print(df_display.head(3))

if __name__ == "__main__":
    str = "node_818:24.862533;node_243:25.923757;node_315:26.030034;node_315:26.030034;node_432:26.329065;node_551:26.396010;node_21:26.461203;node_41:26.692871;node_41:26.692871;node_41:26.692871;node_41:26.692871;node_41:26.692871;node_357:26.699853;node_720:26.759491;node_720:26.759491;node_720:26.759491;node_720:26.759491;node_720:26.759491;node_749:26.828453;node_749:26.828453;node_795:26.835305;node_795:26.835305;node_795:26.835305;node_618:26.985084;node_618:26.985084;node_618:26.985084;node_618:26.985084;node_181:27.003057;node_181:27.003057;node_181:27.003057;node_474:27.042752;node_517:27.065215;node_521:27.083840;node_521:27.083840;node_521:27.083840;node_633:27.095338;node_633:27.095338;node_185:27.188983;node_185:27.188983;node_194:27.235930;node_194:27.235930;node_194:27.235930;node_194:27.235930;node_194:27.235930;node_194:27.235930;node_99:27.258009;node_99:27.258009;node_99:27.258009;node_727:27.336715;node_785:27.351662;node_785:27.351662;node_785:27.351662;node_785:27.351662;node_655:27.351892;node_655:27.351892;node_655:27.351892;node_29:27.425611;node_29:27.425611;node_425:27.493497;node_425:27.493497;node_425:27.493497;node_425:27.493497;node_339:27.522657;node_902:27.574874;node_902:27.574874;node_463:27.590526;node_463:27.590526;node_463:27.590526;node_970:27.633704;node_970:27.633704;node_970:27.633704;node_970:27.633704;node_970:27.633704;node_970:27.633704;node_977:27.648501;node_977:27.648501;node_791:27.693806;node_791:27.693806;node_791:27.693806;node_791:27.693806;node_791:27.693806;node_791:27.693806;node_791:27.693806;node_593:27.742903;node_593:27.742903;node_593:27.742903;node_593:27.742903;node_593:27.742903;node_781:27.774836;node_781:27.774836;node_781:27.774836;node_781:27.774836;node_781:27.774836;node_781:27.774836;node_433:27.775254;node_433:27.775254;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_870:27.778331;node_973:27.820164;node_973:27.820164;node_140:27.873715;node_140:27.873715;node_140:27.873715;node_399:27.902593;node_399:27.902593;node_399:27.902593;node_399:27.902593;node_802:27.927175;node_802:27.927175;node_802:27.927175;node_691:27.957219;node_691:27.957219;node_691:27.957219;node_403:27.983973;node_403:27.983973;node_403:27.983973;node_403:27.983973;node_403:27.983973;node_154:28.047012;node_588:28.051341;node_467:28.058598;node_467:28.058598;node_467:28.058598;node_467:28.058598;node_467:28.058598;node_571:28.104623;node_571:28.104623;node_572:28.107613;node_572:28.107613;node_286:28.108073;node_286:28.108073;node_286:28.108073;node_286:28.108073;node_295:28.113665;node_295:28.113665;node_295:28.113665;node_295:28.113665;node_235:28.163633;node_235:28.163633;node_235:28.163633;node_235:28.163633;node_235:28.163633;node_235:28.163633;node_235:28.163633;node_235:28.163633;node_235:28.163633;node_726:28.165919;node_322:28.168047;node_322:28.168047;node_322:28.168047;node_322:28.168047;node_438:28.173361;node_438:28.173361;node_438:28.173361;node_363:28.240763;node_363:28.240763;node_363:28.240763;node_100:28.242386;node_100:28.242386;node_14:28.244380;node_14:28.244380;node_14:28.244380;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_694:28.270476;node_180:28.270977;node_180:28.270977;node_180:28.270977;node_180:28.270977;node_180:28.270977;node_180:28.270977;node_180:28.270977;node_180:28.270977;node_180:28.270977;node_653:28.274000;node_653:28.274000;node_653:28.274000;node_653:28.274000;node_653:28.274000;node_653:28.274000;node_917:28.289608;node_917:28.289608;node_917:28.289608;node_917:28.289608;node_283:28.322928;node_283:28.322928;node_283:28.322928;node_283:28.322928;node_283:28.322928;node_283:28.322928;node_283:28.322928;node_166:28.323367;node_166:28.323367;node_166:28.323367;node_166:28.323367;node_166:28.323367;node_212:28.323927;node_212:28.323927;node_212:28.323927;node_212:28.323927;node_212:28.323927;node_212:28.323927;node_212:28.323927;node_212:28.323927;node_212:28.323927;node_471:28.371665;node_471:28.371665;node_471:28.371665;node_471:28.371665;node_471:28.371665;node_471:28.371665;node_201:28.374828;node_201:28.374828;node_201:28.374828;node_201:28.374828;node_323:28.375244;node_323:28.375244;node_323:28.375244;node_323:28.375244;node_323:28.375244;node_860:28.382437;node_860:28.382437;node_860:28.382437;node_860:28.382437;node_860:28.382437;node_860:28.382437;node_860:28.382437;node_529:28.408915;node_529:28.408915;node_529:28.408915;node_529:28.408915;node_529:28.408915;node_529:28.408915;node_529:28.408915;node_529:28.408915;node_529:28.408915;node_529:28.408915;node_605:28.417522;node_605:28.417522;node_605:28.417522;node_605:28.417522;node_605:28.417522;node_605:28.417522;node_605:28.417522;node_371:28.431972;node_371:28.431972;node_371:28.431972;node_371:28.431972;node_679:28.436296;node_679:28.436296;node_679:28.436296;node_954:28.445769;node_963:28.472948;node_963:28.472948;node_963:28.472948;node_963:28.472948;node_963:28.472948;node_963:28.472948;node_963:28.472948;node_959:28.486910;node_959:28.486910;node_959:28.486910;node_959:28.486910;node_959:28.486910;node_959:28.486910;node_959:28.486910;node_959:28.486910;node_959:28.486910;node_925:28.510470;node_350:28.542400;node_350:28.542400;node_350:28.542400;node_350:28.542400;node_22:28.576774;node_22:28.576774;node_22:28.576774;node_22:28.576774;node_22:28.576774;node_22:28.576774;node_22:28.576774;node_22:28.576774;node_22:28.576774;node_22:28.576774;node_376:28.633760;node_376:28.633760;node_376:28.633760;node_376:28.633760;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_203:28.650137;node_76:28.655861;node_76:28.655861;node_76:28.655861;node_391:28.701856;node_391:28.701856;node_391:28.701856;node_391:28.701856;node_590:28.728308;node_590:28.728308;node_590:28.728308;node_590:28.728308;node_590:28.728308;node_570:28.748636;node_570:28.748636;node_570:28.748636;node_570:28.748636;node_570:28.748636;node_687:28.752525;node_687:28.752525;node_687:28.752525;node_687:28.752525;node_687:28.752525;node_687:28.752525;node_108:28.776295;node_108:28.776295;node_642:28.776361;node_642:28.776361;node_642:28.776361;node_642:28.776361;node_624:28.776893;node_624:28.776893;node_624:28.776893;node_390:28.786720;node_390:28.786720;node_390:28.786720;node_390:28.786720;node_390:28.786720;node_390:28.786720;node_390:28.786720;node_516:28.794711;node_516:28.794711;node_516:28.794711;node_516:28.794711;node_516:28.794711;node_434:28.807412;node_434:28.807412;node_434:28.807412;node_434:28.807412;node_704:28.808047;node_704:28.808047;node_704:28.808047;node_648:28.811011;node_648:28.811011;node_648:28.811011;node_648:28.811011;node_648:28.811011;node_648:28.811011;node_648:28.811011;node_592:28.819999;node_592:28.819999;node_592:28.819999;node_592:28.819999;node_407:28.821395;node_407:28.821395;node_407:28.821395;node_773:28.824485;node_773:28.824485;node_773:28.824485;node_773:28.824485;node_773:28.824485;node_773:28.824485;node_773:28.824485;node_773:28.824485;node_182:28.844097;node_182:28.844097;node_182:28.844097;node_182:28.844097;node_182:28.844097;node_750:28.844960;node_750:28.844960;node_750:28.844960;node_750:28.844960;node_750:28.844960;node_750:28.844960;node_750:28.844960;node_750:28.844960;node_547:28.858809;node_547:28.858809;node_547:28.858809;node_54:28.861411;node_54:28.861411;node_54:28.861411;node_54:28.861411;node_54:28.861411;node_54:28.861411;node_54:28.861411;node_54:28.861411;node_54:28.861411;node_54:28.861411;node_508:28.899662;node_508:28.899662;node_508:28.899662;node_344:28.902169;node_344:28.902169;node_344:28.902169;node_344:28.902169;node_344:28.902169;node_775:28.907905;node_775:28.907905;node_775:28.907905;node_775:28.907905;node_775:28.907905;node_775:28.907905;node_775:28.907905;node_775:28.907905;node_317:28.935757;node_317:28.935757;node_317:28.935757;node_317:28.935757;node_317:28.935757;node_317:28.935757;node_317:28.935757;node_317:28.935757;node_317:28.935757;node_267:28.945924;node_267:28.945924;node_267:28.945924;node_267:28.945924;node_267:28.945924;node_267:28.945924;node_267:28.945924;node_267:28.945924;node_267:28.945924;node_267:28.945924;node_530:28.952037;node_530:28.952037;node_530:28.952037;node_530:28.952037;node_530:28.952037;node_530:28.952037;node_530:28.952037;node_530:28.952037;node_530:28.952037;node_530:28.952037;node_560:28.987100;node_560:28.987100;node_560:28.987100;node_560:28.987100;node_560:28.987100;node_560:28.987100;node_560:28.987100;node_560:28.987100;node_362:29.001194;node_362:29.001194;node_362:29.001194;node_495:29.003625;node_495:29.003625;node_495:29.003625;node_601:29.010876;node_601:29.010876;node_601:29.010876;node_601:29.010876;node_601:29.010876;node_601:29.010876;node_601:29.010876;node_601:29.010876;node_601:29.010876;node_144:29.026449;node_144:29.026449;node_144:29.026449;node_144:29.026449;node_144:29.026449;node_144:29.026449;node_144:29.026449;node_537:29.030143;node_537:29.030143;node_537:29.030143;node_537:29.030143;node_537:29.030143;node_537:29.030143;node_757:29.064418;node_757:29.064418;node_2:29.068530;node_2:29.068530;node_2:29.068530;node_2:29.068530;node_394:29.075742;node_394:29.075742;node_394:29.075742;node_394:29.075742;node_163:29.098580;node_163:29.098580;node_163:29.098580;node_163:29.098580;node_538:29.105535;node_538:29.105535;node_538:29.105535;node_538:29.105535;node_538:29.105535;node_538:29.105535;node_872:29.108945;node_872:29.108945;node_872:29.108945;node_872:29.108945;node_872:29.108945;node_872:29.108945;node_872:29.108945;node_872:29.108945;node_872:29.108945;node_872:29.108945;node_224:29.111180;node_224:29.111180;node_224:29.111180;node_224:29.111180;node_224:29.111180;node_122:29.129442;node_122:29.129442;node_122:29.129442;node_122:29.129442;node_122:29.129442;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_165:29.140980;node_45:29.157938;node_45:29.157938;node_45:29.157938;node_569:29.177237;node_569:29.177237;node_569:29.177237;node_569:29.177237;node_569:29.177237;node_569:29.177237;node_569:29.177237;node_569:29.177237;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_999:29.194674;node_292:29.212826;node_292:29.212826;node_292:29.212826;node_292:29.212826;node_292:29.212826;node_292:29.212826;node_292:29.212826;node_824:29.218972;node_464:29.233938;node_464:29.233938;node_464:29.233938;node_464:29.233938;node_875:29.240632;node_875:29.240632;node_875:29.240632;node_875:29.240632;node_875:29.240632;node_261:29.253396;node_261:29.253396;node_261:29.253396;node_261:29.253396;node_261:29.253396;node_261:29.253396;node_261:29.253396;node_261:29.253396;node_261:29.253396;node_261:29.253396;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_719:29.272549;node_596:29.273690;node_596:29.273690;node_596:29.273690;node_596:29.273690;node_596:29.273690;node_596:29.273690;node_596:29.273690;node_596:29.273690;node_475:29.274114;node_475:29.274114;node_475:29.274114;node_475:29.274114;node_475:29.274114;node_475:29.274114;node_475:29.274114;node_475:29.274114;node_475:29.274114;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_663:29.279428;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_831:29.290474;node_341:29.291292;node_341:29.291292;node_341:29.291292;node_341:29.291292;node_341:29.291292;node_341:29.291292;node_341:29.291292;node_341:29.291292;node_341:29.291292;node_807:29.301382;node_807:29.301382;node_807:29.301382;node_807:29.301382;node_807:29.301382;node_807:29.301382;node_807:29.301382;node_807:29.301382;node_807:29.301382;node_895:29.309252;node_895:29.309252;node_895:29.309252;node_895:29.309252;node_895:29.309252;node_405:29.312993;node_405:29.312993;node_49:29.327414;node_49:29.327414;node_49:29.327414;node_49:29.327414;node_49:29.327414;node_49:29.327414;node_49:29.327414;node_49:29.327414;node_49:29.327414;node_49:29.327414;node_797:29.351839;node_797:29.351839;node_797:29.351839;node_797:29.351839;node_797:29.351839;node_797:29.351839;node_372:29.397466;node_372:29.397466;node_372:29.397466;node_372:29.397466;node_372:29.397466;node_372:29.397466;node_372:29.397466;node_576:29.438698;node_576:29.438698;node_576:29.438698;node_576:29.438698;node_576:29.438698;node_576:29.438698;node_576:29.438698;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_223:29.449299;node_865:29.485412;node_865:29.485412;node_865:29.485412;node_865:29.485412;node_865:29.485412;node_865:29.485412;node_608:29.489902;node_608:29.489902;node_608:29.489902;node_608:29.489902;node_608:29.489902;node_608:29.489902;node_608:29.489902;node_697:29.503004;node_697:29.503004;node_697:29.503004;node_697:29.503004;node_697:29.503004;node_697:29.503004;node_697:29.503004;node_697:29.503004;node_697:29.503004;node_779:29.513955;node_779:29.513955;node_696:29.528820;node_696:29.528820;node_696:29.528820;node_696:29.528820;node_696:29.528820;node_696:29.528820;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_906:29.549867;node_129:29.558183;node_548:29.564080;node_548:29.564080;node_548:29.564080;node_924:29.567295;node_924:29.567295;node_924:29.567295;node_924:29.567295;node_924:29.567295;node_924:29.567295;node_924:29.567295;node_924:29.567295;node_924:29.567295;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_839:29.567302;node_878:29.587420;node_878:29.587420;node_878:29.587420;node_878:29.587420;node_878:29.587420;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_777:29.614969;node_654:29.625110;node_654:29.625110;node_654:29.625110;node_654:29.625110;node_654:29.625110;node_654:29.625110;node_654:29.625110;node_654:29.625110;node_654:29.625110;node_188:29.629325;node_188:29.629325;node_188:29.629325;node_188:29.629325;node_188:29.629325;node_188:29.629325;node_188:29.629325;node_105:29.632580;node_105:29.632580;node_105:29.632580;node_105:29.632580;node_105:29.632580;node_105:29.632580;node_105:29.632580;node_105:29.632580;node_105:29.632580;node_105:29.632580;node_234:29.638189;node_504:29.649980;node_504:29.649980;node_504:29.649980;node_504:29.649980;node_504:29.649980;node_504:29.649980;node_504:29.649980;node_504:29.649980;node_351:29.659166;node_351:29.659166;node_351:29.659166;node_351:29.659166;node_351:29.659166;node_351:29.659166;node_351:29.659166;node_912:29.663283;node_912:29.663283;node_912:29.663283;node_912:29.663283;node_912:29.663283;node_912:29.663283;node_534:29.678386;node_534:29.678386;node_534:29.678386;node_534:29.678386;node_998:29.687485;node_998:29.687485;node_998:29.687485;node_998:29.687485;node_998:29.687485;node_998:29.687485;node_848:29.725342;node_215:29.740820;node_215:29.740820;node_215:29.740820;node_215:29.740820;node_215:29.740820;node_215:29.740820;node_215:29.740820;node_215:29.740820;node_215:29.740820;node_978:29.747158;node_978:29.747158;node_978:29.747158;node_978:29.747158;node_978:29.747158;node_978:29.747158;node_285:29.758407;node_285:29.758407;node_285:29.758407;node_285:29.758407;node_285:29.758407;node_285:29.758407;node_285:29.758407;node_285:29.758407;node_285:29.758407;node_285:29.758407;node_575:29.765783;node_575:29.765783;node_575:29.765783;node_575:29.765783;node_575:29.765783;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_810:29.766968;node_643:29.768200;node_643:29.768200;node_643:29.768200;node_643:29.768200;node_643:29.768200;node_643:29.768200;node_361:29.777232;node_361:29.777232;node_361:29.777232;node_361:29.777232;node_361:29.777232;node_361:29.777232;node_361:29.777232;node_361:29.777232;node_361:29.777232;node_764:29.786149;node_764:29.786149;node_764:29.786149;node_764:29.786149;node_764:29.786149;node_764:29.786149;node_764:29.786149;node_43:29.795401;node_43:29.795401;node_43:29.795401;node_43:29.795401;node_43:29.795401;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_734:29.806194;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_389:29.819173;node_606:29.825886;node_606:29.825886;node_828:29.841928;node_828:29.841928;node_841:29.858089;node_841:29.858089;node_841:29.858089;node_841:29.858089;node_125:29.875377;node_125:29.875377;node_751:29.878023;node_751:29.878023;node_751:29.878023;node_751:29.878023;node_751:29.878023;node_751:29.878023;node_751:29.878023;node_751:29.878023;node_751:29.878023;node_789:29.889626;node_789:29.889626;node_789:29.889626;node_789:29.889626;node_789:29.889626;node_789:29.889626;node_789:29.889626;node_662:29.890695;node_662:29.890695;node_662:29.890695;node_662:29.890695;node_662:29.890695;node_662:29.890695;node_483:29.897416;node_483:29.897416;node_483:29.897416;node_483:29.897416;node_483:29.897416;node_483:29.897416;node_483:29.897416;node_587:29.902190;node_587:29.902190;node_587:29.902190;node_587:29.902190;node_587:29.902190;node_587:29.902190;node_587:29.902190;node_587:29.902190;node_587:29.902190;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_910:29.923810;node_658:29.958234;node_658:29.958234;node_658:29.958234;node_658:29.958234;node_658:29.958234;node_658:29.958234;node_195:29.973368;node_195:29.973368;node_195:29.973368;node_195:29.973368;node_195:29.973368;node_195:29.973368;node_195:29.973368;node_195:29.973368;node_195:29.973368;node_195:29.973368;node_945:29.982060"
    list = str.split(';')
    print(len(list))
#     analyze_csv_structure()