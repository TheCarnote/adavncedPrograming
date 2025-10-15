"""
Script pour générer des données synthétiques pour le projet de graphe publicitaire

Usage:
    python generate_data.py --nodes 5000 --ads 500
"""

import numpy as np
import pandas as pd
import argparse
import os


def generate_nodes(num_nodes: int, num_features: int = 50, num_clusters: int = 6) -> pd.DataFrame:
    """
    Génère des nœuds réguliers avec des features aléatoires
    
    Args:
        num_nodes: Nombre de nœuds à générer
        num_features: Nombre de features par nœud (50 par défaut)
        num_clusters: Nombre de clusters (0-5 par défaut)
        
    Returns:
        DataFrame avec les nœuds
    """
    print(f"\n🔧 Génération de {num_nodes} nœuds avec {num_features} features...")
    
    data = {
        'node_id': [f'node_{i+1}' for i in range(num_nodes)]
    }
    
    # Générer les features (valeurs entre 0 et 100)
    for feature_idx in range(1, num_features + 1):
        # Utiliser une distribution normale centrée autour de 50
        features = np.random.normal(loc=50, scale=25, size=num_nodes)
        # Limiter entre 0 et 100
        features = np.clip(features, 0, 100)
        data[f'feature_{feature_idx}'] = features
    
    # Assigner des clusters aléatoires (0 à num_clusters-1)
    data['cluster_id'] = np.random.randint(0, num_clusters, size=num_nodes)
    
    df = pd.DataFrame(data)
    
    print(f"✅ {len(df)} nœuds générés")
    print(f"   - Features: {num_features}")
    print(f"   - Clusters: {num_clusters} (0-{num_clusters-1})")
    print(f"   - Feature min/max: [{df[[f'feature_{i}' for i in range(1, num_features+1)]].min().min():.2f}, {df[[f'feature_{i}' for i in range(1, num_features+1)]].max().max():.2f}]")
    
    return df


def generate_ads(num_ads: int, num_features: int = 50, min_D: float = 5, max_D: float = 30) -> pd.DataFrame:
    """
    Génère des ads avec des vecteurs Y et des rayons D
    
    Args:
        num_ads: Nombre d'ads à générer
        num_features: Nombre de features (doit correspondre aux nœuds)
        min_D: Rayon D minimum
        max_D: Rayon D maximum
        
    Returns:
        DataFrame avec les ads
    """
    print(f"\n🔧 Génération de {num_ads} ads avec {num_features} dimensions Y...")
    
    data = {
        'point_A': [f'ads_{i+1}' for i in range(num_ads)],
        'Y_vector': [],
        'D': []
    }
    
    for i in range(num_ads):
        # Générer le vecteur Y
        # Valeurs aléatoires entre 0 et 0.25 (pondération)
        # Certaines dimensions ont un poids plus élevé pour simuler des features importantes
        Y = np.random.exponential(scale=0.05, size=num_features)
        
        # Ajouter quelques valeurs plus élevées (features importantes)
        important_features = np.random.choice(num_features, size=int(num_features * 0.1), replace=False)
        Y[important_features] = np.random.uniform(0.05, 0.25, size=len(important_features))
        
        # Limiter entre 0 et 0.25
        Y = np.clip(Y, 0, 0.25)
        
        # Formater avec 4 décimales et joindre avec ';'
        Y_str = ';'.join([f'{val:.4f}' for val in Y])
        data['Y_vector'].append(Y_str)
        
        # Générer le rayon D (entier entre min_D et max_D)
        D = np.random.randint(min_D, max_D + 1)
        data['D'].append(D)
    
    df = pd.DataFrame(data)
    
    print(f"✅ {len(df)} ads générés")
    print(f"   - Dimensions Y: {num_features}")
    print(f"   - Rayon D: [{df['D'].min()}, {df['D'].max()}]")
    print(f"   - Rayon D moyen: {df['D'].mean():.1f}")
    
    # Afficher un exemple
    print(f"\n📋 Exemple d'ad:")
    print(f"   ID: {df.iloc[0]['point_A']}")
    print(f"   Y (5 premiers): {';'.join(df.iloc[0]['Y_vector'].split(';')[:5])}")
    print(f"   D: {df.iloc[0]['D']}")
    
    return df


def save_csv(df: pd.DataFrame, filename: str, output_dir: str = '.'):
    """
    Sauvegarde un DataFrame en CSV
    
    Args:
        df: DataFrame à sauvegarder
        filename: Nom du fichier
        output_dir: Répertoire de sortie
    """
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    
    file_size = os.path.getsize(filepath) / (1024 * 1024)  # en MB
    print(f"💾 Fichier sauvegardé: {filepath}")
    print(f"   Taille: {file_size:.2f} MB")
    print(f"   Lignes: {len(df)}")
    print(f"   Colonnes: {len(df.columns)}")


def main():
    parser = argparse.ArgumentParser(
        description='Génère des données synthétiques pour le graphe publicitaire',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Générer 5000 nodes et 500 ads
  python generate_data.py --nodes 5000 --ads 500
  
  # Générer avec des paramètres personnalisés
  python generate_data.py --nodes 10000 --ads 1000 --features 100 --min-d 3 --max-d 50
  
  # Générer dans un dossier spécifique
  python generate_data.py --nodes 5000 --ads 500 --output ./data
        """
    )
    
    parser.add_argument(
        '--nodes',
        type=int,
        default=5000,
        help='Nombre de nœuds réguliers à générer (défaut: 5000)'
    )
    
    parser.add_argument(
        '--ads',
        type=int,
        default=500,
        help='Nombre d\'ads à générer (défaut: 500)'
    )
    
    parser.add_argument(
        '--features',
        type=int,
        default=50,
        help='Nombre de features par nœud/ad (défaut: 50)'
    )
    
    parser.add_argument(
        '--clusters',
        type=int,
        default=6,
        help='Nombre de clusters pour les nœuds (défaut: 6)'
    )
    
    parser.add_argument(
        '--min-d',
        type=float,
        default=5,
        help='Rayon D minimum pour les ads (défaut: 5)'
    )
    
    parser.add_argument(
        '--max-d',
        type=float,
        default=30,
        help='Rayon D maximum pour les ads (défaut: 30)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='.',
        help='Répertoire de sortie (défaut: répertoire courant)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Seed pour la reproductibilité (défaut: aléatoire)'
    )
    
    args = parser.parse_args()
    
    # Définir le seed si spécifié
    if args.seed is not None:
        np.random.seed(args.seed)
        print(f"🎲 Seed défini: {args.seed}")
    
    print(f"\n{'='*60}")
    print(f"🎲 GÉNÉRATION DE DONNÉES SYNTHÉTIQUES")
    print(f"{'='*60}")
    print(f"📊 Paramètres:")
    print(f"   - Nœuds: {args.nodes}")
    print(f"   - Ads: {args.ads}")
    print(f"   - Features: {args.features}")
    print(f"   - Clusters: {args.clusters}")
    print(f"   - Rayon D: [{args.min_d}, {args.max_d}]")
    print(f"   - Sortie: {args.output}")
    
    # Créer le répertoire de sortie si nécessaire
    os.makedirs(args.output, exist_ok=True)
    
    # Générer les nœuds
    nodes_df = generate_nodes(
        num_nodes=args.nodes,
        num_features=args.features,
        num_clusters=args.clusters
    )
    
    # Générer les ads
    ads_df = generate_ads(
        num_ads=args.ads,
        num_features=args.features,
        min_D=args.min_d,
        max_D=args.max_d
    )
    
    # Sauvegarder
    print(f"\n{'='*60}")
    print(f"💾 SAUVEGARDE DES FICHIERS")
    print(f"{'='*60}")
    
    save_csv(nodes_df, 'adsSim_data_nodes_generated.csv', args.output)
    print()
    save_csv(ads_df, 'queries_structured_generated.csv.csv', args.output)
    
    print(f"\n{'='*60}")
    print(f"✅ GÉNÉRATION TERMINÉE")
    print(f"{'='*60}")
    print(f"📁 Fichiers générés dans: {args.output}")
    print(f"   - adsSim_data_nodes_generated.csv: {args.nodes} nœuds × {args.features} features")
    print(f"   - queries_structured_generated.csv: {args.ads} ads × {args.features} dimensions Y")
    print(f"\n💡 Pour utiliser ces fichiers:")
    print(f"   1. Copiez-les dans le dossier backend/")
    print(f"   2. Relancez le backend: python main.py")
    print(f"   3. Construisez le graphe avec le bouton '🔨 Construire'")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()